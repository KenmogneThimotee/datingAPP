
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import ( CustumObtainTokenPairView, RegisterView,
                    validate_code, resend_validation_code,
                    send_password_reset_code, validate_password_reset_code,
                    reset_password, change_password)

urlpatterns = [
    path('login', CustumObtainTokenPairView.as_view(), name='token_obtain_pair'),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterView.as_view(), name='auth_register'),
    path('validate', validate_code, name='validation'),
    path('resend-validation-code', resend_validation_code, name='resend-validation-code'),
    path('send-reset-code', send_password_reset_code, name='password-reset-code'),
    path('validate-password-reset-code', validate_password_reset_code, name='validate-password-reset-code'),
    path('reset-password', reset_password, name='reset-password'),
    path('change-password', change_password, name='change-password')
]
