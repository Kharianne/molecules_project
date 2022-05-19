from django.db import models

class Collection(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

class Molecule(models.Model):
    name = models.CharField(max_length=200)
    smiles = models.CharField(max_length=500)
    inchi_key = models.CharField(max_length=100)
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True)
    image = models.ImageField()
