from flask import Blueprint, jsonify, request, url_for, redirect, render_template
from database import db
from models import Users
from flask_login import login_user, logout_user

api_login_bp = Blueprint("api_login", __name__)

@api_login_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        if username == "":
            return render_template("login.html", error="Please enter a username.")
        
        user = Users.query.filter_by(username=username).first()
        if user==None:
            return render_template("register.html", error="No user found, please register.")
        
        password = request.form.get("password")
        if password == "":
            return render_template("login.html", error="Please Enter a password.")

        if user.password == password: #check if the password entered is same as the user's password
            login_user(user)
            return redirect(url_for("html.home"))
        else:
            return render_template("login.html", error="Incorrect Password")
    return render_template("login.html")