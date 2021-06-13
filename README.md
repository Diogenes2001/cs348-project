# cs348-project

Requirements: node, pip

Installation:
```
pip install -r requirements.txt
cd hello-world
npm install
```

To set up the database:

Install PostgreSQL and create a server with user `postgres` and password `password`. Alternatively, modify add.py with your username and password. Add a database called Flask.

To set up the database, run
```
schema.sql
```
Then, data can be inserted using
```
dummy-data.sql
```

Running the app:

In one terminal run `FLASK_APP=app.py flask run`
In another run `cd hello-world && npm run serve`

Sort of followed this tutorial: https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/
and this one: https://www.askpython.com/python-modules/flask/flask-postgresql