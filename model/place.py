from .db_session import database


class Place(database.Model):
    __tablename__ = 'places'
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    name = database.Column(database.String, nullable=False)
    link = database.Column(database.String, nullable=False)
    city_id = database.Column(database.Integer, database.ForeignKey('cities.id'), nullable=True)
    city = database.relationship('City')
