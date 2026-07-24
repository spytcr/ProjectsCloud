def test_search_filters_by_place(client, make_user, make_project):
    """Регрессия: фильтр сравнивал place.id с User.id и возвращал произвольные проекты."""
    moscow_user = make_user(email='moscow@example.com', place_id=1)
    kazan_user = make_user(email='kazan@example.com', place_id=2)
    make_project(moscow_user, title='Московский проект')
    make_project(kazan_user, title='Казанский проект')

    page = client.get('/projects?place=2').get_data(as_text=True)
    assert 'Казанский проект' in page
    assert 'Московский проект' not in page


def test_search_filters_by_category(client, make_user, make_project):
    user = make_user()
    make_project(user, title='Веб-проект', category_id=1)
    make_project(user, title='Игра', category_id=2)

    page = client.get('/projects?category=2').get_data(as_text=True)
    assert 'Игра' in page
    assert 'Веб-проект' not in page


def test_search_filters_by_title_case_insensitively(client, make_user, make_project):
    user = make_user()
    make_project(user, title='Калькулятор')
    make_project(user, title='Мессенджер')

    page = client.get('/projects?query=калькул').get_data(as_text=True)
    assert 'Калькулятор' in page
    assert 'Мессенджер' not in page


def test_search_combines_filters(client, make_user, make_project):
    moscow_user = make_user(email='moscow@example.com', place_id=1)
    kazan_user = make_user(email='kazan@example.com', place_id=2)
    make_project(moscow_user, title='Бот', category_id=1)
    make_project(kazan_user, title='Бот', category_id=1)
    make_project(kazan_user, title='Игра', category_id=2)

    page = client.get('/projects?place=2&category=1&query=бот').get_data(as_text=True)
    assert 'Бот' in page
    assert 'Игра' not in page


def test_search_ignores_non_numeric_filter_values(client, make_user, make_project):
    user = make_user()
    make_project(user, title='Калькулятор')
    # Значения приходят из query-строки, подделать их тривиально
    response = client.get('/projects?place=не-число&category=;DROP TABLE projects')
    assert response.status_code == 200
    assert 'Калькулятор' in response.get_data(as_text=True)


def test_catalog_paginates(client, make_user, make_project, app):
    user = make_user()
    for i in range(app.config['PROJECTS_PER_PAGE'] + 3):
        make_project(user, title=f'Проект {i}')

    first_page = client.get('/projects').get_data(as_text=True)
    second_page = client.get('/projects?page=2').get_data(as_text=True)
    assert first_page.count('card-img-top') == app.config['PROJECTS_PER_PAGE']
    assert second_page.count('card-img-top') == 3
