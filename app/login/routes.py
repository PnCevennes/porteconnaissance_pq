#coding: utf8

'''
routes relatives aux application, utilisateurs et à l'authentification
'''

import json
import uuid
import datetime
from functools import wraps
from flask import Blueprint, Flask, request, jsonify, session, g, Response
from server import db, init_app as get_app
from . import models
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

from flask import render_template

from ..utils import send_mail

routes = Blueprint('auth', __name__)


def check_auth():
    def _check_auth(fn):
        @wraps(fn)
        def __check_auth(*args, **kwargs):
            print('check auth')
            try:
                s = Serializer(get_app().config['SECRET_KEY'])
                data = s.loads(request.cookies['token'])
            except SignatureExpired:
                print('expired')
                return Response('Token Expired', 403) # valid token, but expired
            except BadSignature:
                print('BadSignature')
                return Response('Token BadSignature', 403) # valid token, but expired
            except Exception as e:
                print('Exception')
                print(e)
                return Response('Forbidden', 403)

            return fn(*args, **kwargs)
        return __check_auth
    return _check_auth


@routes.route('/login', methods=['POST'])
def login():
    try:
        user_data = request.json

        try :
            user = models.AppUser.query\
                .filter(models.AppUser.identifiant==user_data['login'])\
                .one()
        except Exception as e:
            resp = Response(json.dumps({'type':'login', 'msg':'Identifiant invalide'}), status=490)
            return resp

        if not user.check_password(user_data['password']):
            resp = Response(json.dumps({'type':'password', 'msg':'Mot de passe invalide'}), status=490)
            return resp

        if not user.actif:
            print('Inactif')
            resp = Response(json.dumps({'type':'inactif', 'msg':'Compte non actif'}), status=490)
            return resp

        #Génération d'un token
        s = Serializer(get_app().config['SECRET_KEY'], expires_in = get_app().config['COOKIE_EXPIRATION'])
        token = s.dumps({'id_role':user.id_role})
        cookie_exp = datetime.datetime.now() + datetime.timedelta(seconds= get_app().config['COOKIE_EXPIRATION'])

        resp = Response(json.dumps({'user':user.as_dict(), 'token': token.decode('ascii'), 'expires':str(cookie_exp)}))

        resp.set_cookie('token', token, expires=cookie_exp)

        #Log de la session
        session = models.LogSession (id_role = user.id_role)

        db.session.add(session)
        db.session.commit()
        return resp
    except Exception as e:
        print(e)
        resp = Response(json.dumps({'login': False}), status=403)
        return resp


@routes.route('/generate_password', methods=['POST'])
def generate_password():
    try:
        user_data = request.json

        try :
            user = models.AppUser.query\
                .filter(models.AppUser.email==user_data['email'])\
                .one()
        except Exception as e:
            resp = Response(json.dumps({'type':'email', 'msg':'Email invalide'}), status=490)
            return resp
        p = user.generate_newpassword()
        db.session.add(user)
        db.session.commit()

        msg = render_template("generate_password.txt",
                               user=user, newpassword = p)
        msg_html = render_template("generate_password.html",
                              user=user, newpassword = p)

        send_mail('Nouveau mot de passe', msg, msg_html, user.email)

        resp = Response(json.dumps({'generation':'new pass'}))
        return resp
    except Exception as e:
        raise
        resp = Response(json.dumps({'login': False}), status=403)
        return resp
