from flask import Blueprint, jsonify, request, url_for, redirect, render_template
from database import db
from models import Users
from flask_login import login_user
api_register_bp = Blueprint("api_register", __name__)

@api_register_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        if username == "":
            return render_template("register.html", error="Please enter a username")
        
        password = request.form.get("password")
        if password == "":
            return render_template("register.html", error="Please enter a password")

        check = db.select(Users).where(Users.username == username)
        result = db.session.execute(check).scalar()
        if result:
            return render_template("login.html", error="User already exists, please login.")
        
        user = Users(username=username, password=password)
        
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("html.login", error=None))
    return render_template("register.html")