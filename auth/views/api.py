import json
import logging
from flask import current_app as app
from flask import jsonify, request
from flask.views import MethodView
from werkzeug.exceptions import abort
from auth import db
from auth.models import User
import md5

logger = logging.getLogger(__name__)


class AuthAPI(MethodView):
    def __init__(self):
        self.uuid = None

    def get(self, **kwargs):
        """"
        Return an access token for uuid user, given an application uuid.
        """

        uuid = kwargs.get('uuid', None)
        application_uuid = kwargs.get('application_uuid', None)

        if uuid is None:
            # gerar token anonimo
            return application_uuid

        #gerar token com as infos do usuário



        return jsonify([uuid, application_uuid])

    def post(self, **kwargs):
        """"
        Create new user given uuid, password and application uuid.
        Return an access token
        """
        password = md5.new(request.values.get('password')).digest()
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

        user = User(kwargs);


        return 'a'

