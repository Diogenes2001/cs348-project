# PokeDB

Requirements: node, pip

## Installation:
```
pip install -r requirements.txt
cd hello-world
npm install
```

## To set up the database:

Install PostgreSQL and create a server with user `postgres` and password `password`. Add a database called Flask.

To set up the database schema, run
```
schema.sql
```
Then, sample data can be inserted using
```
dummy-data.sql
```
Alternatively, the production data can be inserted using 
```
cd imports
python import_data.py
python generate_user_pokemon.py
```

## Running the app:

In one terminal run `FLASK_APP=app.py flask run`
In another run `cd hello-world && npm run serve`

## Features:

### **Pokedex**

We support the following functionalities: 
- Searching of the Pokemon database based on Pokemon stats and names
- Searching of the Pokemon database based on charactersitics of the moves they know 

The backend is in the `app.py` file and the frontend is in `hello-world/src/components/Pokedex.vue` and `hello-world/src/components/Profile.vue`.

### **Users**

We support the following functionalities:
- Signing up of new users
- Logging in and logging out of existing accounts
- Changing an accounts password
- Deleting an account

The backend is in `app.py`. The frontend is in the following files in the `hello-world/src/components` folder: `Login.vue`, `Signup.vue`, `ChangePassword.vue` and `Delete.vue`.

## References:

Sort of followed this tutorial: https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/
and this one: https://www.askpython.com/python-modules/flask/flask-postgresql
The storage of user data followed this tutorial: https://dev.to/nickitax/persistent-store-with-vuejs-vuex-and-vuex-persisted-state-354n