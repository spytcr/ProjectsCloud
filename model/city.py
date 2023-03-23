from .db_session import database


class City(database.Model):
    __tablename__ = 'cities'
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    name = database.Column(database.String, nullable=False)
