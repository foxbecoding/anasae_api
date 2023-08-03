from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from users.models import *
from utils.helpers import create_uid
from PIL import Image
import stripe, requests, os, calendar, time

env = os.getenv

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'pk',
            'uid',
            'first_name',
            'last_name',
            'email',
            'username',
            'display_name',
            'date_of_birth',
            'agreed_to_toa',
            'is_active',
            'stripe_customer_id',
            'addresses',
            'logins',
            'gender_choice',
            'image',
            'payment_methods'
        ]

class EditUserSerializer(serializers.ModelSerializer):
    
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'display_name',
            'username',
            'password',
            'confirm_password'
        ]

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        attrs['password_changed'] = False
        is_password_change = 'password' in attrs or 'confirm_password' in attrs
        both_passwords_exists = 'password' in attrs and 'confirm_password' in attrs
        
        if is_password_change:
            if not both_passwords_exists:
                msg = 'Passwords must match.'
                raise serializers.ValidationError({'password_error': msg}, code='authorization')
            
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            if password != confirm_password:
                msg = 'Passwords must match.'
                raise serializers.ValidationError({'password_error': msg}, code='authorization')
            
            User_Instance = User.objects.get(pk=str(self.context['request'].user.id))
            User_Instance.password=make_password(password)
            User_Instance.save()
            attrs['password_changed'] = True
        
        return attrs

class CreateUserSerializer(serializers.ModelSerializer):
    
    # Create hidden password field for password confirmation
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    gender = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password',
            'confirm_password',
            'date_of_birth',
            'gender'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        username = attrs.get('username').lower()
        email = attrs.get('email').lower()
       
        if User.objects.filter(username=username).exists():
            msg = 'user with this username already exists'
            raise serializers.ValidationError({'username': msg}, code='authorization')

        if User.objects.filter(email=email).exists():
            msg = 'user with this email already exists.'
            raise serializers.ValidationError({'email': msg}, code='authorization')

        # Check if passwords matches
        if password != confirm_password:
            msg = 'Passwords must match.'
            raise serializers.ValidationError({"password": msg}, code='authorization')
        
        #Check if user agreed to terms of agreement
        # if not agreed_to_toa:
        #     msg = 'Please agree to our Terms.'
        #     raise serializers.ValidationError({"agreed_to_toa": msg}, code='authorization')

        uid = create_uid('u-')
        stripe_customer = stripe.Customer.create(
            email = attrs.get('email').lower(),
            name = attrs.get('first_name')+' '+attrs.get('last_name'),
            metadata = {
                "uid": uid
            }                
        )
        stripe_customer_id = stripe_customer.id

        # Save User in database
        User_Instance = User.objects.create(
            uid = uid,
            first_name = attrs.get('first_name'),
            last_name = attrs.get('last_name'),
            email = attrs.get('email').lower(),
            username = attrs.get('username').lower(),
            password = make_password(attrs.get('password')),
            agreed_to_toa = True, 
            date_of_birth = attrs.get('date_of_birth'), 
            stripe_customer_id = stripe_customer_id
        )
        User_Instance.save()

        gender_pk = attrs.get('gender')
        User_Gender_Instance = UserGender.objects.get(pk=gender_pk)
        User_Gender_Choice_Instance = UserGenderChoice.objects.create(
            user_gender = User_Gender_Instance,
            user = User_Instance
        )
        User_Gender_Choice_Instance.save()

        attrs['user'] = User_Instance
        return attrs  

class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=True,
        write_only=True
    )

    def validate(self, attrs):
        # Set username and password from attrs
        username = attrs.get('username')
        password = attrs.get('password')
       
        if username and password:

            # Find user with username/email and password combination
            user = self.authenticate(username, password)
    
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: Invalid authentication credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')

        User_Login_Instance = UserLogin.objects.create(user = user)
        User_Login_Instance.save()
        
        attrs['user'] = user
        return attrs
    
    def authenticate(self, username, password) -> User:
        if not User.objects.filter(username=username).exists():
            return None
        User_Instance = User.objects.get(username=username)     
        if not check_password(password, User_Instance.password):
            return None
        return User_Instance

class UserAuthValidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email'
        ]

    def validate(self, attrs):
        username = attrs.get('username').lower()
        email = attrs.get('email').lower()
       
        if User.objects.filter(username=username).exists():
            msg = 'user with this username already exists'
            raise serializers.ValidationError({'username': msg}, code='authorization')

        if User.objects.filter(email=email).exists():
            msg = 'user with this email already exists.'
            raise serializers.ValidationError({'email': msg}, code='authorization')
        
        return attrs
    
class UserAuthValidateDetailsSerializer(serializers.ModelSerializer):
    birth_month = serializers.CharField(write_only=True)
    birth_day = serializers.CharField(write_only=True)
    birth_year = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'birth_month',
            'birth_day',
            'birth_year'
        ]

class UserAuthValidatePasswordSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = [
            'password',
            'confirm_password'
        ]
    
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        
        # Check if passwords matches
        if password != confirm_password:
            msg = 'Passwords must match.'
            raise serializers.ValidationError({"password": msg}, code='authorization')
        
        return attrs
        
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLogin
        fields = [
            'pk',
            'created'
        ]

class UserGenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGender
        fields = [
            'pk',
            'gender',
            'is_active'
        ]

class UserGenderChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGenderChoice
        fields = [
            'pk'
        ]

class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = [
            'pk',
            'image'
        ]

class CreateUserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = [
            'user'
        ]

    def validate(self, attrs):
        request_data = self.context['request'].data

        if 'image' not in request_data:
            msg = 'Please upload an image'
            raise serializers.ValidationError({"image": msg}, code='authorization')
        
        if not request_data['image']:
            msg = 'Please upload an image'
            raise serializers.ValidationError({"image": msg}, code='authorization')

        image = request_data['image']
        
        img = Image.open(image)
        valid_formats = ['PNG', 'JPEG']
        if img.format not in valid_formats:
            msg = 'Image must be in PNG or JPEG format'
            raise serializers.ValidationError({"image": msg}, code='authorization')
        
        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)
        image_name = create_uid('ui-')+f'-{time_stamp}.{img.format.lower()}'
        image_path = str(env('CDN_USER_IMAGE_DIR')+image_name)
    
        upload = requests.post(
            f'{env("CDN_HOST_API")}{env("CDN_UPLOAD_IMAGE")}',
            data = {
                "file_path": env('CDN_USER_IMAGE_DIR'),
                "image_name": image_name
            },
            files={ "image": image.file.getvalue() }
        )

        if upload.status_code != 200:
            msg = 'Please try again'
            raise serializers.ValidationError({"image": msg}, code='authorization')

        User_Image_Instance = UserImage.objects.create(
            user = attrs.get('user'),
            image = image_path
        )

        User_Image_Instance.save()
        attrs['user_image'] = User_Image_Instance
        return attrs
    
class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = [
            'pk',
            'full_name',
            'phone_number',
            'street_address',
            'street_address_ext',
            'country',
            'state',
            'city',
            'postal_code',
            'is_default'
        ]

class CreateUserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = [
            'user',
            'full_name',
            'phone_number',
            'street_address',
            'street_address_ext',
            'country',
            'state',
            'city',
            'postal_code'
        ]

class EditUserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = [
            'full_name',
            'phone_number',
            'street_address',
            'street_address_ext',
            'country',
            'state',
            'city',
            'postal_code',
            'is_default'
        ]

class UserPaymentMethodSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserPaymentMethod
        fields = [
            'pk',
            'stripe_pm_id'
        ]

class CreateUserPaymentMethodSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserPaymentMethod
        fields = [
            'user',
            'stripe_pm_id'
        ]