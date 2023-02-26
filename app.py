from os import environ
from ast import Assign
from multiprocessing.util import ForkAwareThreadLock
from unittest.mock import NonCallableMagicMock
from db import db, User
from flask import Flask, request
import json
import datetime


app = Flask(__name__)
db_filename = "tattoo.db"
 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config['SECRET_KEY'] = 'mysecret'

db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(data, code=200):
    """
    Returns a generic success response
    """
    return json.dumps(data), code

 
def failure_response(message, code=404):
    """
    Returns a generic failure response
    """
    return json.dumps({"error": message}), code

@app.route("/")
def hello_world():
    """
    Endpoint for printing Hello World!
    """
    return "Hello World!"

@app.route("/api/user/")
def get_users():
    """
    Endpoint for the getting all users
    """
    user = [user.serialize() for user in User.query.all()]
    return success_response({"user": user})

@app.route("/api/user/", methods=["POST"])
def create_user():
    """
    Endpoint for creating a new user
    """
    body = json.loads(request.data)
    first = body.get("first")
    last = body.get("last")
    email = body.get("email")

    if email is None or first is None or last is None:
        return failure_response("Missing first name, last name, email, password, or phone number", 400)

    user = User(first = first, last = last, email = email)
    db.session.add(user)
    db.session.commit()
    return user.serialize()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
    