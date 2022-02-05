from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)

class UserManager(BaseUserManager):
    def create_superuser(self, number, password=None, is_active=True, usertype=5):
        user_obj = self.model(password=password, number=number)
        user_obj.set_password(password) # change user password
        user_obj.staff = True
        user_obj.is_active = is_active
        user_obj.is_admin=True
        user_obj.save(using=self._db)
        return user_obj

    def create_user(self, number, name, password=None,photo=None, is_active=True, is_staff=False, usertype=4):
        if not number:
            raise ValueError("Users must have an number")
        if not password:
            raise ValueError("Users must have a password")
        if not name:
            raise ValueError("Users must have a name")
        user_obj = self.model( name=name, password=password, number=number)
        user_obj.set_password(password) # change user password
        user_obj.staff = is_staff
        user_obj.is_active = is_active
        user_obj.photo=photo
        user_obj.usertype=usertype
        #user_obj.branch_id=branch_id
        user_obj.save(using=self._db)
        return user_obj
'''
class Branch(models.Model):
    adress=models.CharField(max_length=25, blank=True)
    phone_number=models.CharField(max_length=255, blank=True)
    schedule=models.CharField(max_length=11, blank=True)

class UserType(models.Model):
    CHOICES = ( (1,'admin'),(2,'florist'), (3,'runner'), (4, 'client'), (5, 'superuser'))
    name = models.IntegerField(choices=CHOICES)
'''
class User(AbstractBaseUser):
    username = None
    number = models.CharField(max_length=13, blank=True, unique=True, null=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    is_staff=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    #usertype = models.ForeignKey(UserType, on_delete=models.CASCADE, default=4)
    CHOICES = ( (1,'admin'),(2,'florist'), (3,'runner'), (4, 'client'), (5, 'superuser'))
    usertype = models.IntegerField(choices=CHOICES, default=4)
    photo = models.TextField(default=None, null=True)
    #branch_id=models.ForeignKey(Branch, on_delete=models.DO_NOTHING, default=None, null=True)

    USERNAME_FIELD = 'number'
    REQUIRED_FIELDS = [] 

    objects=UserManager()

class ConfirmCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
    valid_until = models.DateTimeField()

    def __str__(self):
        return self.code