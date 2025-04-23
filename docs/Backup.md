# Backups
Database backups can be multiple hundreds of gigabyte. Tools like `python manage.py dbbackup` create one large backup file. This is not useful in our case. We wrote a custom python script that exports an sql file per log_id for every model that is dependent on the log model. That way each sql output file has manageable size.

## Create Backups
Usually you run the backup on one of the k8s servers. The you first need to enable forwarding to the postgres port inside the postgres pod. Run this on the server (probably inside a screen session).
```bash
kubectl port-forward postgres-postgresql-0 -n postgres 1234:5432
```

To force export all data you can run:
```bash
python utils/backup.py -a -g -f -o <my_output_path>
```
This will overwrite existing sql files in `<my_output_path>` 

Alternatively you can be more selective about which data you want to backup:
```bash
# only export events, games, logs, log status
python utils/backup.py -g -o <my_output_path>
# select the list of representations to backup
# any representation will also backup the table holding all the frame information
python utils/backup.py -g -a -t image_naoimage -o <my_output_path>
# select all data from specifc logs
python utils/backup.py -g -l 1 2 3 282 -o <my_output_path>
```

For downloading the backups you need to zip the folder first for example like this:
```bash
tar --use-compress-program="pigz -k -3" -cf /opt/local-path-provisioner/db_backup.tar.gz -C /opt/local-path-provisioner/ db_backup/
```

These kind of backups will only backup VAT data and no user related data.


## Restore a backup
Make sure you have a database where no data exists that is the same as the data you want to restore. Also the environment variables need to be set:
- VAT_POSTGRES_HOST
- VAT_POSTGRES_PORT
- VAT_POSTGRES_USER
- VAT_POSTGRES_DB

If you set up the project locally you probably have them already set to the values needed for your local environment. Make sure you have the same database schema as the remote. If you are behind just run:
```bash
python manage.py makemigrations
python mange.py migrate
```

To restore data from the backup run
```bash
python restore.py -i <path to folder containing the sql files>
```

If you deleted the whole database before restoring you need to setup user and organisations manually again. See dev setup for more information.

## Backup Automation
Not implemented yet