from django.db import models
#from django.contrib.auth.models import User
#from django.db.models.signals import post_save


class Collection(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)


class Molecule(models.Model):
    name = models.CharField(max_length=200)
    smiles = models.CharField(max_length=500)
    inchi_key = models.CharField(max_length=100)
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True)
    image = models.ImageField()


class User(models.Model):
    primary_company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=50)


