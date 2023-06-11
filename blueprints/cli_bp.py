from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from models.user import User
from models.card import Card
from init import db, bcyrpt

db_commands = Blueprint('db', __name__)

@db_commands.cli.command("create")
def create_db():
    db.drop_all()
    db.create_all()
    print("Tables created successfully")

@db_commands.cli.command("seed")
def seed_db():
    users = [
        User(
            email='admin@spam.com',
            password=bcrypt.generate_password_hash('spinynorman').decode('utf-8'),
            is_admin=True
        ),
        User(
            name='John Cleese',
            email='cleese@spam.com',
            password=bcrypt.generate_password_hash('tisbutascratch').decode('utf-8')
        )
    ]

    cards = [
        Card(
            title="Start the project",
            description="Stage 1 - Create an ERD",
            status="Done",
            date_created=date.today(),
        ),
        Card(
            title="ORM Queries",
            description="Stage 2 - Implement several queries",
            status="In Progress",
            date_created=date.today(),
        ),
        Card(
            title="Marshmallow",
            description="Stage 3 - Implement jsonify of models",
            status="In Progress",
            date_created=date.today(),
        ),
    ]

    db.session.query(Card).delete()
    db.session.query(User).delete()

    db.session.add_all(cards)
    db.session.add_all(users)

    db.session.commit()
    print("Models seeded")