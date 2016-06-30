#coding: utf8

'''
mappings applications et utilisateurs
'''

import hashlib
import string
import random
from server import db
from sqlalchemy import func

class AppUser(db.Model):

    __tablename__ = 't_roles'
    __table_args__ = {'schema':'utilisateurs'}
    id_role = db.Column(db.Integer, primary_key=True)
    identifiant = db.Column(db.Unicode)
    nom_role = db.Column(db.Unicode)
    prenom_role = db.Column(db.Unicode)
    _password = db.Column('pass', db.Unicode)
    email = db.Column(db.Unicode)
    code_insee = db.Column(db.Integer)
    commune = db.Column(db.Unicode)
    actif = db.Column(db.Boolean)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pwd):
        self._password = hashlib.md5(pwd.encode('utf8')).hexdigest()

    def check_password(self, pwd):
        return self._password == hashlib.md5(pwd.encode('utf8')).hexdigest()

    def generate_newpassword(self) :
        newPass = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
        self._password = hashlib.md5(newPass.encode('utf8')).hexdigest()
        return newPass

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != 'pass' }


class LogSession(db.Model):
    __tablename__ = 'log_session'
    __table_args__ = {'schema':'utilisateurs'}
    id = db.Column(db.Integer, primary_key=True)
    id_role = db.Column(db.Integer)
    date_login = db.Column(db.DateTime, server_default=db.func.now())

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns }
