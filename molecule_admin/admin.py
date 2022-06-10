from django.contrib import admin
from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple

from molecule_admin.models import Molecule, Collection, Profile


class MoleculeAdmin(admin.ModelAdmin):
    fields = ["name", "smiles", "inchi_key", "collection", "image"]
    list_display = ["name", "inchi_key", "collections"]
    list_filter = ["collection"]
    search_fields = ["name", "collection__name"]

    # Changes multiple select to CheckboxSelectMultiple
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    # Disables adding new collection via MoleculeAdmin
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['collection'].widget.can_change_related = False
        form.base_fields['collection'].widget.can_add_related = False
        return form


class CollectionAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]

class UserAdmin(admin.ModelAdmin):
    #fields = ["user", "institution", "name", "surname"]
    list_display = ["user", "name", "surname", "institution"]
    list_filter = ["institution"]
    search_fields = ["user", "name", "surname"]


admin.site.register(Molecule, MoleculeAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Profile, UserAdmin)
