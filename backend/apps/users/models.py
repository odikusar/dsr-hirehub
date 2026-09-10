from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


# Custom manager is required because the stock UserManager expects a username,
# which we removed. create_user/create_superuser is the contract used by
# createsuperuser and any code that creates users.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra):
        if not email:
            raise ValueError("Email is required")
        # normalize_email lowercases the domain part (Oleg@GMAIL.COM -> Oleg@gmail.com).
        user = self.model(email=self.normalize_email(email), **extra)
        # Hashes the password — never assign user.password directly.
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra)


# Custom user: email login instead of username, plus a role field.
# Inherits password handling, permissions, is_active/is_staff etc. from AbstractUser.
class User(AbstractUser):
    class Role(models.TextChoices):
        # NAME = "db value", "human-readable label"
        CANDIDATE = "CANDIDATE", "Candidate"
        HR = "HR", "HR"

    # Assigning None removes the inherited field — no username column at all.
    username = None
    # AbstractUser's email is not unique — override it.
    email = models.EmailField(unique=True)
    # default=HR: createsuperuser only asks email/password, and Phase 1 has HR users only.
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.HR)
    created_at = models.DateTimeField(auto_now_add=True)  # set once on INSERT
    updated_at = models.DateTimeField(auto_now=True)  # updated on every save()

    objects = UserManager()

    # Field used as the login identifier (admin login, authenticate(), createsuperuser).
    USERNAME_FIELD = "email"
    # Extra fields createsuperuser prompts for (email/password are always asked).
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
