from auth import db

from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    uuid = db.Column(db.String(32), primary_key=True, autoincrement=False)
    password = db.Column(db.String(32), index=True, nullable=False)
    token = db.Column(db.String(32), index=True, nullable=False)
    ip = db.Column(db.String(15), nullable=False)

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'password': self.password,
            'token': self.token,
            'ip': self.ip,
        }

    def __str__(self):
        return '{}/{}'.format(self.uuid, self.token)
