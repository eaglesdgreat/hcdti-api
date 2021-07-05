from datetime import date
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser, UserManager, BaseUserManager
from django.http import request
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.sessions.models import Session



class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True)
    staffname = models.TextField("staffname", null=True, blank=True)
    staffid = models.TextField(null=True, blank=True)
    is_credit_officer = models.BooleanField(default=False)
    is_branch_manager = models.BooleanField(default=False)
    is_senior_manager = models.BooleanField(default=False)
    is_agency_bank = models.BooleanField(default=False)
    is_staff = models.BooleanField(verbose_name='is_staff', default=True)
    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    is_active = models.BooleanField(verbose_name='is_active', default=True)
    objects =  UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['staffname']

    class Meta:
        db_table = 'user'


class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_session'
        

class Otp(models.Model):
    email = models.EmailField(null=True)
    otp_code = models.TextField(null=True)
    dt_created = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'otp'
        
class Groups(models.Model):
    group_id = models.CharField(max_length=100, null=True)
    group_name = models.TextField(null=True)
    active = models.BooleanField(default=False)
    date_created = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'groups'
        

class GroupMember(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    groups_id = models.TextField(null=True)
    member_name = models.TextField(null=True)
    mobile_number = models.TextField(null=True)
    is_leader = models.BooleanField(null=True)
    date_added = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'group_member'