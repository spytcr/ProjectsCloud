class DebugConfig:
    DEBUG = True
    SECRET_KEY = 'secretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite?check_same_thread=False'
