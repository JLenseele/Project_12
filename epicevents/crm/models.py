from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, PermissionsMixin, BaseUserManager
from django.utils import timezone


class CustomAccountManager(BaseUserManager):

    def create_user(self, email, username, first_name, password, **other_fields):

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


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

    object = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Client(models.Model):
    POTENTIEL = "PO"
    EXISTANT = "EX"
    STATUS = [("PO", "Potentiel"), ("EX", "Existant")]

    first_name = models.fields.CharField(max_length=25)
    last_name = models.fields.CharField(max_length=25)
    email = models.fields.EmailField(max_length=100)
    phone = models.fields.CharField(max_length=25)
    company_name = models.fields.CharField(max_length=100)
    date_created = models.fields.DateTimeField(auto_now_add=True)
    date_updated = models.fields.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    client_status = models.fields.CharField(choices=STATUS)


class Contrat(models.Model):
    date_created = models.fields.DateTimeField(auto_now_add=True)
    date_updated = models.fields.DateTimeField(auto_now=True)
    status = models.fields.BooleanField
    amount = models.fields.FloatField
    payment_due = models.fields.DateTimeField
    client = models.ForeignKey(Client, null=False, on_delete=models.CASCADE)


class Event(models.Model):
    ORGANISATION = "OR"
    PRET = "PR"
    TERMINE = "TE"
    STATUS = [("OR", "Organisation"), ("PR", "Prêt"), ("TE", "Terminé")]

    date_created = models.fields.DateTimeField(auto_now_add=True)
    date_updated = models.fields.DateTimeField(auto_now=True)
    attendees = models.fields.IntegerField
    event_date = models.fields.DateTimeField
    notes = models.fields.CharField(max_length=1000)
    contrat = models.ForeignKey(Contrat, null=False, on_delete=models.CASCADE)
    support_contact = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    event_status = models.fields.CharField(choices=STATUS)