# Bollards API

## Environment variables for development

Make sure the minumum environment variables are set, in production, use provided example env files to create your own .env files.
- api.env.example (api environment variables)
- db.env.example (db environment variables)

## Deployment with Docker and Docker-compose
This project can be deployied using docker-compose. An example docker-compose.yml file is provided in this repository.
Note that you may need to create necessary folder structure on the target server before deploying. Make sure you also have 

## Flask Migrate create initial database
Once your postgres and python docker are running, exec into the python docker (which has flask migrate installed) and run the following command:
```bash
flask db upgrade
```
Hopefully it works first time, if not, you may want to recreate a new migration file using flask migrate documentation and the section below.


## Flask Migrate setup:

The project db migration has been initiated with:
```bash
flask db init
```
(To create the first migration file, make sure you have deleted any existing sqlite db on the project and use):
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
- If everything starts to mess up, just delete the migrations folder, delete the line with revision number in alambic table (DO NOT remove the table itself)


## Tests
To run unit test suite, install pytest (it should allready be installed if requirements are installed):
```bash
pip install pytest
```
To run the tests, make sure you are in the virtual environment and use:
```bash
pytest
```
Installed packages included with pytest:
pyparsing, toml, py, pluggy, packaging, iniconfig, attrs, pytest.

## Test Coverage
To run tests with an html cover report, use: 
```bash
pytest --cov=bollards_api --cov-report=html
```
This will create an htmlcov directory that can be browsed on any browser.
