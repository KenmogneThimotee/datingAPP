from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import Dislikes, Likes, User, SEX_CHOICES, Match
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from .helpers import random_with_N_digits
from django.contrib.gis.geos import fromstr


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
        fields = ('password', 'password2', 'email', 'first_name', 'last_name', 'sex',
                  'preferred_sex', 'preferred_age_min',
                  'preferred_age_max', 'last_location', 'preferred_radius', 'profile_picture')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'sex': {'required': True},
            'preferred_sex': {'required': True},
            'preferred_age_min': {'required': True},
            'preferred_age_max': {'required': True},
            'last_location': {'required': True},
            'preferred_radius': {'required': True},
            'profile_picture': {'required': True}
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
            sex=validated_data['sex'],
            preferred_sex=validated_data['preferred_sex'],
            preferred_age_min=validated_data['preferred_age_min'],
            preferred_age_max=validated_data['preferred_age_max'],
            last_location=validated_data['last_location'],
            preferred_radius=validated_data['preferred_radius'],
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

class ResetPasswordSerializer(serializers.Serializer):
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs
    
class ChangePasswordSerializer(serializers.Serializer):
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs
    
class UserSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'date_of_birth', 'sex',
                  'preferred_sex', 'preferred_age_min',
                  'preferred_age_max', 'last_location', 'preferred_radius', 'profile_picture']
        
class LikesSerializers(serializers.ModelSerializer):
    
    user = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())
    liked = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())
    
    class Meta:
        model = Likes
        fields = ['user', 'liked', 'date']
        
    def validate(self, attrs):
        
        request = self.context.get('request')
        
        user = User.objects.get(email=attrs['user'])
        liked = User.objects.get(email=attrs['liked'])
        
        if user.email != request.user.email:
            raise serializers.ValidationError("You are not allowed to perform this action")
        elif len(Likes.objects.filter(user=user, liked=liked)) > 1:
            raise serializers.ValidationError("You have already like this user")
        elif user.email == liked.email:
            raise serializers.ValidationError("This is the same user it's not allowed")
        else:
            return super().validate(attrs)
        

    def create(self, validated_data):

        
        user = User.objects.get(email=validated_data['user'])
        liked = User.objects.get(email=validated_data['liked'])
        
        
        if user.email in [usr.liked.email for usr in liked.initial_user.all()]:
            
            match = Match.objects.create(user1=user, user2=liked)
            match.user1 = user 
            match.user2 = liked
            match.save()
        
        likes = Likes(user=user, liked=liked)
        likes.save()
        
        return likes
        
class DislikesSerializers(serializers.ModelSerializer):
    
    user = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())
    disliked = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())
    
    class Meta:
        model = Dislikes
        fields = '__all__'
        
    def validate(self, attrs):
        
        request = self.context.get('request')
        
        user = User.objects.get(email=attrs['user'])
        liked = User.objects.get(email=attrs['liked'])
        
        if user.email != request.user.email:
            raise serializers.ValidationError("You are not allowed to perform this action")
        elif len(Dislikes.objects.filter(user=user, liked=liked)) > 1:
            raise serializers.ValidationError("You have already dislike this user")
        elif user.email == liked.email:
            raise serializers.ValidationError("This is the same user it's not allowed")
        else:
            return super().validate(attrs)
        

    def create(self, validated_data):

        
        user = User.objects.get(email=validated_data['user'])
        disliked = User.objects.get(email=validated_data['disliked'])
        
    
        
        dislikes = Likes(user=user, liked=disliked)
        dislikes.save()
        
        return dislikes
        
class ListUserListSerializer(serializers.ModelSerializer):
    preferred_sex = serializers.ChoiceField(choices=SEX_CHOICES, default='male')
    sex = serializers.ChoiceField(choices=SEX_CHOICES, default='male')
    distance = serializers.SerializerMethodField(read_only=True)
    smaller_radius = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['smaller_radius', 'distance','id', 'email', 'first_name', 'last_name', 'date_of_birth', 'sex',
                  'preferred_sex', 'preferred_age_min',
                  'preferred_age_max', 'last_location', 'preferred_radius', 'profile_picture']

    def get_distance(self, obj):
        if hasattr(obj, 'distance'):
            return round(obj.distance.m, 1)
        else:
            return None

    def to_representation(self, instance):
        ret = super(ListUserListSerializer, self).to_representation(instance)
        pnt = fromstr(ret['last_location'])
        ret['last_location'] = {'longitude': pnt.coords[0], 'latitude': pnt.coords[1]}
        return ret