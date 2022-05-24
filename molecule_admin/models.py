from django.db import models
#from django.contrib.auth.models import User
#from django.db.models.signals import post_save
from django.db.models.constraints import UniqueConstraint


class Collection(models.Model, primary_key=True):
    name = models.CharField(max_length=200, blank=True, null=True, primary_key=True, unique=True)


class Molecule(models.Model):
    name = models.CharField(max_length=200, primary_key=True, unique=True)
    smiles = models.CharField(max_length=500)
    inchi_key = models.CharField(max_length=100)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, null=True, unique=True)
    image = models.ImageField()

    class Meta:
        UniqueConstraint(fields=['Collection', 'Molecule'], name='unique_collection')

class User(models.Model):
    COMPANY_CHOICES = (
        ('a', 'GREEN'),
        ('b', 'BLUE'),
        ('c', 'RED'),
        ('d', 'ORANGE'),
        ('e', 'BLACK'),
    )

    company = models.CharField(max_length=6, choices=COMPANY_CHOICES, default='a', on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
