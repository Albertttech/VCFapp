from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class MemberAccountManager(BaseUserManager):
    def create_user(self, mobile_number, country_code, username, password=None, **extra_fields):
        if not mobile_number:
            raise ValueError('Users must have a mobile number')
        if not country_code:
            raise ValueError('Users must have a country code')
        
        user = self.model(
            mobile_number=mobile_number,
            country_code=country_code,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, country_code, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(mobile_number, country_code, username, password, **extra_fields)

class MemberAccount(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    mobile_number = models.CharField(max_length=20, unique=True)
    country_code = models.CharField(max_length=5)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = MemberAccountManager()
    
    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['username', 'country_code']
    
    class Meta:
        verbose_name = _('Member Account')
        verbose_name_plural = _('Member Accounts')

class MemberProfile(models.Model):
    account = models.OneToOneField(
        MemberAccount, 
        on_delete=models.CASCADE,
        related_name='profile'
    )
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    contact_name = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.account.mobile_number}"