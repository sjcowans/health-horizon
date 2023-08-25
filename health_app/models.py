from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from datetime import date

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class UserProfile(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    height = models.PositiveIntegerField(help_text="Height in centimeters")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # This is needed for the admin site
    is_superuser = models.BooleanField(default=False)  # Needed for Django's built-in permissions

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['age', 'sex', 'height']

    def __str__(self):
        return self.username

class DateInfo(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='date_infos')
    sleep = models.PositiveIntegerField(help_text="Sleep in minutes")
    calories = models.PositiveIntegerField(help_text="Calories consumed")
    stress = models.PositiveIntegerField(help_text="Stress level from 0 to 100")
    steps = models.PositiveIntegerField()
    weight = models.PositiveIntegerField(help_text="Weight in kilograms")
    wellness_score = models.PositiveIntegerField(help_text="Wellness score from 0 to 100")
    date = models.DateField(default=date.today)

    class Meta:
        unique_together = ['user', 'date']

    def __str__(self):
        return f"Metrics for {self.user.username} on {self.date}"