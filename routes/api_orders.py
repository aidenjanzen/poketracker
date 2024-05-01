from flask import Blueprint, jsonify, request
from database import db
from models import Customer, Order, Product, ProductOrder

api_orders_bp = Blueprint("api_orders", __name__)

@api_orders_bp.route("/", methods=["POST"])
def create_order():
    data = request.json
    if "customer_id" not in data:
        return "Invalid request", 400
    if not isinstance(data["customer_id"], int):
        return "Invalid value", 400
    
    customer = db.get_or_404(Customer, data["customer_id"])
    order = Order(customers=customer)
    db.session.add(order)

    for item in data["items"]:
        product = db.select(Product).where(Product.name == item["name"])
        addProduct = db.session.execute(product).scalar()
        if addProduct == None:
            return "Product not found", 400
        if not isinstance(item["quantity"], int):
            return "Invalid quantity value", 400
        if item["quantity"] <=0:
            return "Must enter a positive product amount", 400
        final = ProductOrder(orders=order, product=addProduct, quantity=item["quantity"])
        db.session.add(final)
    order.total = order.order_total()
    db.session.commit()
    return "Order added", 204

@api_orders_bp.route("/<int:order_id>", methods=["PUT"])
def process_order_api(order_id):
    data=request.json

    strategy = data.get("strategy", "adjust")

    ava_strategies = ["adjust", "ignore", "reject"]
    order = db.get_or_404(Order, order_id)
    if data["process"]!= True:
        return "Process is not True.", 400
    
    if strategy not in ava_strategies:
        return "Process Strategy Not Found.", 400
    result, code = order.process_order(strategy)
    return result, code

