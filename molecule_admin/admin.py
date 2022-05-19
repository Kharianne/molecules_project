from django.contrib import admin
import molecule_admin.models as models
# Create your models here.
class MoleculeAdmin(admin.ModelAdmin):
    fields = ["name", "smiles", "inchi_key", "collection", "image"]
    readonly_fields = ["inchi_key"]
    list_display = ["name", "smiles", "inchi_key", "collection", "image"]
    list_filter = ["name", "smiles", "inchi_key", "collection"]
    search_fields = ["name", "collection"]

class CollectionAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]



admin.site.register(models.Molecule, MoleculeAdmin)
admin.site.register(models.Collection, CollectionAdmin)

