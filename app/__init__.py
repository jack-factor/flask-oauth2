from flask import Flask
from flask_oauthlib.provider import OAuth2Provider
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS',
                                      'app.config.DevelopmentConfig'))
oauth = OAuth2Provider(app)
db = SQLAlchemy(app)


from app.api import mod_oauth


app.register_blueprint(mod_oauth)


if(__name__ == 'app'):
    db.init_app(app)
    with app.app_context():
        # crea las tablas que no existen
        db.create_all()
