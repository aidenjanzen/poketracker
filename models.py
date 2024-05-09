from sqlalchemy import Boolean, Float, Numeric, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import functions as func
from database import db
from flask import jsonify
from flask_login import UserMixin

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

class Customer(db.Model):
    id = mapped_column(Integer, primary_key=True)  # auto increments by default
    name = mapped_column(String(200), nullable=False, unique=True)
    phone = mapped_column(String(20), nullable=False)
    balance = mapped_column(Numeric(10, 2), nullable=False, default=0)
    orders = relationship("Order")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "balance": self.balance,
        }


class Order(db.Model):
    id = mapped_column(Integer, primary_key=True)
    customer_id = mapped_column(Integer, ForeignKey(Customer.id), nullable=False)
    customers = relationship("Customer", back_populates="orders")
    products = relationship("ProductOrder", back_populates="orders", cascade="all, delete-orphan")
    total = mapped_column(Numeric(10,2), default=0)
    created = mapped_column(DateTime, nullable=False, default=func.now())
    processed = mapped_column(DateTime, nullable=True)
    
    def order_total(self):
        total = 0
        for product in self.products: #products is productorder
            value = product.quantity * product.product.price
            total = total + value
        return total
    def process_order(self, strategy="adjust"):
        order_total = 0
        if self.processed is not None:
            return "Order Already Processed", 400
        if self.customers.balance <= 0:
            return "Balance low", 400
        
        if strategy == "adjust":
            for product in self.products:
                if product.quantity > product.product.available:
                    product.quantity = product.product.available
                product.product.available -= product.quantity
                order_total += product.quantity * product.product.price
        elif strategy == "reject":
            for product in self.products:
                if product.quantity > product.product.available:
                    return "Rejected Order. Not enough product in store.", 400
            for product in self.products:
                product.product.available -= product.quantity
                order_total += product.quantity * product.product.price

        else:
            for product in self.products:
                if product.quantity > product.product.available:
                    product.quantity = 0
                product.product.available -= product.quantity
                order_total += product.quantity * product.product.price
        self.customers.balance -= order_total
        self.total = order_total
        self.processed = func.now()
        db.session.commit()
        return "Order Processed", 200 #return true doesnt work here

class Product(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(200), nullable=False, unique=True)
    price = mapped_column(Numeric(10, 2), nullable=False)
    available = mapped_column(Integer, nullable=False, default=1)  # true
    orders = relationship("ProductOrder")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
        }
    

class ProductOrder(db.Model):
    id = mapped_column(Integer, primary_key=True)
    order_id = mapped_column(Integer, ForeignKey(Order.id), nullable=False)
    product_id = mapped_column(Integer, ForeignKey(Product.id), nullable=False)
    orders = relationship("Order")
    product = relationship("Product", back_populates="orders")  # back populates
    quantity = mapped_column(Integer, nullable=False)

    def price_quantity(self):
        return self.quantity * self.product.price