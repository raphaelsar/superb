from auth import db

from .base import BaseModel
import enum

class TypeEnum(enum.Enum):
    user = 1
    application = 2


class User(BaseModel):
    __tablename__ = 'users'

    uuid = db.Column(db.String(32), primary_key=True, autoincrement=False)
    password = db.Column(db.String(32), index=True, nullable=False)
    token = db.Column(db.String(32), index=True, nullable=False)
    ip = db.Column(db.String(15), nullable=False)
    type = db.Column(db.Enum(TypeEnum), nullable=False)

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'password': self.password,
            'token': self.token,
            'ip': self.ip,
            'type': self.type
        }

    def __str__(self):
        return '{}/{}'.format(self.uuid, self.token)
