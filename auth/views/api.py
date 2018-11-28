import json
import logging

from flask import current_app as app
from flask import jsonify, request
from flask.views import MethodView
from werkzeug.exceptions import abort

from auth import db
from auth.models import User

logger = logging.getLogger(__name__)


class AuthAPI(MethodView):
    def __init__(self):
        self.uuid = None

    def get(self, **kwargs):
        """"
        Return an access token for uuid user, given an application uuid.
        """
        print(dir(kwargs.values))
        uuid = kwargs.get('uuid', 200)
        application_uuid = kwargs.get('application_uuid', 300)
        teste = kwargs.get('teste', 400)
        return jsonify([uuid, application_uuid, teste])

    def post(self, uuid, password, app_uuid):

        """"
        Create new user given uuid, password and application uuid.
        Return an access token
        """
        return app_uuid

