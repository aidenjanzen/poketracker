from sqlalchemy import Boolean, Float, Numeric, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import functions as func
from database import db
from flask import jsonify
from flask_login import UserMixin

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False, unique=False)
    collections = relationship("Collection")

class Collection(db.Model):
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey(Users.id), nullable=False)
    users = relationship("Users", back_populates="collections")
    pokemon = relationship("PokeCollection", back_populates="collections", cascade="all, delete-orphan")

class Pokemon(db.Model):
    number = mapped_column(Integer, primary_key=True)
    collection_id = mapped_column(Integer, ForeignKey(Collection.id), nullable=False)
    collections = relationship("PokeCollection")

class PokeCollection(db.Model):
    id = mapped_column(Integer, primary_key=True)
    collection_id = mapped_column(Integer, ForeignKey(Collection.id), nullable=False)
    pokemon_number = mapped_column(Integer, ForeignKey(Pokemon.number), nullable=False)
    collections = relationship("Collection")
    pokemon = relationship("Pokemon", back_populates="collections")  # back populates
