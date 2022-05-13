import csv
from dataclasses import dataclass
from os.path import exists

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from molecule_admin.models import Collection, Molecule


@dataclass
class MoleculeData:
    name: str
    smiles: str
    inchi_key: str
    set: str


class Command(BaseCommand):
    help = "Loads molecule data into DB."

    def add_arguments(self, parser):
        parser.add_argument('file_path', action='store', type=str)

    def handle(self, *args, **options):

        csv_file = options['file_path']
        if not exists(csv_file):
            raise CommandError(f"File: {csv_file} does not exist.")

        with open(csv_file) as f:
            data = csv.reader(f, delimiter=',')
            next(data, None)  # Skip header

            for line in data:
                if len(line) != 4:
                    self.stderr.write(f"Malformed data for {line}")
                    continue
                try:
                    new_molecule = MoleculeData(
                        name=line[0],
                        smiles=line[1],
                        inchi_key=line[2],
                        set=line[3]
                    )
                except IndexError:
                    self.stderr.write(f"Malformed data for {line}")
                else:
                    collection = self._ensure_collection(new_molecule)
                    molecule = self._ensure_molecule(new_molecule)
                    molecule.collection.add(collection)

    def _ensure_collection(self, new_molecule):
        try:
            collection = Collection.objects.create(
                name=new_molecule.set)
            self.stdout.write(self.style.SUCCESS(
                f"Collection {new_molecule.set} was added to DB."))
        except IntegrityError:
            collection = Collection.objects.get(
                name=new_molecule.set)
            self.stdout.write(
                f"Collection {new_molecule.set} "
                f"already exists, skipping.")
        return collection

    def _ensure_molecule(self, new_molecule):
        try:
            molecule = Molecule.objects.create(
                name=new_molecule.name,
                smiles=new_molecule.smiles,
                inchi_key=new_molecule.inchi_key)
            self.stdout.write(self.style.SUCCESS(
                f"Molecule {new_molecule.name} was added to DB."))
        except IntegrityError:
            molecule = Molecule.objects.get(
                name=new_molecule.name,
                inchi_key=new_molecule.inchi_key)
            self.stdout.write(
                f"Molecule {new_molecule.name} "
                f"already exists, skipping.")
        return molecule
