# Pes league

## For development

### Create virtual environment
```
python -m venv .env
```

### Activate virtual environment
```
.env\Scripts\activate
```

### Install dependencies
```
cd pes_league
pip install -r requirements.txt
```

### Migrate database
```
python manage.py migrate
```

### Run development server
```
python manage.py runserver
```
