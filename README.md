# METSENAT

    []: # Language: markdown
    []: # Path: README.md
    # METSENAT

## Installation

pip install -r requirements.txt

## Env variables

Change below variables to connect database (PostgreSQL)

```python
# Database name
DB_NAME = metsenat
# Database User
DB_USER = postgres
# Database Password
DB_PASSWORD = 1
# Database host
DB_HOST = localhost
# Database port
DB_PORT = 5432
# Debug option(For Development process put True, for production level put False)
DEBUG = True

```

## To create table in database run below commands

``` 
python manage.py makemigrations
```

``` 
python manage.py migrate
```     

## To create superuser in Django run below commands

```
python manage.py createsuperuser
```

## For questions and feedbacks:

phone: +99893 120 98 06

telegram: [@sh1209806](http://t.me/sh1209806)
