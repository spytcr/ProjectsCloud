from flask import (Blueprint, abort, current_app, flash, redirect,
                   render_template, request, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from form.comment import CommentForm
from form.login import LoginForm
from form.profile import ProfileForm
from form.project import ProjectForm
from form.register import RegisterForm
from form.search import SearchForm
from model import Category, City, Comment, Project, User, database

main = Blueprint('main', __name__)


def _int_list(values):
    result = []
    for value in values or ():
        try:
            result.append(int(value))
        except (TypeError, ValueError):
            continue
    return result


def _place_choices():
    return {city.name: [(place.id, place.name) for place in city.places]
            for city in database.session.query(City).order_by(City.name).all()}


def _category_choices():
    return [(category.id, category.name)
            for category in database.session.query(Category).order_by(Category.name).all()]


@main.app_template_global()
def page_url(page):
    args = request.args.to_dict(flat=False)
    args['page'] = page
    return url_for('main.projects', **args)


@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.projects'))
    form = RegisterForm()
    form.place.choices = _place_choices()
    if form.validate_on_submit():
        if database.session.query(User).filter(User.email == form.email.data).first():
            flash('Пользователь с такой почтой уже существует', 'danger')
            return render_template('register.html', form=form)
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            place_id=form.place.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        database.session.add(user)
        database.session.commit()
        flash('Регистрация завершена, теперь можно войти', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.projects'))
    form = LoginForm()
    if form.validate_on_submit():
        user = database.session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('main.projects'))
        flash('Неверный e-mail или пароль', 'danger')
    return render_template('login.html', form=form)


@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    form.place.choices = _place_choices()
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
        flash('Профиль обновлён', 'success')
        return redirect(url_for('main.projects'))
    return render_template('profile.html', form=form)


@main.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.projects'))


@main.route('/')
def index():
    return redirect(url_for('main.projects'))


@main.route('/projects')
def projects():
    form = SearchForm(request.args)
    form.category.choices = _category_choices()
    form.place.choices = _place_choices()

    conditions = []
    if form.query.data:
        conditions.append(func.lower(Project.title).like(f'%{form.query.data.lower()}%'))
    categories = _int_list(form.category.data)
    if categories:
        conditions.append(Project.category_id.in_(categories))
    places = _int_list(form.place.data)
    if places:
        conditions.append(User.place_id.in_(places))

    statement = (
        select(Project)
        .join(Project.user)
        .where(*conditions)
        .order_by(Project.created_time.desc())
        .options(
            joinedload(Project.category),
            joinedload(Project.user).joinedload(User.place),
        )
    )
    pagination = database.paginate(
        statement, per_page=current_app.config['PROJECTS_PER_PAGE'], error_out=False)
    return render_template('projects.html', form=form, pagination=pagination,
                           projects=pagination.items)


@main.route('/project/<int:id>')
def project(id):
    project = database.session.get(Project, id)
    if not project:
        abort(404)
    comments = (database.session.query(Comment)
                .filter(Comment.project_id == id)
                .options(joinedload(Comment.user))
                .order_by(Comment.created_time.desc())
                .all())
    return render_template('project.html', project=project,
                           comment_form=CommentForm(), comments=comments)


@main.route('/create', methods=['GET', 'POST'])
@login_required
def create_project():
    form = ProjectForm()
    form.category.choices = _category_choices()
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
        return redirect(url_for('main.project', id=project.id))
    return render_template('edit.html', form=form)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    # Проверка владельца встроена в сам запрос, а не выполняется отдельным if
    # после выборки: чужая запись просто не находится.
    project = database.session.query(Project).filter(
        Project.id == id, Project.user_id == current_user.id).first()
    if not project:
        abort(404)
    form = ProjectForm()
    form.category.choices = _category_choices()
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
        return redirect(url_for('main.project', id=id))
    return render_template('edit.html', form=form)


@main.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_project(id):
    project = database.session.query(Project).filter(
        Project.id == id, Project.user_id == current_user.id).first()
    if not project:
        abort(404)
    database.session.delete(project)
    database.session.commit()
    flash('Проект удалён', 'success')
    return redirect(url_for('main.projects'))


@main.route('/comment/<int:id>', methods=['POST'])
@login_required
def comment(id):
    project = database.session.get(Project, id)
    if not project:
        abort(404)
    form = CommentForm()
    if form.validate_on_submit():
        database.session.add(Comment(
            text=form.comment.data,
            user_id=current_user.id,
            project_id=project.id
        ))
        database.session.commit()
    else:
        flash('Комментарий не сохранён: ' + '; '.join(form.comment.errors), 'danger')
    return redirect(url_for('main.project', id=id) + '#comments')


@main.route('/comment/<int:project_id>/delete/<int:comment_id>', methods=['POST'])
@login_required
def comment_delete(project_id, comment_id):
    comment = database.session.query(Comment).filter(
        Comment.project_id == project_id,
        Comment.id == comment_id,
        Comment.user_id == current_user.id).first()
    if not comment:
        abort(404)
    database.session.delete(comment)
    database.session.commit()
    return redirect(url_for('main.project', id=project_id) + '#comments')
