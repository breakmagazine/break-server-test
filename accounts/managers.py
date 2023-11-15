# managers.py
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, oid, **extra_fields):
        if not oid:
            raise ValueError(_('카카오 로그인을 통해서 로그인 해주세요.'))
        user = self.model(oid=oid, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, oid, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(oid, **extra_fields)
