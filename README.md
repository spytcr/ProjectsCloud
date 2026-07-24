# Projects Cloud

<img src="static/img/logo.png" alt="Projects Cloud" width="80">

Веб-платформа для публикации и обсуждения учебных проектов: автор загружает описание,
видео-демонстрацию и ссылку на репозиторий, а остальные пользователи ищут проекты по
категории и региону, смотрят их и оставляют комментарии.

Идея выросла из практической проблемы: работы учащихся расходятся по личным репозиториям
и чатам, и найти, что делали ребята с других площадок, невозможно. Projects Cloud
собирает их в одном каталоге с поиском.

**Стек:** Python · Flask · SQLAlchemy · Flask-Login · Flask-RESTful · Jinja2 · Bootstrap 5 · SQLite

---

## Возможности

| | |
|---|---|
| **Каталог проектов** | Карточки с автоподтягиванием превью из YouTube, автор, категория, дата, постраничная навигация |
| **Поиск и фильтры** | Поиск по названию без учёта регистра + мультифильтр по категориям и площадкам (153 города, 320 площадок в предзаполненном справочнике); состояние поиска живёт в URL |
| **Аккаунты** | Регистрация, вход, сессии «запомнить меня», редактирование профиля |
| **CRUD проектов** | Создание, редактирование и удаление — только владельцем записи |
| **Комментарии** | Обсуждение под проектом с удалением собственных комментариев |
| **REST API** | Публичная выдача каталога и справочника площадок в JSON |

## Архитектура

```
main.py              — фабрика приложения, маршруты и регистрация ресурсов API
config.py            — конфигурации для разработки и production
seed.py              — идемпотентное наполнение справочников
model/               — модели SQLAlchemy (User, Project, Comment, Category, City, Place)
form/                — формы WTForms с валидацией
resources/           — ресурсы Flask-RESTful (JSON API)
templates/           — шаблоны Jinja2, наследуемые от base.html
static/              — стили и статика
data/seed.json       — справочник городов и площадок
tests/               — тесты pytest
```

Приложение собирается фабрикой `create_app(config)`: тесты поднимают его с базой
в памяти, не трогая рабочую, а окружение выбирается переменной `FLASK_ENV`.

Слои разделены по назначению: модели не знают о формах, формы — о маршрутах, а API
переиспользует те же модели, что и серверный рендеринг. Сериализация в JSON вынесена в
`SerializerMixin` с явным белым списком полей, чтобы хеши паролей и e-mail не попадали
в ответ.

### Модель данных

```
City ──< Place ──< User ──< Project >── Category
                    │         │
                    └──< Comment >─┘
```

Пользователь привязан к площадке, площадка — к городу; это позволяет фильтровать каталог
по географии одним join'ом, не денормализуя данные.

## REST API

| Метод | Эндпоинт | Описание |
|---|---|---|
| `GET` | `/api/projects` | Каталог с постраничной выдачей (`?page=`, `?per_page=`, максимум 100) |
| `GET` | `/api/project/<id>` | Один проект, `404` если не найден |
| `GET` | `/api/places` | Справочник площадок с городами |

```bash
curl http://localhost:5000/api/project/1
```

```json
{
  "title": "Projects Cloud",
  "description": "Платформа для публикации учебных проектов",
  "youtube": "dQw4w9WgXcQ",
  "github": "https://github.com/spytcr/ProjectsCloud",
  "category": {"name": "Веб-разработка"},
  "user": {"name": "Александр", "surname": "Иванов",
           "place": {"name": "Школа №1", "city": {"name": "Москва"}}},
  "created_time": "2023-04-22T16:50:06"
}
```

## Запуск

```bash
git clone https://github.com/spytcr/ProjectsCloud.git
cd ProjectsCloud

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python seed.py                  # справочник: 3 категории, 153 города, 320 площадок
python main.py
```

Приложение поднимется на http://localhost:5000 (порт переопределяется переменной `PORT`).
Схема создаётся автоматически при старте, `seed.py` идемпотентен — повторный запуск
не плодит дубликатов.

### Production

Конфигурация читается из окружения, шаблон — в [`.env.example`](.env.example):

```bash
export FLASK_ENV=production
export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
export DATABASE_URI=postgresql+psycopg2://user:password@localhost/projectscloud
```

`ProductionConfig` отказывается стартовать без `SECRET_KEY` и включает `Secure`,
`HttpOnly` и `SameSite` для сессионной куки.

## Тесты

```bash
pip install -r requirements-dev.txt
pytest
```

47 тестов на базе в памяти покрывают регистрацию и вход, разграничение доступа
(чужой проект нельзя ни открыть на редактирование, ни удалить), защиту от CSRF,
все фильтры каталога, пагинацию, нормализацию ссылок и контракт REST API —
включая проверку, что в выдачу не попадают e-mail и хеши паролей.

## Стек

| Слой | Технологии |
|---|---|
| Backend | Python 3, Flask 2.2 |
| ORM | SQLAlchemy 2.0, Flask-SQLAlchemy |
| Аутентификация | Flask-Login, Werkzeug Security |
| Формы и валидация | Flask-WTF, WTForms |
| API | Flask-RESTful, SQLAlchemy-Serializer |
| Frontend | Jinja2, Bootstrap 5, bootstrap-select, jQuery |
| БД | SQLite (совместимо с PostgreSQL) |
| Тесты | pytest |
