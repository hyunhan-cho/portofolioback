from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):
    """커스텀 유저 매니저"""
    
    def create_user(self, email, password=None, **extra_fields):
        """일반 유저 생성"""
        if not email:
            raise ValueError('이메일은 필수입니다.')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """관리자 유저 생성"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('관리자는 is_staff=True여야 합니다.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('관리자는 is_superuser=True여야 합니다.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """커스텀 유저 모델 - 이메일을 사용자명으로 사용"""
    
    email = models.EmailField(
        verbose_name='이메일',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = '유저'
        verbose_name_plural = '유저들'
    
    def __str__(self):
        return self.email


class MemberProfile(models.Model):
    """회원 추가 정보 모델 - 확장 필드 보관"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=50, blank=True)
    full_name = models.CharField(max_length=100, blank=True)
    tier = models.CharField(max_length=20, default='basic')  # 예: basic, premium 등
    is_premium = models.BooleanField(default=False)
    last_active = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '회원 프로필'
        verbose_name_plural = '회원 프로필들'

    def __str__(self):
        return f"Profile({self.user.email})"
