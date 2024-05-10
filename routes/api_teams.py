from flask import Blueprint, jsonify, request, url_for
from database import db
from models import Users
from flask import Flask, render_template, jsonify, request, redirect, url_for

api_teams_bp = Blueprint("api_teams", __name__)

@api_teams_bp.route("/")
def create_order():
    # data = request.json
    # if "customer_id" not in data:
    #     return "Invalid request", 400
    # if not isinstance(data["customer_id"], int):
    #     return "Invalid value", 400
    
    # customer = db.get_or_404(Customer, data["customer_id"])
    # order = Order(customers=customer)
    # db.session.add(order)

    # for item in data["items"]:
    #     product = db.select(Product).where(Product.name == item["name"])
    #     addProduct = db.session.execute(product).scalar()
    #     if addProduct == None:
    #         return "Product not found", 400
    #     if not isinstance(item["quantity"], int):
    #         return "Invalid quantity value", 400
    #     if item["quantity"] <=0:
    #         return "Must enter a positive product amount", 400
    #     final = ProductOrder(orders=order, product=addProduct, quantity=item["quantity"])
    #     db.session.add(final)
    # order.total = order.order_total()
    # db.session.commit()
    return "Order added", 204