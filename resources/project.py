from flask import current_app, jsonify, request
from flask_restful import Resource, abort
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from model import Project, User, database

_fields = ('id', 'title', 'description', 'youtube', 'github', 'category.name',
           'user.name', 'user.surname', 'user.place.city.name', 'user.place.name',
           'created_time', 'comments.user.name', 'comments.user.surname',
           'comments.text', 'comments.created_time')

MAX_PER_PAGE = 100


class ProjectResource(Resource):
    def get(self, id):
        project = database.session.get(Project, id)
        if not project:
            abort(404, message=f'Проект {id} не найден')
        return jsonify(project.to_dict(only=_fields))


class ProjectsResource(Resource):
    def get(self):
        statement = (
            select(Project)
            .order_by(Project.created_time.desc())
            .options(
                joinedload(Project.category),
                joinedload(Project.user).joinedload(User.place),
            )
        )
        pagination = database.paginate(
            statement,
            per_page=request.args.get(
                'per_page', current_app.config['PROJECTS_PER_PAGE'], type=int),
            max_per_page=MAX_PER_PAGE,
            error_out=False,
        )
        return jsonify({
            'projects': [project.to_dict(only=_fields) for project in pagination.items],
            'page': pagination.page,
            'pages': pagination.pages,
            'total': pagination.total,
        })
