from database import db
from flask import Blueprint
from flask import Flask, render_template, jsonify, request, redirect, url_for
from models import Users
from flask_login import logout_user
import requests

from pokedex import pokedex

import os
web_pages_bp = Blueprint("html", __name__)

@web_pages_bp.route("/")
def base():
    return render_template("home.html")

@web_pages_bp.route("/home")
def home():
    return render_template("home.html")

@web_pages_bp.route("/search")
def search():
    return render_template("search.html")

@web_pages_bp.route("/gen<int:number>")
def gen(number):
    amounts = [151, 100, 135, 107, 156, 72, 88, 96, 120]
    startNumber = [1, 152, 252, 387, 494, 650, 722, 810, 906]
    return render_template("generations.html", number=number, pokedex=pokedex, amounts=amounts, startNumber=startNumber)


@web_pages_bp.route("/register")
def register():
    return render_template("register.html")

@web_pages_bp.route("/login")
def login():
    return render_template("login.html")

@web_pages_bp.route("/logout")
def logout():
    logout_user()
    return render_template("home.html")



@web_pages_bp.route("/teams")
def teams():
    return render_template("teams.html")
