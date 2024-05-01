from flask import Blueprint, jsonify, request, url_for
from database import db
from models import Product, Customer
api_final_bp = Blueprint("api_final", __name__)


@api_final_bp.route("/final/customers-warning", methods=["GET"])
def warn_customer():
    statement = db.select(Customer).where(Customer.balance <= 0)
    results = db.session.execute(statement)
    customers = []
    for customer in results.scalars():
        json_record = {
            "name": customer.name,
            "balance": customer.balance,
            "url": f"{url_for('api_customers.customers_json')}{customer.id}"
        }
        customers.append(json_record)
    return jsonify(customers)


@api_final_bp.route("/final/out-of-stock", methods=["GET"])
def warn_product():
    statement = db.select(Product).where(Product.available == 0)
    results = db.session.execute(statement)
    products = []
    for product in results.scalars():
        products.append(product.name)
    return jsonify(products)
    

    