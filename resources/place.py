from flask import jsonify
from flask_restful import Resource
from model import database, Place


class PlacesResource(Resource):
    def get(self):
        places = database.session.query(Place).all()
        return jsonify({'places': [place.to_dict(only=('name', 'city.name'))
                                   for place in places]})
