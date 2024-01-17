from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from .helpers import random_with_N_digits


class CustumTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(CustumTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['email'] = user.email
        return token
  
  

class RegisterSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            validation_code=random_with_N_digits(5)
        )

        user.set_password(validated_data['password'])
        user.save()
        
        subject = 'Welcome to Trust'
        message = f'Thank you for creating an account! your verification code is {user.validation_code}'
        from_email = 'thimoteekenmogne@gmail.com'
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

        return user
    

class PasswordResetCodeSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)
    
class ValidatePasswordResetCodeSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)
    reset_code = serializers.CharField(max_length=5, required=True)

class ResetPasswordSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs
    
class ChangePasswordSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs