import os
import secrets


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///database.sqlite')
    PROJECTS_PER_PAGE = 12


class DebugConfig(Config):
    DEBUG = True
    # В разработке ключ можно не задавать: генерируем эфемерный, сессии живут до перезапуска.
    SECRET_KEY = Config.SECRET_KEY or secrets.token_hex(32)


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    def __init__(self):
        if not self.SECRET_KEY:
            raise RuntimeError(
                'Переменная окружения SECRET_KEY обязательна в production. '
                'Сгенерировать: python -c "import secrets; print(secrets.token_hex(32))"'
            )


def get_config():
    """Выбирает конфигурацию по FLASK_ENV (по умолчанию — разработка)."""
    if os.environ.get('FLASK_ENV') == 'production':
        return ProductionConfig()
    return DebugConfig()
