from .db_session import database
import datetime


class Comment(database.Model):
    __tablename__ = 'comments'
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    text = database.Column(database.String, nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id', ondelete='CASCADE',
                                                                    onupdate='CASCADE'), nullable=False)
    user = database.relationship('User')
    project_id = database.Column(database.Integer, database.ForeignKey('projects.id', ondelete='CASCADE',
                                                                       onupdate='CASCADE'), nullable=False)
    created_time = database.Column(database.DateTime, default=datetime.datetime.now)
