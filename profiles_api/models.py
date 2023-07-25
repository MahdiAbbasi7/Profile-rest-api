from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    ''' Manager for user profiles'''
    def create_user(self, email, name, password=None):
        ''' Create a new user profile '''
        if not email :
            raise ValueError("User is must have a email address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password=None):
        ''' Create and save a new super user profile '''
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    ''' Database model for users and fields '''
    email = models.EmailField(max_length=250, unique=True)
    name = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # Access to django admin

    objects = UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        "Return full name of user"
        return self.name
    def get_short_name(self):
        "Return short name of user"
        return self.email
    def __str__(self):
        "Return string representation email of user"
        return self.email
