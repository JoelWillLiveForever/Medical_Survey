from django.contrib.auth.base_user import BaseUserManager
from django.db import models
import re


class PatientManager(BaseUserManager):
    use_in_migrations = True

    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        isValidEmailReg = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$'
        isValidPhoneReg = r'\+?(?:[^\d\s]*\d){11,18}'
        if not email:
            raise ValueError(('The Email must be set'))
        if not re.match(isValidEmailReg, email):
            raise ValueError(('Incorrect Email'))
        # if not phone:
        #     raise ValueError(('The Phone must be set'))
        # if not re.match(isValidPhoneReg, phone):
        #     raise ValueError(('Incorrect phone number'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)






