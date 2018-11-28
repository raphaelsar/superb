import logging
import os


class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    LOGS_LEVEL = logging.INFO

    TIMEZONE = os.environ.get('TIMEZONE', 'America/Sao_Paulo')
    SENTRY_DSN = os.environ.get('SENTRY_DSN')
    BUCKET_NAME = os.environ.get('BUCKET_NAME', 'apoena-staging')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    # set to True if use signals
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    LOGS_LEVEL = logging.CRITICAL
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/apoena-document-service'


class StagingConfig(Config):
    pass


class ProductionConfig(Config):
    LOGS_LEVEL = logging.ERROR