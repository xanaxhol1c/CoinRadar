from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy 

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError(gettext_lazy('The email field is required'))
        
        if not username:
            raise ValueError(gettext_lazy('The username field is required'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(gettext_lazy('is_staff has to be true for superuser'))
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(gettext_lazy('is_superuser has to be true for superuser'))
        
        return self.create_user(email, username, password, **extra_fields)