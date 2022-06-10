from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Collection(models.Model):
    name = models.CharField(max_length=200,
                            primary_key=True,
                            unique=True)
    def __str__(self):
        return(self.name)

class Molecule(models.Model):
    name = models.CharField(max_length=200)
    smiles = models.CharField(max_length=500)
    inchi_key = models.CharField(max_length=500, unique=True)
    collection = models.ManyToManyField(Collection)
    image = models.ImageField(blank=True, null=True)

    # Inchi_key is nearly unique, so we need to be sure that we don't have
    # duplicates
    class Meta:
        #verbose_name_plural = molecules
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'inchi_key'], name='unique-molecule-constraint'
            )
        ]


    @property
    def collections(self):
        return ', '.join([c.name for c in self.collection.all()])

    def __str__(self):
        return(self.name)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=75)
    institution = models.CharField(max_length=100, null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

"""
TODO: Create a model named Profile with following fields:
- user = models.OneToOneField(User, on_delete=models.CASCADE) --> User model
has to be imported from django.contrib.auth.models
- institution
- name
- surname

Create a post_save signal to create Profile for User after registration
"""