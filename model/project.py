from .db_session import database
import datetime


class Project(database.Model):
    __tablename__ = 'projects'
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    title = database.Column(database.String, nullable=False)
    description = database.Column(database.String, nullable=False)
    video = database.Column(database.String, nullable=False)
    github = database.Column(database.String, nullable=False)
    category_id = database.Column(database.Integer, database.ForeignKey('categories.id'), nullable=True)
    category = database.relationship('Category')
    user_id = database.Column(database.Integer, database.ForeignKey('users.id', ondelete='CASCADE',
                                                                    onupdate='CASCADE'), nullable=False)
    user = database.relationship('User')
    comments = database.relationship('Comment')
    created_time = database.Column(database.DateTime, default=datetime.datetime.now)
