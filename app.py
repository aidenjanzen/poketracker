from flask import Flask, render_template, jsonify, request, redirect, url_for
import csv
from pathlib import Path
from database import db
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.py"  # database url

app.instance_path = Path("./data").resolve()  # current path
db.init_app(app)


from routes import web_pages_bp, api_teams_bp

app.register_blueprint(web_pages_bp, url_prefix="/")

app.register_blueprint(api_teams_bp, url_prefix="/")

if __name__ == "__main__":  # keep at the bottom
    app.run(debug=True, port=8888)
