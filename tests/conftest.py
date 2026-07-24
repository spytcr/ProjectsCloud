import pytest

from main import create_app
from model import Category, City, Comment, Place, Project, User, database


class TestConfig:
    TESTING = True
    SECRET_KEY = 'test-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite://'  # in-memory, своя база на каждый тест
    PROJECTS_PER_PAGE = 12
    WTF_CSRF_ENABLED = False


class CsrfConfig(TestConfig):
    WTF_CSRF_ENABLED = True


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        _seed_reference_data()
        yield app
        database.session.remove()
        database.drop_all()


@pytest.fixture
def csrf_app():
    app = create_app(CsrfConfig)
    with app.app_context():
        _seed_reference_data()
        yield app
        database.session.remove()
        database.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def _seed_reference_data():
    moscow = City(name='Москва')
    kazan = City(name='Казань')
    database.session.add_all([moscow, kazan])
    database.session.flush()
    database.session.add_all([
        Place(name='Площадка А', city_id=moscow.id),
        Place(name='Площадка Б', city_id=kazan.id),
        Category(name='Flask'),
        Category(name='Pygame'),
    ])
    database.session.commit()


@pytest.fixture
def make_user(app):
    def _make(email='user@example.com', password='password123', place_id=1):
        user = User(name='Иван', surname='Иванов', email=email, place_id=place_id)
        user.set_password(password)
        database.session.add(user)
        database.session.commit()
        return user
    return _make


@pytest.fixture
def make_project(app):
    def _make(user, title='Проект', category_id=1, youtube='https://youtu.be/dQw4w9WgXcQ'):
        project = Project(
            title=title,
            description='Описание',
            github='https://github.com/user/repo',
            category_id=category_id,
            user_id=user.id,
        )
        project.set_youtube(youtube)
        database.session.add(project)
        database.session.commit()
        return project
    return _make


@pytest.fixture
def login(client):
    def _login(email='user@example.com', password='password123'):
        return client.post('/login', data={'email': email, 'password': password},
                           follow_redirects=True)
    return _login
