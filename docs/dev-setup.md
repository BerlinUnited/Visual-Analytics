# Local Developer Setup
Our django application expects a postgres to be available


Setup python requirements
```bash
cd django
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

Import backup
```bash
python restore.py -i <folder of sql files>
```

Setup User
```bash
python manage.py createsuperuser
```






