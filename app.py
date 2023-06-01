from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://trello_dev:spameggs123@localhost:5432/trello'

db = SQLAlchemy(app)

class Card(db.Model):
  __tablename__ = 'cards'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100))
  description = db.Column(db.Text())
  status = db.Column(db.String(30))
  date_created = db.Column(db.Date())

@app.cli.command('create')
def create_db():
  db.drop_all()
  db.create_all()
  print('Tables created successfully')

@app.cli.command('seed')
def seed_db():
    # Create instances of the Card model in memory
    cards = [
        Card(
            title='Start the project',
            description='Stage 1 - Create an ERD',
            status="Done",
            date_created=date.today()
        ),
        Card(
            title='ORM Queries',
            description='Stage 2 - Implement several queries',
            status="In Progress",
            date_created=date.today()
        ),
        Card(
            title='Marshmallow',
            description='Stage 3 - Implement jsonify of models',
            status="In progress",
            date_created=date.today()
        )
    ]

    # Truncate the Card table
    db.session.query(Card).delete()

    # Add each card to the session (transaction)
    for card in cards:
        db.session.add(card)

    # Commit the transaction to the database
    db.session.commit()
    print('Models seeded')


@app.route('/cards')
def all_cards():
    # Select all cards from the table
    stmt = db.select(Card).order_by (Card.status.desc())
    cards = db.session.scalars(stmt).all()
    return json.dumps(cards)


@app.route('/')
def index():
  return 'Hello World!'

if __name__ == '__main__':
  app.run(debug=True)