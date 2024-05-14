from flask import Blueprint, jsonify, request, url_for
from database import db
from models import Users, Collection, PokeCollection, Pokemon
from flask import Flask, render_template, jsonify, request, redirect, url_for

api_teams_bp = Blueprint("api_teams", __name__)

@api_teams_bp.route("/")
def get_collection():
    pokemon = db.session.execute(db.select(Collection).where(
        Collection.collection_id == collection.id, 
        PokeCollection.pokemon_number==number
        )).first()
    
    request = db.session.execute(db.select(Order).order_by(Order.id)) 
    orders = []

    for i in request.scalars():
        i.total = Order.price(i)
        db.session.commit()
        order = {
            'id': i.id, 
            'customer_id': i.customer_id, 
            'products': [f"{products.product.product} ({products.quantity})" for products in i.products_order], 
            'total': Order.price(i),
            'processed': None
        }
        order['processed'] = i.processed or 'Not processed'

        orders.append(order)

    return render_template('./orders.html', orders=orders)