from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from users.models import *
from utils.helpers import create_uid
from PIL import Image
from utils.helpers import create_uid
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
            'date_of_birth',
            'agreed_to_toa',
            'is_active',
            'stripe_customer_id',
            'addresses',
            'logins',
            'profiles',
            'gender_choice'
        ]

class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
        ]

class CreateUserSerializer(serializers.ModelSerializer):
    
    # Create hidden password field for password confirmation
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

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
            'agreed_to_toa'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        agreed_to_toa = attrs.get('agreed_to_toa')
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        # Check if passwords matches
        if password != confirm_password:
            msg = 'Passwords must match.'
            raise serializers.ValidationError({"password": msg}, code='authorization')
        
        #Check if user agreed to terms of agreement
        if not agreed_to_toa:
            msg = 'Please agree to our Terms.'
            raise serializers.ValidationError({"agreed_to_toa": msg}, code='authorization')

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
        user = User(
            uid = uid,
            first_name = attrs.get('first_name'),
            last_name = attrs.get('last_name'),
            email = attrs.get('email').lower(),
            password = make_password(attrs.get('password')),
            agreed_to_toa = attrs.get('agreed_to_toa'), 
            date_of_birth = attrs.get('date_of_birth'), 
            stripe_customer_id = stripe_customer_id
        )
        user.save()
        attrs['user'] = user
        return attrs  

class AuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'write_only': True},
        }

    email = serializers.CharField(
        label="Email",
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
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:

            # Find user with username/email and password combination
            user = self.authenticate(email, password)
    
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: Invalid authentication credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "email" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')

        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs
    
    def authenticate(self, username, password) -> User:
        if not User.objects.filter(username=username).exists():
            return None
        User_Instance = User.objects.get(username=username)     
        if not check_password(password, User_Instance.password):
            return None
        return User_Instance
        
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLogin
        fields = [
            'pk',
            'user',
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
            'pk',
            'user_gender',
            'user'
        ]

class UserProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileImage
        fields = [
            'pk',
            'user_profile',
            'image'
        ]

class CreateUserProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileImage
        fields = [
            'user_profile'
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
        user_profile = attrs.get('user_profile')

        img = Image.open(image)
        valid_formats = ['PNG', 'JPEG']
        if img.format not in valid_formats:
            msg = 'Image must be in PNG or JPEG format'
            raise serializers.ValidationError({"image": msg}, code='authorization')
        
        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)
        image_name = create_uid('up-')+f'-{time_stamp}.{img.format.lower()}'
        image_path = str(env('CDN_USER_PROFILE_DIR')+image_name)
    
        upload = requests.post(
            f'{env("CDN_HOST_API")}{env("CDN_UPLOAD_IMAGE")}',
            data = {
                "file_path": env('CDN_USER_PROFILE_DIR'),
                "image_name": image_name
            },
            files={ "image": image.file.getvalue() }
        )

        if upload.status_code != 200:
            msg = 'Please try again'
            raise serializers.ValidationError({"image": msg}, code='authorization')

        user_profile_image = UserProfileImage.objects.create(
            user_profile = user_profile,
            image = image_path
        )

        user_profile_image.save()
        attrs['user_profile_image'] = user_profile_image
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
            'full_name',
            'phone_number',
            'street_address',
            'street_address_ext',
            'country',
            'state',
            'city',
            'postal_code'
        ]
    
    def validate(self, attrs):
        User_Address_Instance = UserAddress.objects.create(
            user = self.context['user'],
            full_name = attrs.get('full_name'),
            phone_number = attrs.get('phone_number'),
            street_address = attrs.get('street_address'),
            street_address_ext = attrs.get('street_address_ext'),
            country = attrs.get('country'),
            state = attrs.get('state'),
            city = attrs.get('city'),
            postal_code = attrs.get('postal_code')
        )
        User_Address_Instance.save()
        attrs['address'] = User_Address_Instance
        return attrs 

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