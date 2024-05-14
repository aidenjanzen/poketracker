from flask import Blueprint, jsonify, request, url_for
from database import db
from models import Users, Collection, PokeCollection, Pokemon
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_login import current_user

api_collections_bp = Blueprint("api_collections", __name__)

@api_collections_bp.route("/collections")
def get_collection():

    # id = current_user.id

    # request = db.session.execute(db.select(PokeCollection).where(PokeCollection.collection_id == id)).order_by(PokeCollection.pokemon_number)
    

    collection_id = current_user.collections[0].id

    # Query PokeCollection based on the collection ID
    request = db.session.execute(
        db.select(PokeCollection).where(PokeCollection.collection_id == collection_id)
        .order_by(PokeCollection.pokemon_number)
    )
    results = request.scalars()
    return render_template('./collections.html', pokemon=results)