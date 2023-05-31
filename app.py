from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://trello_dev:spameggs123@localhost:5432/trello'

db = SQLAlchemy(app)

class Card(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100))
  description = db.Column(db.Text())
  date_created = db.Column(db.Date())

@app.cli.command('create')
def create_db():
  db.create_all()
  print('Tables created successfully')

@app.cli.command('seed')
def seed_db():
    card = Card(
      title = 'Start the project',
      description = 'Stage 1 - Create an ERD',
      date = date.today()
    )

    db.session.add(card)
    

@app.route('/')
def index():
  return 'Hello World!'

if __name__ == '__main__':
  app.run(debug=True)