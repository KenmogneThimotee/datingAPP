from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ('first_name', 'last_name', 'email')
    list_filter = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'old_password', 'new_password', 'new_password2')}),
        ('Personal Information', {'fields': ('first_name', 'last_name')}),
    )
    
    add_fieldsets = (
        (None, {'fields': ('email', 'password', 'password2')}),
        ('Personal Information', {'fields': ('first_name', 'last_name')}),
    )
    
    ordering = ('email',)
    
# Register your models here.
admin.site.register(User, CustomUserAdmin)
