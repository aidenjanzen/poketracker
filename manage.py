from database import db
from models import Customer, Product, Order, ProductOrder
import csv
from sqlalchemy.sql import functions as func
import random
from app import app


def main():
    with open("./data/customers.csv", "r") as file:
        data = csv.DictReader(file)
        for i in data:
            obj = Customer(name=i["name"], phone=i["phone"])
            db.session.add(obj)
            db.session.commit()

    with open("./data/products.csv", "r") as file:
        data = csv.DictReader(file)
        for i in data:
            obj = Product(name=i["name"], price=i["price"])
            db.session.add(obj)
            db.session.commit()


def test_relationships():
    customer = Customer(name="TEST", phone="778-778-7788")
    db.session.add(customer)
    order = Order(customer_id=21, total=13.50)
    product_order = ProductOrder(order_id=1, product_id=1, quantity=5)
    db.session.add(customer)
    db.session.add(order)
    db.session.add(product_order)
    db.session.commit()
    print(customer.orders)
    print(order.customers)
    print(order.products)
    print(order.products[0].product)
    print(order.products[0].product.name)
    print(customer.orders[0].products[0].quantity)


def random_orders():
    # Find a random customer
    cust_stmt = db.select(Customer).order_by(func.random()).limit(1)
    customer = db.session.execute(cust_stmt).scalar()
# Make an order
    order = Order(customers=customer)
    db.session.add(order)
# Find a random product
    prod_stmt = db.select(Product).order_by(func.random()).limit(1)
    product = db.session.execute(prod_stmt).scalar()
    rand_qty = random.randint(10, 20)
# Add that product to the order
    association_1 = ProductOrder(
        orders=order, product=product, quantity=rand_qty)
    db.session.add(association_1)
# Do it again
    prod_stmt = db.select(Product).order_by(func.random()).limit(1)
    product = db.session.execute(prod_stmt).scalar()
    rand_qty = random.randint(10, 20)
    association_2 = ProductOrder(
        orders=order, product=product, quantity=rand_qty)
    db.session.add(association_2)
    order.total=order.order_total()
# Commit to the database
    db.session.commit()
    print("Thisworked")


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        main()
        # test_relationships()
        random_orders()
        random_orders()
        random_orders()
        random_orders()
        random_orders()
        random_orders()
        random_orders()
        random_orders()
        random_orders()
