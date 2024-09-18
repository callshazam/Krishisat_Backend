import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    '''
    Creating a manager for a custom user model.
    '''
    def create_user(self, phone_number,user_name, password=None, **extra_fields):
        """
        Create and return a `User` with a phone number and password.
        """
        if not phone_number:
            raise ValueError('Users must have a phone number')

        user = self.model(
            phone_number=phone_number,
            user_name=user_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, user_name, password=None, **extra_fields):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if not password:
            raise TypeError('Superusers must have a password.')
        
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        user = self.create_user(
            phone_number=phone_number,
            user_name=user_name,
            password=password,
            **extra_fields
        )
        return user


    def create_farmeruser(self,phone_number, user_name, password):
        if password is None:
            raise TypeError('Farmers must have a password')
        user = self.create_user(phone_number, user_name, password)
        user.is_farmer = True
        user.save()
        return user

    def create_staffuser(self, phone_number, user_name, password):
        if password is None:
            raise TypeError('Staff must have a password')
        user = self.create_user(phone_number, user_name, password)
        user.is_staff = True
        user.save()
        return user

class CustomUser(AbstractBaseUser):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=15, unique=True)
    user_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_farmer = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['user_name']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.user_name} ({self.phone_number})"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    class Meta:
        db_table = "login"