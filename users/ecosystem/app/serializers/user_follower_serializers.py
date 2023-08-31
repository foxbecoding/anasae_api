from rest_framework import serializers
from users.models import *
import os


env = os.getenv

class UserFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollower
        fields = [
            'pk',
            'user',
            'follower'
        ]

class CreateUserFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollower
        fields = [
            'user',
            'follower'
        ]
    
    def validate(self, attrs):
        user = attrs.get('user')
        follower = attrs.get('follower')

        if UserFollower.objects.filter(user_id=user.id).filter(follower_id=follower.id).exists():
            msg = 'Already following this user.'
            raise serializers.ValidationError({"errors": msg}, code='authorization')
        
        instance = UserFollower.objects.create(
            user = user,
            follower = follower
        )

        instance.save()

        attrs['user_follower'] = instance
        return attrs