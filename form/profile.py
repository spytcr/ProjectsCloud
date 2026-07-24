from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class ProfileForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(max=255)])
    surname = StringField('Фамилия', validators=[DataRequired(), Length(max=255)])
    place = SelectField('Площадка', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
