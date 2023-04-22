from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import database
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(database.Model, UserMixin, SerializerMixin):
    __tablename__ = 'users'
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    name = database.Column(database.String(255), nullable=False)
    surname = database.Column(database.String(255), nullable=False)
    place_id = database.Column(database.Integer, database.ForeignKey('places.id'), nullable=False)
    place = database.relationship('Place')
    email = database.Column(database.String(255), nullable=False, index=True, unique=True)
    hashed_password = database.Column(database.String(255), nullable=False)
    created_time = database.Column(database.DateTime, default=datetime.datetime.now)
    projects = database.relationship('Project', back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
