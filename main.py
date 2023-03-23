from flask import Flask
from model import *

app = Flask(__name__)
app.config.from_object(app.config.from_object('config.DebugConfig'))

database.init_app(app)
with app.app_context():
    database.create_all()


if __name__ == '__main__':
    app.run()

