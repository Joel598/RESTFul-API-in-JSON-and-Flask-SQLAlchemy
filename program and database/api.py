#imports here
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
#flask app name
app = Flask(__name__)

#database configuration
#database: mydb.db
app.config['PASSWORD'] = 'xyz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/dsouz/Downloads/Compressed/api/mydb.db'  

#database communication between Python program and databases
db = SQLAlchemy(app)

#classes represent as tables of database
class User(db.Model):
#database attributes
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)


#route to login method
@app.route('/login')
#function for login check

#route for retrive all user resource using public id
@app.route('/user', methods=['GET'])
#function for retriving all users
def get_all_users():
    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users' : output})
    

#route for retrive single user resource using public id
@app.route('/user/<public_id>', methods=['GET'])
def get_one_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})
    #retriving data
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user' : user_data})

#route for creating new user resource
@app.route('/user', methods=['POST'])
def create_user():
    #passing JSON data 
    data = request.get_json() 
    
    #generate hasked password
    hashed_password = generate_password_hash(data['password'], method='sha256') 
    #CREATING new users
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user) #add
    db.session.commit() #save
    #prints response for JSON
    return jsonify({'message' : 'New user created!'})

#route for updating  existing user resource using public id
@app.route('/user/<public_id>', methods=['PUT'])
def promote_user(public_id):
    #filter user by public_id
    user = User.query.filter_by(public_id=public_id).first()
    
    #user not exist
    if not user:
        return jsonify({'message' : 'No user found!'})
    
    #user exists
    user.admin = True
    db.session.commit()

    return jsonify({'message' : 'The user has been promoted!'})

#route for deleting a user resource using name attribute
@app.route('/user/<name>', methods=['DELETE'])
def delete_user(name):
    #filter user by user_name
    user = User.query.filter_by(name=name).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'User item deleted!'})

#executing the script or debugging
if __name__ == '__main__':
    app.run(debug=True)