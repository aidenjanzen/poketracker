from flask import Blueprint, jsonify, request, url_for, redirect, render_template
from database import db
from models import Users
from flask_login import login_user
api_register_bp = Blueprint("api_register", __name__)

@api_register_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = Users(username=request.form.get("username"), password=request.form.get("password"))

        db.session.add(user)
        db.session.commit()

        return render_template("login.html")
    return render_template("register.html")