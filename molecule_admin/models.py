from django.contrib.auth.models import User
from django.db import models


class Collection(models.Model):
    name = models.CharField(max_length=200,
                            primary_key=True,
                            unique=True)


class Molecule(models.Model):
    name = models.CharField(max_length=200)
    smiles = models.CharField(max_length=500)
    inchi_key = models.CharField(max_length=500)
    collection = models.ManyToManyField(Collection)
    image = models.ImageField(blank=True, null=True)

    # Inchi_key is nearly unique, so we need to be sure that we don't have
    # duplicates
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'inchi_key'], name='unique-molecule-constraint'
            )
        ]

    @property
    def collections(self):
        return ', '.join([c.name for c in self.collection.all()])


class Note(models.Model):
    note_text = models.TextField()
    molecule = models.ForeignKey(Molecule, on_delete=models.PROTECT)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


"""
TODO: Create a model named Profile with following fields:
- user = models.OneToOneField(User, on_delete=models.CASCADE) --> User model
has to be imported from django.contrib.auth.models
- institution
- name
- surname

Create a post_save signal to create Profile for User after registration
"""