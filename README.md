# Bollards API

## Environment variables for development

Make sure the following env variables are set:
- FLASK_APP
- FLASK_DEBUG (optional, do not use in production)


## Flask Migrate setup:

The project db migration has been initiated with:
```bash
flask db init
```
To create the first migration file, make sure you have deleted any existing sqlite db on the project and use:
```bash
DATABASE_URL=sqlite:/// flask db migrate
```
```bash
flask db stamp head
```
```bash
flask db upgrade
```

Notes:
- Make sure the database is empty when upgrading for the first time. (import db and db.drop_all())
- If any change is made to sqlalchemy models, use flask db migrate, then flask db upgrade
