# Pes league

## For development

### Create virtual environment
```
python -m venv .venv
```

### Activate virtual environment
```
.venv\Scripts\activate
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

### Debug for VSCode
- Turn off development server (`Ctrl+C`)
- Press `F5`

### Environment variables
Default variables should work already, but if you need to customize:
- Add file `pes_league/.env`
- Available variables can be seen in `pes_league/pes_league/settings.py` file:
```
env = environ.Env(
    # Available variables are listed here
)
```
