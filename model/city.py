from sqlalchemy_serializer import SerializerMixin

from .db_session import database


class City(database.Model, SerializerMixin):
    __tablename__ = 'cities'
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    name = database.Column(database.String, nullable=False)
    places = database.relationship('Place', back_populates='city')
