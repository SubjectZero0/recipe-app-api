from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


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