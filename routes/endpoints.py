from database import db
from flask import Blueprint
from flask import Flask, render_template, jsonify, request, redirect, url_for
from models import Users, Collection, PokeCollection, Pokemon
from flask_login import login_user, logout_user, current_user
import requests

from pokedex import pokedex

import os
web_pages_bp = Blueprint("html", __name__)

@web_pages_bp.route("/")
def base():
    return render_template("home.html", current_page="home")

@web_pages_bp.route("/home")
def home():
    return render_template("home.html", current_page="home")

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

@web_pages_bp.route("/add", methods=["POST"])
def add_pokemon():

    if not current_user.is_authenticated:
        return render_template("register.html")

    number = request.form.get("pokemon_number")
    gen_number = request.form.get("gen_number")

    collection = Collection.query.filter_by(user_id=current_user.id).first()
    if not collection:
        collection = Collection(user_id=current_user.id)
        db.session.add(collection)
        db.session.commit()


    exist = db.session.execute(db.select(PokeCollection).where(
        PokeCollection.collection_id == collection.id, 
        PokeCollection.pokemon_number==number
        )).first()
    if exist:
        return redirect(url_for('html.gen', number=gen_number))

    pokemon = db.select(Pokemon).where(Pokemon.number == number)
    addPokemon = db.session.execute(pokemon).scalar()
    if addPokemon == None:
        pokemon = Pokemon(number=number)
        db.session.add(pokemon)

    pokecollection = PokeCollection(collection_id=collection.id, pokemon_number=number)
    db.session.add(pokecollection)

    db.session.commit()


    return redirect(url_for('html.gen', number=gen_number))


@web_pages_bp.route("/remove", methods=["POST"])
def remove_pokemon():
    if not current_user.is_authenticated:
        return render_template("register.html")
    
    number = request.form.get("pokemon_number")

    collection = Collection.query.filter_by(user_id=current_user.id).first()

    exist = db.session.execute(db.select(PokeCollection).where(
        PokeCollection.collection_id == collection.id, 
        PokeCollection.pokemon_number==number
        )).scalar()

    db.session.delete(exist)
    db.session.commit()
 
    return redirect(url_for('api_collections.get_collection'))
