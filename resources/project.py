from flask import jsonify
from flask_restful import abort, Resource
from model import database, Project

_fields = ('title', 'description', 'youtube', 'github', 'category.name', 'user.name', 'user.surname',
           'user.place.city.name', 'user.place.name', 'created_time', 'comments.user.name',
           'comments.user.surname', 'comments.text', 'comments.created_time')


class ProjectResource(Resource):
    def get(self, id):
        project = database.session.query(Project).filter(Project.id == id).first()
        if not project:
            abort(404)
        return jsonify(project.to_dict(only=_fields))


class ProjectsResource(Resource):
    def get(self):
        projects = database.session.query(Project).all()
        return jsonify({'projects': [project.to_dict(only=_fields) for project in projects]})
