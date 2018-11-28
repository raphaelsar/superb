import os
import uuid
import redis
import tornado.ioloop
import tornado.options
from tornado.web import RequestHandler, Application
from  tornado.httpserver import HTTPServer
from tornado.options import define, options
from sqlalchemy import Column, Integer, String
from tornado_sqlalchemy import SessionMixin, as_future, declarative_base, make_session_factory

auth_port = os.getenv("AUTH_PORT", 8888)
redis_host = os.getenv("REDIS_HOST", "127.0.0.1")
redis_port = os.getenv("REDIS_PORT", "6379")
debug = os.getenv("ENV", "DEV") == "DEV"

mysql_host = os.getenv("MYLSQ_HOST", "127.0.0.1")
mysql_port = os.getenv("MYSQL_PORT", "3306")
mysql_user = os.getenv("MYSQL_USER", "auth_app")
mysql_pwd = os.getenv("MYSQL_PWD", "WMNSnKmaCYbeLzba")
mysql_scheme = os.getenv("MYSQL_SCHEME", "auth")

mysql_string = "mysql+mysqldb://{0}:{1}@{2}:{3}/{4}".format(
    mysql_user, mysql_pwd, mysql_host,mysql_port,mysql_scheme
)

define("port", default=auth_port, help="run on the given port", type=int)
define("redis_host", default=redis_host, help="redis host")
define("redis_port", default=redis_port, help="redis port")
define("debug", default=debug, help="redis password")
define("mysql_string", default=mysql_string, help="mysql string conn")

DeclarativeBase = declarative_base()

class MainHandler(RequestHandler):
    def get(self):
        self.write('ola')

class AppHandler(SessionMixin, RequestHandler):
    def get(self):
        self.write('app registration')

    def post(self):
        app_name = None
        app_pwd = None
        session = self.make_session()
        app_name = self.get_argument('name')
        app_pwd = self.get_argument('pwd')
        new_app = AppBase(uuid=uuid.uuid4(), name=app_name, pwd=app_pwd);
        with self.make_session as session:
            session.add(new_app)

        print (new_app.name)


class AppBase(DeclarativeBase):
    __tablename__ = "applications"
    uuid = Column(String(32), primary_key=True)
    name = Column(String(50))
    pwd = Column(String(32))


class Application(Application):
    def __init__(self, redis, session_factory, debug):
        self.redis = redis
        self.session_factory = session_factory
        handlers = [
            (r"/", MainHandler),
            (r"/application", AppHandler, )
        ]

        settings = dict(
            debug=debug,
            session_factory=session_factory,
        )

        super(Application, self).__init__(handlers, **settings)

if __name__ == "__main__":
    redis_db = redis.Redis(host=options.redis_host, port=options.redis_port, db=0)
    # redis_db = None
    session_factory=make_session_factory(options.mysql_string)
    app = Application(redis_db, session_factory, options.debug)
    server = HTTPServer(app)
    server.listen(8888)
    tornado.ioloop.IOLoop.current().start()
