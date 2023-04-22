from sqlalchemy_serializer import SerializerMixin
from .db_session import database


class Place(database.Model, SerializerMixin):
    __tablename__ = 'places'
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    name = database.Column(database.String, nullable=False)
    city_id = database.Column(database.Integer, database.ForeignKey('cities.id', ondelete='CASCADE',
                                                                    onupdate='CASCADE'), nullable=False)
    city = database.relationship('City')
