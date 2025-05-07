import secrets

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """

    class USER_TYPE_CHOICES(models.TextChoices):
        ADMIN = "admin", "Admin"
        USER = "user", "User"

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES.choices,
        default=USER_TYPE_CHOICES.USER,
    )

    def __str__(self):
        return self.username


class Resume(models.Model):
    """
    Resume model that stores user resumes.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume_file = models.FileField(upload_to="resumes/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Resume"


class UserProfile(models.Model):
    """
    User profile model that extends the custom user model.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    # profile_picture = models.ImageField(
    #     upload_to="profile_pictures/", blank=True, null=True
    # )

    def __str__(self):
        return f"{self.user.username}'s Profile"


class AuthToken(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="auth_token"
    )
    key = models.CharField(max_length=40, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_token():
        return secrets.token_hex(20)

    def __str__(self):
        return f"Token for {self.user.username}"
