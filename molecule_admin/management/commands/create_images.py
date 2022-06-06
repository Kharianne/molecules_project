from os.path import exists

from django.core.exceptions import SuspiciousFileOperation
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import get_valid_filename
from rdkit import Chem
from rdkit.Chem import Draw

from molecule_admin.models import Molecule


class Command(BaseCommand):
    help = "Create images for molecules."

    def add_arguments(self, parser):
        parser.add_argument('file_path', action='store', type=str)

    def handle(self, *args, **options):
        output_dir = options['file_path']
        if not exists(output_dir):
            raise CommandError(f"File: {output_dir} does not exist.")

        molecules = Molecule.objects.all()
        for molecule in molecules:
            m = Chem.MolFromSmiles(molecule.smiles)
            try:
                file_name = f"{get_valid_filename(molecule.name)}.png"
            except SuspiciousFileOperation:
                file_name = f"{molecule.id}.png"
            try:
                Draw.MolToFile(m, f'{output_dir}/'
                                  f'{file_name}')
                molecule.image = file_name
                molecule.save()
                self.stdout.write(f"Created image for {molecule.name}")
            except (FileNotFoundError, ValueError):
                self.stderr.write(f"Couldn't create image for {molecule.name}")
