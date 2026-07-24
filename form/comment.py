from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class CommentForm(FlaskForm):
    comment = TextAreaField('Оставьте комментарий', validators=[
        DataRequired(), Length(max=2000, message='Не более 2000 символов')])
    submit = SubmitField('Отправить')
