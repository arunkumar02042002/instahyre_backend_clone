from rest_framework import serializers

# 
from django.contrib.auth import get_user_model


User = get_user_model()

class UserLoginSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "username",
            "first_name",
            "last_name",
            "user_type",
            "date_joined",
            "is_active",
            "is_superuser"
        )
        read_only_fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "user_type",
            "date_joined",
            "is_active",
            "is_superuser"
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }
    
    def validate_username_or_email(self, value):
        return value.lower()