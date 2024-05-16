from flask import Blueprint, jsonify, request, url_for, redirect, render_template, flash
from database import db
from models import Users
from flask_login import login_user, logout_user, current_user

api_login_bp = Blueprint("api_login", __name__)

@api_login_bp.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("Already logged in.")
        return redirect(url_for("html.home"))

    if request.method == "POST":
        username = request.form.get("username")
        if username == "":
            flash("Please enter a username.")
            return redirect(url_for("html.login"))
        
        user = Users.query.filter_by(username=username).first()
        if user==None:
            flash("No user found.")
            return redirect(url_for("html.register"))
        
        password = request.form.get("password")
        if password == "":
            flash("Please enter a password.")
            return redirect(url_for("html.login"))

        if user.password == password: #check if the password entered is same as the user's password
            login_user(user)
            return redirect(url_for("html.home"))
        else:
            flash("Incorrect password.")
            return redirect(url_for("html.login"))
    return redirect(url_for("html.login"))

