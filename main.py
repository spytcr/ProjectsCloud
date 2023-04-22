from flask import Flask, redirect, render_template, abort
from flask_restful import Api

from form.comment import CommentForm
from form.login import LoginForm
from form.profile import ProfileForm
from form.project import ProjectForm
from form.register import RegisterForm
from form.search import SearchForm
from model import *
from flask import request
from flask_login import LoginManager, login_required, logout_user, login_user, current_user

from resources.place import PlacesResource
from resources.project import ProjectResource, ProjectsResource

app = Flask(__name__)

database.init_app(app)
with app.app_context():
    database.create_all()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return database.session.query(User).get(user_id)


api = Api(app)
api.add_resource(ProjectResource, '/api/project/<int:id>')
api.add_resource(ProjectsResource, '/api/projects')
api.add_resource(PlacesResource, '/api/places')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        abort(404)
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
        abort(404)
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


@app.route('/projects', methods=['GET', 'POST'])
def projects():
    form = SearchForm()
    form.category.choices = [(category.id, category.name)
                             for category in database.session.query(Category).all()]
    form.place.choices = {city.name: [(place.id, place.name) for place in city.places]
                          for city in database.session.query(City).all()}
    if form.validate_on_submit():
        projects = database.session.query(Project).join(Project.user).filter(
            Project.title.ilike(f'%{form.query.data.lower()}%'),
            not form.category.data or Project.category_id.in_(form.category.data),
            not form.place.data or User.id.in_(form.place.data)).all()
    else:
        projects = database.session.query(Project).all()
    return render_template('projects.html', form=form, projects=projects)


@app.route('/project/<int:id>')
def project(id):
    project = database.session.query(Project).filter(Project.id == id).first()
    if not project:
        abort(404)
    comment_form = CommentForm()
    comments = database.session.query(Comment).filter(Comment.project_id == id).all()
    return render_template('project.html', project=project, comment_form=comment_form, comments=comments)


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_project():
    form = ProjectForm()
    form.category.choices = [(category.id, category.name)
                             for category in database.session.query(Category).all()]
    if form.validate_on_submit():
        project = Project(
            title=form.title.data,
            description=form.description.data,
            github=form.github.data,
            category_id=form.category.data,
            user_id=current_user.id
        )
        project.set_youtube(form.youtube.data)
        database.session.add(project)
        database.session.commit()
        return redirect('/')
    return render_template('edit.html', form=form)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = database.session.query(Project).filter(Project.id == id, Project.user == current_user).first()
    if not project:
        abort(404)
    form = ProjectForm()
    form.category.choices = [(category.id, category.name)
                             for category in database.session.query(Category).all()]
    if request.method == 'GET':
        form.title.data = project.title
        form.description.data = project.description
        form.youtube.data = project.get_youtube()
        form.github.data = project.github
        form.category.default = project.category_id
        form.category.process([])
    elif form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data
        project.set_youtube(form.youtube.data)
        project.github = form.github.data
        project.category_id = form.category.data
        database.session.commit()
        return redirect(f'/project/{id}')
    return render_template('edit.html', form=form)


@app.route('/delete/<int:id>')
@login_required
def delete_project(id):
    project = database.session.query(Project).filter(Project.id == id, Project.user == current_user).first()
    if project:
        database.session.delete(project)
        database.session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/comment/<int:id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    project = database.session.query(Project).filter(Project.id == id).first()
    if not project:
        abort(404)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            text=form.comment.data,
            user_id=current_user.id,
            project_id=project.id
        )
        database.session.add(comment)
        database.session.commit()
    return redirect(f'/project/{id}#comments')


@app.route('/comment/<int:project_id>/delete/<int:comment_id>')
@login_required
def comment_delete(project_id, comment_id):
    comment = database.session.query(Comment).filter(
        Comment.project_id == project_id, Comment.id == comment_id, Comment.user == current_user).first()
    if comment:
        database.session.delete(comment)
        database.session.commit()
    else:
        abort(404)
    return redirect(f'/project/{project_id}#comments')


if __name__ == '__main__':
    app.config.from_object(app.config.from_object('config.DebugConfig'))
    app.run()
