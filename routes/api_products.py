from flask import Blueprint, jsonify, request
from database import db
from models import Product
api_products_bp = Blueprint("api_products", __name__)

@api_products_bp.route("/")
def products_json():
    statement = db.select(Product).order_by(Product.name)
    results = db.session.execute(statement)
    products = []  # output variable
    for product in results.scalars():
        temp = product.to_json()
        products.append(temp)
    return products

@api_products_bp.route("/<int:product_id>")
def product_detail_json(product_id):
    statement = db.select(Product).where(Product.id == product_id)
    result = db.session.execute(statement)
    product = result.scalar()
    product = product.to_json()
    return jsonify(product)

@api_products_bp.route("/<int:product_id>", methods=["DELETE"])  # delete
def product_delete(product_id):
    product = db.get_or_404(Product, product_id)
    db.session.delete(product)
    db.session.commit()
    return "Product Deleted", 204

@api_products_bp.route("/", methods=["POST"])  # post
def add_product():
    data = request.json
    if "name" not in data or "price" not in data:
        return "Invalid request", 400
    if not isinstance(data["price"], (int, float)) or data["price"] <=0:
        return "Invalid price", 400
    
    productSearch = db.select(Product).where(Product.name == data["name"])
    addProduct = db.session.execute(productSearch).scalar()
    if addProduct: #error checks if product exists already
        return "Product Already Exists", 400
    
    product = Product(name=data["name"], price=data["price"])
    if "available" in data:
        product.available = data["available"]
    db.session.add(product)
    db.session.commit()

    return "Product added", 201

@api_products_bp.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.json
    print("Start of update")
    product = db.get_or_404(Product, product_id)
    if "name" in data:
        print("name")
        product.name = data["name"]
    if "price" in data:
        if not isinstance(data["price"], (int, float)) or data["price"] < 0:
            return "Invalid request: price", 400
        product.price = data["price"]
    if "quantity" in data:
        print("quantity")
        if not isinstance(data["quantity"], [int] or data["quantity"] < 0):
            return "Invalid request: quantity", 400
        product.quantity = data["quantity"]
    print(type(product))
    db.session.commit()
    return "Product updated", 204

@api_products_bp.route("/final/warning", methods=["POST"])
def almost_out_product():
    data = request.json
    if "threshold" in data:
        statement = db.select(Product).where(Product.available < data["threshold"])
        results = db.session.execute(statement)
        products = []

        for product in results.scalars():
            json_record = {
                "name": product.name,
                "available": product.available,
            }
            products.append(json_record)
    else:
        return "Threshold not specified", 400
    
    json_record = {
        "threshold": data["threshold"], 
        "products":products,
    }
    return jsonify(json_record)
    