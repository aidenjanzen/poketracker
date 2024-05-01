from flask import Flask, render_template, jsonify, request, redirect, url_for
import csv
from pathlib import Path
from database import db
from models import Customer, Product, Order, ProductOrder
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.py"  # database url

# picFolder = os.path.join('static', 'sprites') #allows access by using current_app. in blueprints
# app.config['UPLOAD_FOLDER'] = picFolder

app.instance_path = Path("./data").resolve()  # current path
db.init_app(app)




from routes import api_orders_bp, api_products_bp, api_customers_bp, web_pages_bp, api_final_bp
app.register_blueprint(api_customers_bp, url_prefix="/api/customers")
app.register_blueprint(api_products_bp, url_prefix="/api/products")
app.register_blueprint(api_orders_bp, url_prefix="/api/orders")
app.register_blueprint(web_pages_bp, url_prefix="/")

app.register_blueprint(api_final_bp, url_prefix="/")



if __name__ == "__main__":  # keep at the bottom
    app.run(debug=True, port=8888)
