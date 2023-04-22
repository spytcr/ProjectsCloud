from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, ValidationError, Regexp
import re
from model.project import YOUTUBE_REGEX, GITHUB_REGEX


class ProjectForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    youtube = URLField('Ссылка на youtube видео', validators=[
        DataRequired(), Regexp(YOUTUBE_REGEX, message='Неверный формат ссылки')])
    github = URLField('Ссылка на github репозиторий', validators=[
        DataRequired(), Regexp(GITHUB_REGEX, message='Неверный формат ссылки')])
    category = SelectField('Категория', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
