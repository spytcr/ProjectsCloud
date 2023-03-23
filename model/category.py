from .db_session import database


class Category(database.Model):
    __tablename__ = 'categories'
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    name = database.Column(database.String, nullable=False)
