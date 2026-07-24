from model import Comment, Project, User, database


def test_owner_can_edit_own_project(client, make_user, make_project, login):
    user = make_user()
    project = make_project(user)
    login()
    client.post(f'/edit/{project.id}', data={
        'title': 'Новое название', 'description': 'Описание',
        'youtube': 'https://youtu.be/dQw4w9WgXcQ',
        'github': 'https://github.com/user/repo', 'category': '1',
    })
    assert database.session.get(Project, project.id).title == 'Новое название'


def test_stranger_cannot_edit_foreign_project(client, make_user, make_project, login):
    owner = make_user(email='owner@example.com')
    project = make_project(owner)
    make_user(email='stranger@example.com')
    login(email='stranger@example.com')

    assert client.get(f'/edit/{project.id}').status_code == 404
    response = client.post(f'/edit/{project.id}', data={
        'title': 'Взломано', 'description': 'x',
        'youtube': 'https://youtu.be/dQw4w9WgXcQ',
        'github': 'https://github.com/user/repo', 'category': '1',
    })
    assert response.status_code == 404
    assert database.session.get(Project, project.id).title == 'Проект'


def test_stranger_cannot_delete_foreign_project(client, make_user, make_project, login):
    owner = make_user(email='owner@example.com')
    project = make_project(owner)
    make_user(email='stranger@example.com')
    login(email='stranger@example.com')

    assert client.post(f'/delete/{project.id}').status_code == 404
    assert database.session.get(Project, project.id) is not None


def test_delete_rejects_get_request(client, make_user, make_project, login):
    user = make_user()
    project = make_project(user)
    login()
    # Удаление по GET-ссылке обходило бы CSRF-защиту и срабатывало от префетча браузера
    assert client.get(f'/delete/{project.id}').status_code == 405
    assert database.session.get(Project, project.id) is not None


def test_owner_can_delete_own_project(client, make_user, make_project, login):
    user = make_user()
    project = make_project(user)
    login()
    client.post(f'/delete/{project.id}', follow_redirects=True)
    assert database.session.get(Project, project.id) is None


def test_delete_without_csrf_token_is_rejected(csrf_app):
    """Мутации без формы защищены только глобальным CSRFProtect, а не FlaskForm."""
    user = User(name='Иван', surname='Иванов', email='user@example.com', place_id=1)
    user.set_password('password123')
    database.session.add(user)
    database.session.commit()
    project = Project(title='Проект', description='Описание', youtube='dQw4w9WgXcQ',
                      github='https://github.com/user/repo', category_id=1, user_id=user.id)
    database.session.add(project)
    database.session.commit()

    client = csrf_app.test_client()
    with client.session_transaction() as session:
        session['_user_id'] = str(user.id)

    response = client.post(f'/delete/{project.id}')
    assert response.status_code == 400
    assert database.session.get(Project, project.id) is not None


def test_comment_author_can_delete_only_own_comment(client, make_user, make_project, login):
    owner = make_user(email='owner@example.com')
    project = make_project(owner)
    stranger = make_user(email='stranger@example.com')
    comment = Comment(text='Комментарий', user_id=owner.id, project_id=project.id)
    database.session.add(comment)
    database.session.commit()

    login(email='stranger@example.com')
    response = client.post(f'/comment/{project.id}/delete/{comment.id}')
    assert response.status_code == 404
    assert database.session.get(Comment, comment.id) is not None


def test_project_page_returns_404_for_missing_project(client):
    assert client.get('/project/999').status_code == 404
