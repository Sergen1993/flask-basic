from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from datetime import timedelta
from os import environ
from dotenv import load_dotenv
from models.user import User, UserSchema
from models.card import Card, CardSchema
from init import db, ma, bcyrpt, jwt
from blueprints.cli_bp import db_commands

load_dotenv()

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')

db.init_app(app)
ma.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)

def admin_required():
    user_email = get_jwt_identity()
    stmt = db.select(User).filter_by(email=user_email)
    user = db.session.scalar(stmt)
    if not (user and user.is_admin):
        abort(401)

@app.errorhandler(401)
def unauthorized(err):
    return {'error': 'You must be an admin'}, 401


app.register_blueprint(db_commands)


@app.route('/register', methods=['POST'])
def register():
    try:
        user_info = UserSchema().load(request.json)
        user = User(
            email=user_info['email'],
            password=bcrypt.generate_password_hash(user_info['password']).decode('utf-8'),
            name=user_info['name']
        )
        db.session.add(user)
        db.session.commit()
        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        return {'error': 'Email address already in use'}, 409

@app.route('/login', methods=['POST'])
def login():
    try:
        stmt = db.select(User).filter_by(email=request.json['email'])
        user = db.session.scalar(stmt)
        if user and bcrypt.check_password_hash(user.password, request.json['password']):
            token = create_access_token(identity=user.email, expires_delta=timedelta(days=1))
            return {'token': token, 'user': UserSchema(exclude=['password']).dump(user)}
        else:
            return {'error': 'Invalid email address or password'}, 401
    except KeyError:
        return {'error': 'Email and password are required'}, 400

@app.route('/cards')
@jwt_required()
def all_cards():
    admin_required()


@app.route("/")
def index():
    return "Hello World!"



if __name__ == "__main__":
    app.run(debug=True)