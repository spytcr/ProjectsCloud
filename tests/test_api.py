def test_project_endpoint_returns_project(client, make_user, make_project):
    user = make_user()
    project = make_project(user, title='Калькулятор')

    payload = client.get(f'/api/project/{project.id}').get_json()
    assert payload['title'] == 'Калькулятор'
    assert payload['youtube'] == 'dQw4w9WgXcQ'
    assert payload['user']['name'] == 'Иван'
    assert payload['user']['place']['city']['name'] == 'Москва'


def test_project_endpoint_returns_404_for_missing_id(client):
    assert client.get('/api/project/999').status_code == 404


def test_api_never_exposes_credentials(client, make_user, make_project):
    user = make_user()
    make_project(user)

    body = client.get('/api/projects').get_data(as_text=True)
    assert 'hashed_password' not in body
    assert 'user@example.com' not in body


def test_projects_endpoint_paginates(client, make_user, make_project):
    user = make_user()
    for i in range(5):
        make_project(user, title=f'Проект {i}')

    payload = client.get('/api/projects?per_page=2').get_json()
    assert len(payload['projects']) == 2
    assert payload['total'] == 5
    assert payload['pages'] == 3


def test_projects_endpoint_caps_per_page(client, make_user, make_project):
    user = make_user()
    make_project(user)
    # Иначе клиент мог бы запросить всю таблицу одним вызовом
    payload = client.get('/api/projects?per_page=100000').get_json()
    assert payload['projects']


def test_places_endpoint_lists_places_with_cities(client):
    payload = client.get('/api/places').get_json()
    names = {place['name'] for place in payload['places']}
    assert names == {'Площадка А', 'Площадка Б'}
