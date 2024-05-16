from flask import Blueprint, jsonify, request, url_for, redirect, render_template, flash
from database import db
from models import Users
from flask_login import login_user
api_register_bp = Blueprint("api_register", __name__)

@api_register_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        if username == "":
            flash("Please enter a username.")
            return redirect(url_for("html.register"))
        
        password = request.form.get("password")
        if password == "":
            flash("Please enter a password.")
            return redirect(url_for("html.register"))

        check = db.select(Users).where(Users.username == username)
        result = db.session.execute(check).scalar()
        if result:
            flash("User already exists, please login.")
            return redirect(url_for("html.login"))
        
        user = Users(username=username, password=password)
        
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("html.login"))
    return render_template("register.html")