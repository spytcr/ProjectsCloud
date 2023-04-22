from sqlalchemy_serializer import SerializerMixin
from .db_session import database


class Category(database.Model, SerializerMixin):
    __tablename__ = 'categories'
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    name = database.Column(database.String(255), nullable=False)
