import pymongo
import jwt
from flask import Flask, jsonify, request, Response, abort
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from flask_pymongo import PyMongo
from datetime import datetime, timedelta


#MONGODB_URI = 'mongodb://admin:URL_GOES_HERE:PORT/NAME_OF_DB'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'
# connect to local database
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = 27017
app.config['MONGO_DBNAME'] = 'chemo'
mongo = PyMongo(app, config_prefix='MONGO')

#mongo = pymongo.MongoClient(MONGODB_URI)
#db = mongo.get_default_database()

def create_token(user_id):
    payload = {
            # subject
            'sub': user_id,
            #issued at
            'iat': datetime.utcnow(),
            #expiry
            'exp': datetime.utcnow() + timedelta(days=1)
            }

    token = jwt.encode(payload, app.secret_key, algorithm='HS256')
    return token.decode('unicode_escape')

def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, app.secret_key, algorithms='HS256')

@app.errorhandler(400)
def respond400(error):
    return jsonify({'message': error.description['message']})
@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/users", methods=['GET'])
def list_users():
    users = mongo.db.users.find()
    for document in users:
        print(document)
    print users
    return "Hello World!"

@app.route('/login', methods=['POST'])
def login():
    email = request.get_json().get('email')
    password = request.get_json().get('password')

    cursor = mongo.db.users.find({"email": email})

    if cursor.count() == 0:
        error_message = "A user with the email " + email + " does not exist."
        abort(400, {'message': error_message})


    user_document = cursor.next()

    if not check_password_hash(user_document['password'], password):
        error_message = "Invalid password for " + email + "."
        abort(400, {'message': error_message})

    userid = str(user_document['_id'])
    token = create_token(userid)
    print(token)
    resp = jsonify({"access_token": token,
                    "userid": userid})

    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/register', methods = ['POST'])
def register():
    name = request.get_json().get('name')
    password = request.get_json().get('password')
    email = request.get_json().get('email')


    if name is None or password is None or email is None:
        # missing arguments
        abort(400, {'message': 'Missing required parameters' \
            ' name, password, and email are ALL required.'})

    # Should do error checking to see if user exists already
    if mongo.db.users.find({"email": email}).count() > 0:
        # Email already exists
        abort(400, {'message': 'A user with the email #{email} already exists'})



    _id = mongo.db.users.insert({"name": name, "password": generate_password_hash(password), "email" : email})

    user = User(str(_id), name, password, email, location)

    # Now we have the Id, we need to create a jwt access token
    # and send the corresponding response back
    token = create_token(user.id)
    resp = jsonify({"access_token": token,
                    "userid": str(_id)})

    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == "__main__":
    app.run()