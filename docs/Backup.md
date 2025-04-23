# Backups
Database backups can be multiple hundreds of gigabyte. Tools like `python manage.py dbbackup` create one large backup file. This is not useful in our case. We wrote a custom python script that exports an sql file per log_id for every model that is dependent on the log model. That way each sql output file has manageable size.

## Create Backups Manually
Usually you run the backup on one of the k8s servers. The you first need to enable forwarding to the postgres port inside the postgres pod. Run this on the server (probably inside a screen session). For this to work you need to be added to the kubernetes admins.
```bash
kubectl port-forward postgres-postgresql-0 -n postgres 1234:5432
```

To get access to the live postgres you need to have the postgres password set as environment variable `PGPASSWORD`.

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
Restoring a backup can only work for a database that has no data in the tables you want to restore. Usually the backup restoring is done locally to have some data for development purposes so you can just reset your database:

```bash
./utils/dbubtils.sh renew
```

This will completely wipe the database. The script uses the same database credentials the django settings use. Namely those environment variables:
- VAT_POSTGRES_HOST
- VAT_POSTGRES_PORT
- VAT_POSTGRES_USER
- VAT_POSTGRES_DB

You need to be on the same state the remote server is. The important part is that you have all the migration files that are in the commit that runs in production.

To restore data from the backup run
```bash
python restore.py -i <path to folder containing the sql files>
```

If you deleted the whole database before restoring you need to setup user and organisations manually again. See dev setup for more information.

## Backup Automation
Not implemented yet