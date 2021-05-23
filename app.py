import json
from flask import Flask, request, json, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, InfoModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost:5432/Flask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/test")
def test():
    new_user = InfoModel(name='Cinna', age='1')
    db.session.add(new_user)
    db.session.commit()
    return jsonify("Success!")

if __name__ == "main":
    app.run()