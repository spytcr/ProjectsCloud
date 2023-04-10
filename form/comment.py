from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    comment = StringField('Оставьте комментарий', validators=[DataRequired()])
    submit = SubmitField('Отправить')
