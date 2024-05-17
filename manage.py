from database import db
from app import app
from models import Users

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = Users(username="mpt", password="123")
        db.session.add(user)
        db.session.commit()
