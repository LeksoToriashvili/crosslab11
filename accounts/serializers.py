from rest_framework import serializers

from accounts.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    # Enforcing password as a write-only field
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'is_active', 'is_staff']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False},
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True},
        }

    def create(self, validated_data):
        """
        Create a new CustomUser instance with a hashed password.
        """
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
