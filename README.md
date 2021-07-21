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
Alternatively, the production data can be inserted via 
```
cd imports
python import_data.py
python generate_user_pokemon.py
```
Since there is a limit on the file size for submission, the image for each Pokemon has to be scraped before the app can be used using
```
cd image_scraping
python image_scraper.py
```
The image scraper is expected to take some time. Some pictures already have been downloaded manually, as the scraper has trouble scraping them.

## Running the app:

In one terminal run `FLASK_APP=app.py flask run`
In another run `cd hello-world && npm run serve`

## Features:

### **Pokedex**

We support the following functionalities: 
- Searching of the Pokemon database based on Pokemon stats and names
- Searching of the Pokemon database based on charactersitics of the moves they know 

The backend is in the `app.py` file and the frontend is in `hello-world/src/components/Pokedex.vue` and `hello-world/src/components/Profile.vue`.

### **Pokemon Details**
We support the following functionalities:
- Clicking on images on the Pokedex and Team pages to see the Pokemon's details
- Details include:
    - Pokemon stats
    - All possible moves the Pokemon can learn
    - Which Pokemon it can evolve into (including links to their pages)

The backend is in the `app.py` file and the frontend is in `hello-world/src/components/Pokemon.vue` and `hello-world/src/components/Profile.vue`.

### **Users**

We support the following functionalities:
- Signing up of new users
- Logging in and logging out of existing accounts
- Changing an accounts password
- Deleting an account

Existing accounts you can use for testing:

|  Username  |  Password  |
|:----------:|:----------:|
|   user1    |   pass1    |
|   user2    |   pass2    |
|   user3    |   pass3    |

The backend is in `app.py`. The frontend is in the following files in the `hello-world/src/components` folder: `Login.vue`, `Signup.vue`, `ChangePassword.vue` and `Delete.vue`.

### **Program-Generated Teams**

We support the following functionalities:
- We will generate up to 5 program-generated teams of 6 Pokemon, selecting each Pokemon greedily based on highest sum of percentages that each pair of Pokemon are matched up, while restricting that Pokemon must have different types
- We also allow users to filter on teams containing a specific Pokemon
- Only images of Pokemon are shown, but if you hover over the Pokemon image, the name appears in a popup

The backend is in `app.py` (`POST /program_generated_teams`). The frontend is in `TeamGeneration.vue` of the `hello-world/src/components` folder.

### **User-Generated Teams**

We support the following functionalities:
- We will return up to 5 user-generated teams of 6 Pokemon with top win rate and at least 2 games played
- We also allow users to filter on teams containing a specific Pokemon
- Only images of Pokemon are shown, but if you hover over the Pokemon image, the name appears in a popup

The backend is in `app.py` (`POST /user_generated_teams`). The frontend is in `TeamGeneration.vue` of the `hello-world/src/components` folder.

## References:

Sort of followed this tutorial: https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/
and this one: https://www.askpython.com/python-modules/flask/flask-postgresql
The storage of user data followed this tutorial: https://dev.to/nickitax/persistent-store-with-vuejs-vuex-and-vuex-persisted-state-354n
