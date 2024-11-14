from flask import Flask, request, jsonify
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
        if 'error' in result:
            return jsonify(result), 500
        return jsonify(result)
    
    @auth_required
    def post(self):
        """Create a new trail"""
        data = request.json
        result = db_instance.create_trail(data['name'], data['description'], data['owner_id'])
        if 'error' in result:
            return jsonify(result), 500
        return jsonify(result), 201


class Trail(Resource):
    @auth_required
    def get(self, trail_id):
        """Get a single trail by ID"""
        result = db_instance.get_trail(trail_id)
        if 'error' in result:
            return jsonify(result), 500
        if result is None:
            return jsonify({'error': 'Trail not found'}), 404
        return jsonify(result)

    @auth_required
    def put(self, trail_id):
        """Update a trail"""
        data = request.json
        result = db_instance.update_trail(trail_id, data['name'], data['description'])
        if 'error' in result:
            return jsonify(result), 500
        return jsonify(result)

    @auth_required
    def delete(self, trail_id):
        """Delete a trail"""
        result = db_instance.delete_trail(trail_id)
        if 'error' in result:
            return jsonify(result), 500
        return jsonify(result)
    

api.add_resource(TrailList, '/trails')
api.add_resource(Trail, '/trails/<int:trail_id>')

if __name__ == '__main__':
    app.run(debug=True)
