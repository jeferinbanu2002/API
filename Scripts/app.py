from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contact = db.Column(db.String(100), unique=True)

    def __init__(self, name, contact):
        self.name = name
        self.contact = contact

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'contact')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Add new user
@app.route('/user', methods=['POST'])
def add_user():
    name = request.json['name']
    contact = request.json['contact']
    new_user = User(name, contact)
    try:
        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify(new_user)
    except IntegrityError:
        db.session.rollback()  # Rollback the session to avoid it being in an invalid state
        return jsonify({"message": "User with this contact already exists."}), 409

# Get all users
@app.route('/user', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

# Get user by ID
@app.route('/user/<id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

# Update user by ID
@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    name = request.json['name']
    contact = request.json['contact']
    user.name = name
    user.contact = contact
    db.session.commit()
    return user_schema.jsonify(user)

# Delete user by ID
@app.route('/user/<id>', methods=['DELETE'])
def delete_user_by_id(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created.")
    app.run(debug=True, port=5000)

