# models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    STATUS_APPROVED = 'approved'
    STATUS_PENDING = 'pending'
    STATUS_REJECTED = 'rejected'

    username = models.CharField(max_length=100, unique=False)  # 일반 username 필드
    oid = models.CharField(max_length=100, unique=True)  # 카카오 user_id
    # 추가 필드들
    position = models.CharField(max_length=100, blank=True)
    directNumber = models.IntegerField(null=True, blank=True)
    profileImage = models.URLField(max_length=200, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            (STATUS_APPROVED, 'Approved'),
            (STATUS_PENDING, 'Pending'),
            (STATUS_REJECTED, 'Rejected')
        ],
        default=STATUS_PENDING
    )

    is_staff = models.BooleanField(default=False)  # 관리자 사이트 액세스 권한
    is_superuser = models.BooleanField(default=False)  # 슈퍼유저 권한
    is_active = models.BooleanField(default=True)  # 계정 활성화 상태
    # is_superuser, is_staff 모두 True => 승인 / is_superuser=False, is_staff=True => 보류 / 둘다 False => 반려

    USERNAME_FIELD = 'oid'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.is_superuser and self.is_staff:
            self.status = self.STATUS_APPROVED
        elif self.is_staff and not self .is_superuser:
            self.status = self.STATUS_PENDING
        else:
            self.status = self.STATUS_REJECTED

        super().save(*args, **kwargs)


    def __str__(self):
        return self.username
