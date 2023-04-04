from flask import Flask, redirect, render_template
from model import *
from flask import request
from flask_login import LoginManager, login_required, logout_user

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
    pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    pass


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
