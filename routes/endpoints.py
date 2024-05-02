from database import db
from flask import Blueprint
from flask import Flask, render_template, jsonify, request, redirect, url_for
from models import Customer, Product, Order, ProductOrder

import os
web_pages_bp = Blueprint("html", __name__)

@web_pages_bp.route("/")
def base():
    imageList = os.listdir('static/sprites')
    imagelist = sorted(['sprites/' + image for image in imageList if image.endswith(".png")], key=lambda x: int(os.path.splitext(x.split('/')[-1])[0]))

    return render_template("home.html", sprites=imagelist)


@web_pages_bp.route("/home")
def home():
    return render_template("home.html")


@web_pages_bp.route("/customers")
def customers():
    statement = db.select(Customer).order_by(Customer.name)
    records = db.session.execute(statement)
    results = records.scalars()
    return render_template("customers.html", customers=results)


@web_pages_bp.route("/customers/<int:customer_id>")
def customer_details(customer_id):
    statement = db.select(Customer).where(Customer.id == customer_id)
    result = db.session.execute(statement)
    customer = result.scalar()
    return render_template("customerorders.html", customer=customer)



@web_pages_bp.route("/products")
def products():
    statement = db.select(Product).order_by(Product.name)
    records = db.session.execute(statement)
    results = records.scalars()
    return render_template("products.html", products=results)


@web_pages_bp.route("/orders")
def orders():
    statement = db.select(Order).order_by(Order.id)
    records = db.session.execute(statement)
    results = records.scalars()
    return render_template("orders.html", orders=results,) #customers=results1

@web_pages_bp.route("/orders/<int:order_id>")
def order_details(order_id):
    statement = db.select(Order).where(Order.id == order_id)
    result = db.session.execute(statement)
    order = result.scalar()
    return render_template("orderdetails.html", order=order)

@web_pages_bp.route("/orders/<int:order_id>/delete", methods=["POST"])
def order_delete(order_id):
    order = db.get_or_404(Order, order_id)
    statement= db.select(ProductOrder).where(ProductOrder.order_id == order_id)
    results = db.session.execute(statement).scalars()
    for product_order in results:
        db.session.delete(product_order)
    db.session.commit()
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for("html.orders"))


@web_pages_bp.route("/orders/<int:order_id>/process", methods=["POST"])
def process_order_web(order_id):
    order = db.get_or_404(Order, order_id)
    result = order.process_order()
    db.session.commit()
    print(result) #error if any
    return redirect(url_for("html.orders"))
