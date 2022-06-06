## Molecules project

#### Load molecules into database
Loading molecules into the database is managed by import_data Django command.  

This command accepts  a path to csv file and then goes through molecules present
in the file and check if the collection and molecule is already present,
otherwise it adds them to the database.
```commandline
python manage.py import_data <path_to_csv_file>
```
#### Images and create images
In order to have images of molecules create inside of project new directory named **images**. 
```
  .  
    ├── images                      # Newly created directory images  
    ├── molecule_admin                
    ├── molecule_project                    
    └── README.md  
    etc...
```

This command accepts a path to images directory, then command reads all molecules in database and 
generates an image from smile key of the molecule using rdkit package.
```commandline
python manage.py create_images <path_to_media_directory>
```
