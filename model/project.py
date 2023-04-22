from sqlalchemy_serializer import SerializerMixin
from .db_session import database
import datetime
import re

YOUTUBE_REGEX = r'https://(?:youtu\.be/|(?:[a-z]{2,3}\.)?youtube\.com/watch(?:\?|#!)v=)([\w-]{11}).*'
GITHUB_REGEX = r'https://github\.com/\w*/\w*'


class Project(database.Model, SerializerMixin):
    __tablename__ = 'projects'
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    title = database.Column(database.String, nullable=False)
    description = database.Column(database.String, nullable=False)
    youtube = database.Column(database.String, nullable=False)
    github = database.Column(database.String, nullable=False)
    category_id = database.Column(database.Integer, database.ForeignKey('categories.id'), nullable=False)
    category = database.relationship('Category')
    user_id = database.Column(database.Integer, database.ForeignKey('users.id', ondelete='CASCADE',
                                                                    onupdate='CASCADE'), nullable=False)
    user = database.relationship('User')
    comments = database.relationship('Comment')
    created_time = database.Column(database.DateTime, default=datetime.datetime.now)

    def set_youtube(self, youtube):
        self.youtube = re.match(YOUTUBE_REGEX, youtube)[1]

    def get_youtube(self):
        return 'https://youtu.be/' + self.youtube
