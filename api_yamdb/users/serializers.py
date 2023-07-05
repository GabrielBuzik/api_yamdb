from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.validators import UniqueValidator

import re

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    role = serializers.ChoiceField(default='user',
        choices=User.USER_TYPE_CHOICES)

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User
    
    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError("Username cannot be 'me'.")
        if len(value) > 150:
            raise serializers.ValidationError("Username too long.")
        
        pattern = r'^[\w.@+-]+\z'

        return value