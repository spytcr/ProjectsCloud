"""Наполняет базу справочниками: категории, города и площадки.

Скрипт идемпотентен — повторный запуск не создаёт дубликатов, поэтому его
безопасно вызывать при каждом развёртывании.

    python seed.py
"""
import json
from pathlib import Path

from main import create_app
from model import Category, City, Place, database

SEED_FILE = Path(__file__).parent / 'data' / 'seed.json'


def seed():
    data = json.loads(SEED_FILE.read_text(encoding='utf-8'))

    existing_categories = {c.name for c in database.session.query(Category).all()}
    for name in data['categories']:
        if name not in existing_categories:
            database.session.add(Category(name=name))

    existing_cities = {c.name: c for c in database.session.query(City).all()}
    existing_places = {(p.city_id, p.name) for p in database.session.query(Place).all()}

    for city_data in data['cities']:
        city = existing_cities.get(city_data['name'])
        if city is None:
            city = City(name=city_data['name'])
            database.session.add(city)
            database.session.flush()  # нужен city.id для площадок
            existing_cities[city.name] = city
        for place_name in city_data['places']:
            if (city.id, place_name) not in existing_places:
                database.session.add(Place(name=place_name, city_id=city.id))

    database.session.commit()

    print(f'Категорий: {database.session.query(Category).count()}, '
          f'городов: {database.session.query(City).count()}, '
          f'площадок: {database.session.query(Place).count()}')


if __name__ == '__main__':
    with create_app().app_context():
        seed()
