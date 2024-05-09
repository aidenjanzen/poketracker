from flask import Blueprint, jsonify, request, url_for, redirect, render_template
from database import db
from models import Users
from flask_login import login_user, logout_user

api_login_bp = Blueprint("api_login", __name__)

@api_login_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by( #filtering for username
            username=request.form.get("username")).first()
        
        if user.password == request.form.get("password"): #check if the password entered is same as the user's password
            login_user(user)
            return redirect(url_for("html.home"))
    return render_template("login.html")