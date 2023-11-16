from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


PASSWORD_MIN_LENGTH = 8


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("이메일 주소가 필요합니다.")

        user = self.model(
            email=self.normalize_email(email),
        )

        if password is None:
            raise ValueError("비밀번호가 필요합니다.")

        if len(password) < PASSWORD_MIN_LENGTH:
            raise ValueError("비밀번호는 8자리 이상입니다.")

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
