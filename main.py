from flask import Flask, redirect, render_template

from form.login import LoginForm
from form.profile import ProfileForm
from form.register import RegisterForm
from model import *
from flask import request
from flask_login import LoginManager, login_required, logout_user, login_user, current_user

app = Flask(__name__)
app.config.from_object(app.config.from_object('config.DebugConfig'))

database.init_app(app)
with app.app_context():
    database.create_all()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return database.session.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegisterForm()
    form.place.choices = {city.name: [(place.id, place.name) for place in city.places]
                          for city in database.session.query(City).all()}
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', form=form, message='Пароли не совпадают')
        if database.session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', form=form, message="Пользователь уже существует")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            place_id=form.place.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        database.session.add(user)
        database.session.commit()
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = database.session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', message='Неверный e-mail или пароль', form=form)
    return render_template('login.html', form=form)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    form.place.choices = {city.name: [(place.id, place.name) for place in city.places]
                          for city in database.session.query(City).all()}
    if request.method == 'GET':
        form.name.data = current_user.name
        form.surname.data = current_user.surname
        form.place.default = current_user.place_id
        form.place.process([])
    elif form.validate_on_submit():
        current_user.name = form.name.data
        current_user.surname = form.surname.data
        current_user.place_id = form.place.data
        database.session.commit()
        return redirect('/')
    return render_template('profile.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect('/projects')


@app.route('/projects')
def projects():
    if request.method == 'POST':
        title = request.form.get('title')
        categories = request.form.getlist('category')
        places = request.form.getlist('place')
        cities = request.form.getlist('city')


@app.route('/project/<int:id>')
def project(id):
    pass


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_project():
    pass


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    pass


@app.route('/comment/<int:id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    if request.method == 'POST':
        text = request.form.get('text')
    return redirect(f'/project/{id}#comments')


if __name__ == '__main__':
    app.run()
