## Molecules project

#### Load molecules into database
Loading molecules into the database is managed by import_data Django command.  

This command accept path to csv file and then goes through molecules present
in the file and check if the collection and molecule is already present,
otherwise it adds them to the database.
```commandline
python manage.py import_data <path_to_csv_file>
```
