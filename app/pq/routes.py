#coding: utf8

'''
routes relatives aux application, utilisateurs et à l'authentification
'''
from flask import Blueprint, Flask, request, jsonify,  Response
from server import db, init_app as get_app
from . import models
from ..login import routes as fnauth, models as userModels

from sqlalchemy import func
from geojson import Feature, FeatureCollection, dumps

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

routes = Blueprint('pq', __name__)

@routes.route('/', methods=['GET'])
@fnauth.check_auth()
def get_pq():
    s = Serializer(get_app().config['SECRET_KEY'])
    user_id = s.loads(request.cookies['token'])

    user = userModels.AppUser.query\
        .filter(userModels.AppUser.id_role==user_id['id_role'])\
        .one()

    data = db.session.query(models.PqData)\
        .join(models.Communes, func.ST_Intersects(models.PqData.geom, models.Communes.geom_buffer))\
        .filter(models.Communes.code_insee == user.code_insee)\
        .all()

    # data = db.session.query(models.PqData)\
    #     .all()
    return jsonify(FeatureCollection([liste.as_geofeature() for liste in data]))


@routes.route('/communes', methods=['GET'])
@fnauth.check_auth()
def get_communes():
    data = models.CommunesEmprises.query.all()
    return jsonify([liste.as_dict() for liste in data])


@routes.route('/maskcommunes/<code_insee>', methods=['GET'])
@fnauth.check_auth()
def get_maskcommunes(code_insee):
    data = models.Communes.query.filter(models.Communes.code_insee == code_insee).one()
    return jsonify(data.as_geofeature())

@routes.route('/contact/massifs', methods=['GET'])
@fnauth.check_auth()
def get_contact_massifs():
    data = models.ContactMassifs.query.filter(models.ContactMassifs.nom_agent.isnot(None)).all()
    return jsonify({liste.as_dict()['nom_massif']: liste.as_dict() for liste in data})

@routes.route('/contact/dt', methods=['GET'])
@fnauth.check_auth()
def get_contact_dt():
    data = models.ContactDt.query.filter(models.ContactDt.nom_dt.isnot(None)).all()
    return jsonify({liste.as_dict()['nom_massif']: liste.as_dict() for liste in data})

@routes.route('/contact/secteurs', methods=['GET'])
@fnauth.check_auth()
def get_contact_secteurs():
    data = models.ContactSecteurs.query.filter(models.ContactSecteurs.nom_agent.isnot(None)).all()
    return jsonify({liste.as_dict()['id_secteur']: liste.as_dict() for liste in data})
