from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

class UserSerializer(ModelSerializer):
    """Serializer for Custom User"""

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'name', 'password']
        extra_kwargs = {'password': {'write_only': True},
                        'id' : {'read_only':True},
                        }

    def create(self, validated_data):
        """Create a User"""
        return get_user_model().objects.create_user(**validated_data)



    def update(self, instance, validated_data):
        """Updates and hashes updated user password"""

        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class UserLoginSerializer(serializers.Serializer):
    """Serializer for handling User Login and token generation"""

    email = serializers.EmailField()
    password = serializers.CharField(style = {'input_type' : 'password'})

    def validate(self, data):
        """
        with given data(credentials), attempts to authenticate user.

        """
        email = data.get('email')
        password = data.get('password')

        user = authenticate(
            username = email,
            password = password
        )

        if user is not None:
            data['user'] = user
            return data
        else:
            msg = 'Could not authenticate. Make sure you type the correct email and/or password'
            raise serializers.ValidationError(msg, code='authorization')