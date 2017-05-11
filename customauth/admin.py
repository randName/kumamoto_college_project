from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import ModelForm, CharField, PasswordInput, ValidationError

from .models import KUser


class UserCreationForm(ModelForm):
    """A form for creating new users. Includes all the required fields."""
    password1 = CharField(label='Password', widget=PasswordInput)
    password2 = CharField(label='Password confirmation', widget=PasswordInput)

    class Meta:
        model = KUser
        fields = ('email', 'given_name', 'family_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(ModelForm):
    """A form for updating users. Includes all the fields on the user, but
    replaces the password field with admin's password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = KUser
        fields = ('email', 'password', 'given_name', 'family_name', 'is_active', 'is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'given_name', 'family_name', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('given_name', 'family_name')}),
        ('Permissions', {'fields': ('is_staff',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
    )

    search_fields = ('email', 'given_name', 'family_name')
    ordering = ('email',)


admin.site.register(KUser, UserAdmin)
