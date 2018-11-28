import logging
import logging.config
import os
import unittest

from flask import Flask, Response, json
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)
db = SQLAlchemy()
migrate = Migrate()


def generic_api_error(e):
    resp = json.dumps({"error": {"status": "",
                                 "title": "",
                                 "code": getattr(e, 'api_code', 'UNDEFINED'),
                                 "message": ""
                                 }})

    response = Response(resp, status=e.code, mimetype='application/json')
    response.cache_control.private = True
    response.cache_control.must_revalidate = True
    return response


def install_error_handlers(error_codes, blueprint):
    for code in error_codes:
        blueprint.errorhandler(code)(generic_api_error)


def create_app(config_var=os.getenv('DEPLOY_ENV', 'Development')):
    """
    Create and configure app flask
    :param config_var: enviroment for app (Development, Staging, Production, Testing)
    :return: app flask
    """
    app = Flask(__name__)

    app.config.from_object('auth.config.%sConfig' % config_var)

    db.init_app(app)
    migrate.init_app(app, db, directory=os.path.join(app.config['BASE_DIR'], 'migrations'))

    __configure_logger(app)

    from .routes import api
    app.register_blueprint(api)

    import auth.models

    error_codes = [400, 401, 403, 404, 405, 406, 408, 409, 410, 412, 415, 428, 429, 500, 501]
    install_error_handlers(error_codes, app)

    return app


def __configure_logger(app):
    logger_settings = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '[%(asctime)s][%(levelname)s] %(name)s '
                          '%(filename)s:%(funcName)s:%(lineno)d | %(message)s',
                'datefmt': '%H:%M:%S'
            },
        },
        'handlers': {
            'default': {
                'level': app.config['LOGS_LEVEL'],
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stderr'
            },
            # 'sentry': {
            #     'level': 'WARNING',
            #     'class': 'raven.handlers.logging.SentryHandler',
            #     'dsn': app.config['SENTRY_DSN'],
            # },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': app.config['LOGS_LEVEL'],
                'propagate': True
            }
        }
    }

    logging.config.dictConfig(logger_settings)


class BaseTestCase(unittest.TestCase):
    logger.disabled = True
    maxDiff = None

    def create_app(self):
        app = create_app('Testing')
        app.app_context().push()
        return app

    def setUp(self):
        """ Before each test, set up a blank database """
        self.app = self.create_app()
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        """ Get rid of the database again after each test. """
        with self.app.app_context():
            db.drop_all()
            db.session.rollback()
