from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, PermissionsMixin, BaseUserManager
from django.utils import timezone
from rest_framework.validators import UniqueValidator


class CustomAccountManager(BaseUserManager):

    def create_user(self, email, username, first_name, password, **other_fields):

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(email, username, first_name, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):

    groups = models.ForeignKey(Group, verbose_name='team',
                               null=True, on_delete=models.SET_NULL)
    email = models.CharField(max_length=100, primary_key=True, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, null=True)
    start_date = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    def __str__(self):
        return self.username


class Client(models.Model):
    POTENTIEL = "PO"
    EXISTANT = "EX"
    STATUS = [("PO", "Potentiel"), ("EX", "Existant")]

    company_name = models.fields.CharField(max_length=100)
    first_name = models.fields.CharField(max_length=25)
    last_name = models.fields.CharField(max_length=25)

    email = models.fields.EmailField(max_length=100)
    phone = models.fields.CharField(max_length=25)
    sales_contact = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    date_created = models.fields.DateTimeField(auto_now_add=True)
    date_updated = models.fields.DateTimeField(auto_now=True)

    client_status = models.fields.CharField(choices=STATUS, default="PO")

    def __str__(self):
        return self.company_name


class Contrat(models.Model):

    internal_contrat_number = models.fields.CharField(max_length=20, default='empty')
    status = models.fields.BooleanField(default=False, verbose_name='signé',)
    amount = models.fields.FloatField(default=0.0)
    payment_due = models.fields.DateTimeField(default=0.0)

    client = models.ForeignKey(Client, null=False, on_delete=models.CASCADE, related_name='contrat')

    date_created = models.fields.DateTimeField(auto_now_add=True)
    date_updated = models.fields.DateTimeField(auto_now=True)

    def __str__(self):
        return self.internal_contrat_number


class Event(models.Model):
    ORGANISATION = "OR"
    PRET = "PR"
    TERMINE = "TE"
    STATUS = [("OR", "Organisation"), ("PR", "Prêt"), ("TE", "Terminé")]

    event_name = models.fields.CharField(max_length=100, default="event")
    attendees = models.fields.IntegerField()
    event_date = models.fields.DateTimeField()
    notes = models.fields.CharField(max_length=1000)

    contrat = models.ForeignKey(Contrat, null=False, on_delete=models.CASCADE, related_name='event')
    support_contact = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    event_status = models.fields.CharField(choices=STATUS)
    date_created = models.fields.DateTimeField(auto_now_add=True)
    date_updated = models.fields.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_name
