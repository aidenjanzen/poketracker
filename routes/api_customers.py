from flask import Blueprint, jsonify, request, url_for
from database import db
from models import Customer
# Creates a Blueprint object (similar to Flask). Make sure you give it a name!
api_customers_bp = Blueprint("api_customers", __name__)

@api_customers_bp.route("/", methods=["GET"])
def customers_json():
    statement = db.select(Customer).order_by(Customer.name)
    results = db.session.execute(statement)
    customers = []  # output variable
    for customer in results.scalars():
        temp = customer.to_json()
        customers.append(temp)
    return customers

@api_customers_bp.route("/<int:customer_id>")
def customer_detail_json(customer_id):
    statement = db.select(Customer).where(Customer.id == customer_id)
    result = db.session.execute(statement)
    customer = result.scalar()
    customer = customer.to_json()
    return jsonify(customer)

@api_customers_bp.route("/<int:customer_id>", methods=["DELETE"])
def customer_delete(customer_id):
    customer = db.get_or_404(Customer, customer_id)
    db.session.delete(customer)
    db.session.commit()
    return "Customer deleted", 204

@api_customers_bp.route("/", methods=["POST"])  # post makes a new customer
def add_customer():
    data = request.json
    if "name" not in data or "phone" not in data:
        return "Invalid request", 400
    customer = Customer(name=data["name"], phone=data["phone"])
    db.session.add(customer)
    db.session.commit()
    return "Customer Added", 201

@api_customers_bp.route("/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    data = request.json
    customer = db.get_or_404(Customer, customer_id)
    if "balance" not in data:
        return "Invalid request", 400
    balance = data["balance"]
    if not isinstance(balance, (int, float)):  # has to be tuple not list
        return "Invalid request: balance", 400
    customer.balance = balance
    #here would be nice to update the phone, name, 
    db.session.commit()
    return "Customer updated", 204

