from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(max=255)])
    surname = StringField('Фамилия', validators=[DataRequired(), Length(max=255)])
    place = SelectField('Площадка', validators=[DataRequired()])
    email = EmailField('Почта', validators=[
        DataRequired(), Email(message='Некорректный адрес почты'), Length(max=255)])
    password = PasswordField('Пароль', validators=[
        DataRequired(), Length(min=8, message='Пароль должен быть не короче 8 символов')])
    password_again = PasswordField('Повторите пароль', validators=[
        DataRequired(), EqualTo('password', message='Пароли не совпадают')])
    submit = SubmitField('Зарегистрироваться')
