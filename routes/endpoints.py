from database import db
from flask import Blueprint
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from models import Users, Collection, PokeCollection, Pokemon
from flask_login import login_user, logout_user, current_user
import requests
import string

from pokedex import pokedex

import os
web_pages_bp = Blueprint("html", __name__)


@web_pages_bp.route("/")
def base():
    return render_template("home.html", current_page="nogen")


@web_pages_bp.route("/home")
def home():
    return render_template("home.html", current_page="nogen")


@web_pages_bp.route("/gen<int:number>")
def gen(number):
    amounts = [151, 100, 135, 107, 156, 72, 88, 96, 120]
    startNumber = [1, 152, 252, 387, 494, 650, 722, 810, 906]
    return render_template("generations.html", number=number, pokedex=pokedex, amounts=amounts, startNumber=startNumber)


@web_pages_bp.route("/register")
def register():
    return render_template("register.html", current_page="nogen")


@web_pages_bp.route("/login")
def login():
    return render_template("login.html", current_page="nogen")


@web_pages_bp.route("/logout")
def logout():
    logout_user()
    return render_template("home.html", current_page="nogen")


@web_pages_bp.route("/add", methods=["POST"])
def add_pokemon():

    if not current_user.is_authenticated:
        flash("You are not logged in.")
        return redirect(url_for('html.login'))

    number = request.form.get("pokemon_number")
    gen_number = request.form.get("gen_number")

    collection = Collection.query.filter_by(user_id=current_user.id).first()
    if not collection:
        collection = Collection(user_id=current_user.id)
        db.session.add(collection)
        db.session.commit()

    exist = db.session.execute(db.select(PokeCollection).where(
        PokeCollection.collection_id == collection.id,
        PokeCollection.pokemon_number == number
    )).first()
    if exist:
        return redirect(url_for('html.gen', number=gen_number))

    pokemon = db.select(Pokemon).where(Pokemon.number == number)
    addPokemon = db.session.execute(pokemon).scalar()
    if addPokemon == None:
        pokemon = Pokemon(number=number)
        db.session.add(pokemon)

    pokecollection = PokeCollection(
        collection_id=collection.id, pokemon_number=number)
    db.session.add(pokecollection)

    db.session.commit()

    return redirect(url_for('html.gen', number=gen_number))


@web_pages_bp.route("/remove", methods=["POST"])
def remove_pokemon():
    if not current_user.is_authenticated:
        flash("You are not logged in.")
        return redirect(url_for('html.login'))

    number = request.form.get("pokemon_number")

    collection = Collection.query.filter_by(user_id=current_user.id).first()

    exist = db.session.execute(db.select(PokeCollection).where(
        PokeCollection.collection_id == collection.id,
        PokeCollection.pokemon_number == number
    )).scalar()

    if exist:
        db.session.delete(exist)
        db.session.commit()
    return redirect(url_for('api_collections.get_collection'))


@web_pages_bp.route("/info<int:number>",)
def info(number):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{number}/")
    data = response.json()

    weight = data['weight']
    height = data['height']

    hp = None
    defense = None
    attack = None
    special_attack = None
    special_defense = None
    speed = None

    for stat in data['stats']:
        if stat['stat']['name'] == 'hp':
            hp = stat['base_stat']
        if stat['stat']['name'] == 'defense':
            defense = stat['base_stat']
        if stat['stat']['name'] == 'attack':
            attack = stat['base_stat']
        if stat['stat']['name'] == 'special-attack':
            special_attack = stat['base_stat']
        if stat['stat']['name'] == 'special-defense':
            special_defense = stat['base_stat']
        if stat['stat']['name'] == 'speed':
            speed = stat['base_stat']


    # moves = []

    # for move in data['moves']:
    #     move_name = move["move"]["name"]
    #     for version_detail in move["version_group_details"]:
    #         version_name = version_detail["version_group"]["name"]
    #         moves.append(
    #             {"name": move_name, "version": version_name})


    response = requests.get(
        f"https://pokeapi.co/api/v2/pokemon/{number}/encounters")
    data = response.json()

    locations_with_versions = []

    for location in data:
        location_name = location["location_area"]["name"]
        location_name = location_name.replace("-", " ")
        location_name = string.capwords(location_name)
        
        for version_detail in location["version_details"]:
            version_name = version_detail["version"]["name"]
            version_name = version_name.replace("-", " ")
            version_name = string.capwords(version_name)

            locations_with_versions.append(
                {"location": location_name, "version": version_name})
            
    

    return render_template("info.html",
                           pokedex=pokedex,
                           number=number,
                           weight=weight, height=height,
                           locations=locations_with_versions,
                           hp=hp, defense=defense,
                           attack=attack,
                           special_attack=special_attack,
                           special_defense=special_defense,
                           speed=speed,
                        #    moves=moves
                           )
