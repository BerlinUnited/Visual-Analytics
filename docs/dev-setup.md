# Local Developer Setup


## Setup direnv
In order to setup everything correctly you need to set up a bunch of environment variables. We recommend to use [direnv](https://direnv.net/). However this is optional.

```bash
sudo apt install direnv
```

Add this to the .bashrc file
```bash
eval "$(direnv hook bash)"
```
you need to run `direnv allow` in every folder you have an .envrc file after every change before you can use the variables defined there.

## Setup Postgres
Our django application expects a postgres to be available. We are currently running Postgres 16.2 in production. You need to have the same version to not get problems when ingesting a prod backup.
For Ubuntu 24.04 you can just install postgres via apt to get the same version as the production server.

Run `utils/dbutils.sh create` to create the postgres database that django expects.

The script and later django expect the variables to be set
```bash
export VAT_POSTGRES_DB=
export VAT_POSTGRES_USER=
export VAT_POSTGRES_PASS=
export VAT_POSTGRES_HOST=localhost
export VAT_POSTGRES_PORT=5432
```

## Setup Django

Setup python requirements
```bash
cd django
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

If you set up direnv you can add this to your.envrc in the django folder to automatically load the venv when entering the folder.
```
source venv/bin/activate
unset PS1
```

TODO explain all the other env vars needed here

Import backup
```bash
python restore.py -i <folder of sql files>
```

Setup User
```bash
python manage.py createsuperuser
```

## Setup Frontend
https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-22-04

```
curl -sL https://deb.nodesource.com/setup_22.x -o nodesource_setup.sh
sudo bash nodesource_setup.sh
```




