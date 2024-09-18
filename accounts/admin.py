from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    list_display = ('id','phone_number', 'user_name', 'is_staff', 'is_superuser', 'is_farmer')
    list_filter = ('is_staff', 'is_superuser', 'is_farmer', 'is_active')
    
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (_('Personal Info'), {'fields': ('user_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_farmer')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'user_name', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_farmer'),
        }),
    )
    
    search_fields = ('phone_number', 'user_name')
    ordering = ('phone_number',)
    filter_horizontal = ()

# Register the CustomUser model using the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)
