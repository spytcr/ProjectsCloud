from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    place = SelectField('Площадка', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
