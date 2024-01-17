from django.shortcuts import render

# Create your views here.
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CustumTokenObtainPairSerializer
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.response import Response
from .models import User
from .serializers import RegisterSerializer, PasswordResetCodeSerializer, ValidatePasswordResetCodeSerializer, ResetPasswordSerializer
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes
from rest_framework_simplejwt import authentication
from .helpers import random_with_N_digits
from django.core.mail import send_mail



class CustumObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustumTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    

@api_view(['POST'])
@authentication_classes([authentication.JWTAuthentication])
def validate_code(request):
    
    print(request.user)
    user = request.user
    if user.validated:
        return Response({"message": "Already verified"})
    validation_code = request.data['validation_code']
    
    if user.validation_code != validation_code:
        return Response(data={"message": "Verification code is not correct"}, status=HTTP_400_BAD_REQUEST)
    user.validated = True
    user.save()
    return Response({"message": "Verification code match"}, status=HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([authentication.JWTAuthentication])
def resend_validation_code(request):
    
    user = request.user
    user.validation_code = random_with_N_digits(5)
    user.save()
    
    subject = 'Welcome to Trust'
    message = f'Thank you for creating an account! your verification code is {user.validation_code}'
    from_email = 'thimoteekenmogne@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)

    return Response({"message": "Verification code sent"})

@api_view(['POST'])
@authentication_classes([AllowAny])
def send_password_reset_code(request):
    
    serializer = PasswordResetCodeSerializer(request.data)
    
    if serializer.is_valid():

        email  = serializer.validated_data['email']
        reset_code = random_with_N_digits(5)
        
        user = User.objects.get(email=email)
        user.reset_code = reset_code
        user.save()
        
        subject = 'Password Reset'
        message = f'Your password reet code is {reset_code}'
        from_email = 'thimoteekenmogne@gmail.com'
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

        return Response({"message": "Verification code sent"})
    else:
        return Response({"message": serializer.errors}, status=HTTP_400_BAD_REQUEST)

        
    
@api_view(['POST'])
@authentication_classes([AllowAny])
def validate_password_reset_code(request):
    
    serializer = ValidatePasswordResetCodeSerializer(request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        reset_code = serializer.validated_data['reset_code']
        
        user = User.objects.get(email=email)
        
        if user.reset_code != reset_code:
            return Response(data={"message": "Verification code is not correct"}, status=HTTP_400_BAD_REQUEST)
        user.reset_code_validated = True
        user.save()
        return Response({"message": "Verification code match"}, status=HTTP_200_OK)
    else:
        return Response({"message": serializer.errors}, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([AllowAny])
def reset_password(request):
    
    serializer = ResetPasswordSerializer(request.data)
    
    if serializer.is_valid():
        user = User.objects.get(email=serializer.validated_data['email'])
        if user.reset_code_validated:
            user.set_password(serializer.validated_data['password'])
            user.reset_code_validated = False
            user.reset_code = None
            user.save()
            
            return Response({"message": "Password reset successfully"})
        else:
            return Response({"message": "Not allowed"}, status=HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": serializer.errors}, status=HTTP_400_BAD_REQUEST)
        
    
@api_view(['POST'])
@authentication_classes([authentication.JWTAuthentication])
def change_password(request):
    
    serializer = ResetPasswordSerializer(request.data)
    
    if serializer.is_valid():
        user = request.user
        if user.reset_code_validated:
            user.set_password(serializer.validated_data['password'])
            user.save()
            
            return Response({"message": "Password changed successfully"})
        else:
            return Response({"message": "Not allowed"}, status=HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": serializer.errors}, status=HTTP_400_BAD_REQUEST)
        
    