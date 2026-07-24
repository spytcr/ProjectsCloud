from model import User, database


def test_register_creates_user_and_hashes_password(client):
    response = client.post('/register', data={
        'name': 'Пётр', 'surname': 'Петров', 'place': '1',
        'email': 'new@example.com',
        'password': 'password123', 'password_again': 'password123',
    }, follow_redirects=True)

    assert response.status_code == 200
    user = database.session.query(User).filter(User.email == 'new@example.com').one()
    assert user.hashed_password != 'password123'
    assert user.check_password('password123')


def test_register_rejects_mismatched_passwords(client):
    client.post('/register', data={
        'name': 'Пётр', 'surname': 'Петров', 'place': '1',
        'email': 'new@example.com',
        'password': 'password123', 'password_again': 'other-password',
    })
    assert database.session.query(User).count() == 0


def test_register_rejects_short_password(client):
    client.post('/register', data={
        'name': 'Пётр', 'surname': 'Петров', 'place': '1',
        'email': 'new@example.com', 'password': 'short', 'password_again': 'short',
    })
    assert database.session.query(User).count() == 0


def test_register_rejects_duplicate_email(client, make_user):
    make_user(email='taken@example.com')
    client.post('/register', data={
        'name': 'Пётр', 'surname': 'Петров', 'place': '1',
        'email': 'taken@example.com',
        'password': 'password123', 'password_again': 'password123',
    })
    assert database.session.query(User).filter(User.email == 'taken@example.com').count() == 1


def test_login_with_wrong_password_does_not_authenticate(client, make_user):
    make_user()
    response = client.post('/login', data={
        'email': 'user@example.com', 'password': 'wrong-password'},
        follow_redirects=True)
    assert 'Неверный e-mail или пароль' in response.get_data(as_text=True)


def test_login_then_profile_is_accessible(client, make_user, login):
    make_user()
    login()
    assert client.get('/profile').status_code == 200


def test_profile_requires_authentication(client):
    response = client.get('/profile')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']


def test_logout_rejects_get(client, make_user, login):
    make_user()
    login()
    # Выход меняет состояние сессии, поэтому доступен только по POST
    assert client.get('/logout').status_code == 405
