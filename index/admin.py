from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Medicines, UserRequest, Street, Address

admin.site.register(CustomUser)
admin.site.register(Medicines)
admin.site.register(UserRequest)
admin.site.register(Street)
admin.site.register(Address)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserCreationForm.Meta.model
        fields = '__all__'
        field_classes = UserCreationForm.Meta.field_classes


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = CustomUser

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': (
            'first_name', 'last_name', 'after_name', 'email', 'iin', 'serv')}),
    )
    fieldsets = BaseUserAdmin.fieldsets + (
        (_('Permissions'), {'fields': (
            'first_name', 'last_name', 'after_name', 'email', 'iin', 'serv')}),
    )
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2', 'serv')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
