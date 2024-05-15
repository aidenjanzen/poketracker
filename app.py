from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_login import LoginManager
from flask_login import UserMixin
from pathlib import Path
from database import db
from models import Users
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.py"  # database url
app.config["SECRET_KEY"] = "AGILE_KEY"

app.instance_path = Path("./data").resolve()  # current path
db.init_app(app)

login_manager = LoginManager() #creates the login manager
login_manager.init_app(app) #initializes the login manager

@login_manager.user_loader #retrieves a given user from userid
def loader_user(user_id):
    return Users.query.get(user_id)

from routes import web_pages_bp, api_collections_bp, api_login_bp, api_register_bp

app.register_blueprint(web_pages_bp, url_prefix="/")
app.register_blueprint(api_collections_bp, url_prefix="/")

app.register_blueprint(api_login_bp, url_prefix="/")
app.register_blueprint(api_register_bp, url_prefix="/")

if __name__ == "__main__":  # keep at the bottom
    app.run(debug=True, port=8888)
