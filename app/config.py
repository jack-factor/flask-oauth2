# -*- coding: utf-8 -*-
import os


class BaseConfig(object):
    'Base config class'

    SECRET_KEY = 'A random secret key'
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    'Development environment specific config'

    DEBUG = True
    TESTING = True
    SECRET_KEY = 'Another random secret key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///test.sqlite')
