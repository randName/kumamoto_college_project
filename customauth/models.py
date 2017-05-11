from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _


class KUserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Email is required.')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must be staff.')

        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must be superuser.')

        return self.create_user(email, password, **kwargs)


class KUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    is_staff = models.BooleanField(
        _('staff status'), default=False, help_text=_('Can access admin site.')
    )

    is_active = models.BooleanField(
        _('active'), default=True, help_text=_('Use this instead of deleting.')
    )

    given_name = models.CharField(max_length=50)
    family_name = models.CharField(max_length=50, blank=True)
    middle_name = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    objects = KUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return '%s %s' % (self.given_name, self.family_name.upper())

    def get_short_name(self):
        return self.given_name
