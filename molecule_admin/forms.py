from django import forms
from django.core.exceptions import ValidationError

from molecule_admin.models import Note, Molecule


class CreateNoteForm(forms.ModelForm):
    molecule = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Note
        fields = ['note_text', 'molecule']

    def clean_molecule(self):
        molecule = self.cleaned_data['molecule']
        if molecule:
            try:
                molecule = Molecule.objects.get(pk=molecule)
                return molecule
            except:
                raise ValidationError("Not existing molecule ID.")
        else:
            raise ValidationError("No molecule provided!")
