import os

from flask import Flask, render_template
from flask_login import LoginManager
from flask_restful import Api
from flask_wtf.csrf import CSRFProtect

from config import get_config
from model import User, database
from resources.place import PlacesResource
from resources.project import ProjectResource, ProjectsResource
from views import main as main_blueprint


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config or get_config())

    database.init_app(app)
    with app.app_context():
        database.create_all()
    CSRFProtect(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Войдите, чтобы продолжить'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return database.session.get(User, int(user_id))

    api = Api(app)
    api.add_resource(ProjectResource, '/api/project/<int:id>')
    api.add_resource(ProjectsResource, '/api/projects')
    api.add_resource(PlacesResource, '/api/places')

    app.register_blueprint(main_blueprint)

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    return app


if __name__ == '__main__':
    create_app().run(host=os.environ.get('HOST', '127.0.0.1'),
                     port=int(os.environ.get('PORT', 5000)))
