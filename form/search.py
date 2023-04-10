from flask_wtf import FlaskForm
from wtforms import SubmitField, SearchField, SelectMultipleField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    category = SelectMultipleField('Категория проекта', validate_choice=False)
    place = SelectMultipleField('Площадка Яндекс лицея', validate_choice=False)
    query = SearchField('Введите запрос')
    submit = SubmitField('Найти')
