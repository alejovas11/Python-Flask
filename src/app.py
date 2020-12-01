from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost:27017/citas'
mongo = PyMongo(app)

@app.route('/addCita', methods=['POST'])
def create_user():
    name = request.json['name']
    lastName = request.json['lastName']
    identification = request.json['identification']
    birthDate = request.json['birthDate']
    city = request.json['city']
    neighborhood = request.json['neighborhood']
    phone = request.json['phone']

    if name and lastName and identification and birthDate and city and neighborhood and phone:
        id = mongo.db.customers.insert(
            {
                'name' : name,
                'lastName' : lastName,
                'identification' : identification,
                'birthDate' : birthDate,
                'city' : city,
                'neighborhood' : neighborhood,
                'phone' : phone
            }
        )
        response = {
            'id': str(id),
            'name' : name,
            'lastName' : lastName,
            'identification' : identification,
            'birthDate' : birthDate,
            'city' : city,
            'neighborhood' : neighborhood,
            'phone' : phone
        }
        return response
    else:
        return not_found()
    
    return {'message': 'received'}

@app.route('/getCitas', methods=['GET'])
def get_users():
    customers = mongo.db.customers.find()
    response = {"citas": customers}
    return Response(json_util.dumps(response),  mimetype='application/json')

@app.route('/customer/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.customers.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json')

@app.route('/deleteCita/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.customers.delete_one({'_id': ObjectId(id)})
    response = jsonify({
        'message': 'Customer ' + id + ' was deleted successfully'
    })
    return response

@app.route('/updateCita/<id>', methods=['PUT'])
def update_user(id):
    name = request.json['name']
    lastName = request.json['lastName']
    identification = request.json['identification']
    birthDate = request.json['birthDate']
    city = request.json['city']
    neighborhood = request.json['neighborhood']
    phone = request.json['phone']

    if name and lastName and identification and birthDate and city and neighborhood and phone:
        mongo.db.customers.update_one({'_id': ObjectId(id)}, {'$set': {
            'name' : name,
            'lastName' : lastName,
            'identification' : identification,
            'birthDate' : birthDate,
            'city' : city,
            'neighborhood' : neighborhood,
            'phone' : phone
        }})
        response = jsonify({
        'message': 'Customer ' + id + ' was updated successfully'
    })
    return response

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource not found: ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(debug=True)