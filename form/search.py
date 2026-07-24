from flask_wtf import FlaskForm
from wtforms import SubmitField, SearchField, SelectMultipleField


class SearchForm(FlaskForm):
    """Форма поиска отправляется через GET, поэтому результаты — ссылка,
    которой можно поделиться. CSRF-токен здесь не нужен: запрос ничего не меняет."""

    class Meta:
        csrf = False

    category = SelectMultipleField('Категория проекта', validate_choice=False)
    place = SelectMultipleField('Площадка', validate_choice=False)
    query = SearchField('Введите запрос')
    submit = SubmitField('Найти')
