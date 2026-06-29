from rest_framework import serializers
from django.contrib.auth.models import User
from contact.models import Contact


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = [
            'id', 'name', 'email', 'phone',
            'address', 'is_favourite', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Name must be at least 2 characters."
            )
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                "Name cannot contain numbers."
            )
        return value.strip()

    def validate_phone(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain only digits."
            )
        if value and len(value) > 15:
            raise serializers.ValidationError(
                "Phone number cannot exceed 15 digits."
            )
        return value


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password2': 'Passwords do not match.'}
            )
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)