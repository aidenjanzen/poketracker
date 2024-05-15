from flask import Blueprint, jsonify, request, url_for
from database import db
from models import Users, Collection, PokeCollection, Pokemon
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_login import current_user

from pokedex import pokedex

api_collections_bp = Blueprint("api_collections", __name__)

@api_collections_bp.route("/collections")
def get_collection():
    if not current_user.is_authenticated:
        return render_template("register.html", error="You are not logged in.")
    
    collection = Collection.query.filter_by(user_id=current_user.id).first()
    if not collection:
        collection = Collection(user_id=current_user.id)
        db.session.add(collection)
        db.session.commit()
    
    collection_id = current_user.collections[0].id

    request = db.session.execute(
        db.select(PokeCollection).where(PokeCollection.collection_id == collection_id)
        .order_by(PokeCollection.pokemon_number)
    )
    results = request.scalars()
    # temp = []
    # for i in results:
    #     temp.append(i.pokemon_number)
    # print(temp)
    return render_template('./collections.html', pokemon=results, pokedex=pokedex)