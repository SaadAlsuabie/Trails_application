from flask import Flask, request, jsonify, make_response
from db import APPDB
from flask_restful import Api, Resource
from decorators import auth_required
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

SWAGGER_URL = '/apidocs'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name' : "Trails API"
    }
)

app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix = SWAGGER_URL)
api = Api(app)

entities = ['Users', 'trails', 'locations', 'trail_access_logs']
db_instance = APPDB(entities)


class TrailList(Resource):
    @auth_required
    def get(self):
        """Get all trails"""
        result = db_instance.get_trails()
        if 'server error' in result:
            return make_response(jsonify({'Error': "INTERNAL SERVER ERROR"}), 500)
        return make_response(jsonify(result), 200)
    
    @auth_required
    def post(self):
        """Create a new trail"""
        data = request.json
        result = db_instance.create_trail(data['name'], data['description'], data['owner_id'])
        if 'server error' in result:
            return make_response(jsonify({'Error': "INTERNAL SERVER ERROR"}), 500)
        return make_response(jsonify(result), 201)


class Trail(Resource):
    @auth_required
    def get(self, trail_id):
        """Get a single trail by ID"""
        result = db_instance.get_trail(trail_id)
     
        if 'server error' in result:
            return make_response(jsonify({'Error': "INTERNAL SERVER ERROR"}), 500)
        if result is None:
            return make_response(jsonify({'error': 'Trail not found'}), 404)
        
        return make_response(jsonify(result), 200)

    @auth_required
    def put(self, trail_id):
        """Update a trail"""
        data = request.json
        result = db_instance.update_trail(trail_id, data['name'], data['description'])
        if 'server error' in result:
            return make_response(jsonify({'Error': "INTERNAL SERVER ERROR"}), 500)
        return make_response(jsonify(result), 200)

    @auth_required
    def delete(self, trail_id):
        """Delete a trail"""
        result = db_instance.delete_trail(trail_id)
        if 'server error' in result:
            return make_response(jsonify({'Error': "INTERNAL SERVER ERROR"}), 500)
        return make_response(jsonify(result), 200)
    

api.add_resource(TrailList, '/trails')
api.add_resource(Trail, '/trails/<int:trail_id>')

if __name__ == '__main__':
    app.run(debug=True)
