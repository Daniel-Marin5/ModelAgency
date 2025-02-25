from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The group this user belongs to',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user',
        verbose_name='user permissions',
    )
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=[('client', 'Client'), ('model', 'Model'), ('applicant', 'Applicant'), ('agent', 'Agent')])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    def __str__(self):
        return self.name

class Client(User):
    pass

class Model(User):
    measurements = models.JSONField(default=dict)
    portfolio = models.JSONField(default=list)
    payrate = models.FloatField(default=0.0)
    paysplitpercent = models.FloatField(default=0.0)
    age = models.IntegerField()

class Applicant(User):
    measurements = models.JSONField(default=dict)
    portfolio = models.JSONField(default=list)
    age = models.IntegerField()

class Agent(User):
    paysplitpercent = models.FloatField(default=0.0)
    approved = models.BooleanField(default=False)