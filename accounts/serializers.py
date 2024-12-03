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
            'is_active': {'read_only': True},  # You might not want users to set this directly
            'is_staff': {'read_only': True},  # Staff status is usually admin-controlled
        }

    def create(self, validated_data):
        """
        Create a new CustomUser instance with a hashed password.
        """
        password = validated_data.pop('password')  # Extract password before user creation
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()
        return user
