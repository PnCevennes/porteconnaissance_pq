#coding: utf8

'''
routes relatives aux application, utilisateurs et à l'authentification
'''
from flask import Blueprint, Flask, request, jsonify,  Response
from server import db, init_app as get_app
from . import models
from ..login import routes as fnauth

from geojson import Feature, FeatureCollection, dumps

routes = Blueprint('pq', __name__)

@routes.route('/', methods=['GET'])
@fnauth.check_auth()
def get_pq():
    data = models.PqData.query.all()
    return jsonify(FeatureCollection([liste.as_geofeature() for liste in data]))


@routes.route('/communes', methods=['GET'])
@fnauth.check_auth()
def get_communes():
    data = models.Communes.query.all()
    return jsonify([liste.as_dict() for liste in data])


@routes.route('/contact/massifs', methods=['GET'])
@fnauth.check_auth()
def get_contact_massifs():
    data = models.ContactMassifs.query.filter(models.ContactMassifs.nom_agent.isnot(None)).all()
    return jsonify({liste.as_dict()['nom_massif']: liste.as_dict() for liste in data})


@routes.route('/contact/secteurs', methods=['GET'])
@fnauth.check_auth()
def get_contact_secteurs():
    data = models.ContactSecteurs.query.filter(models.ContactSecteurs.nom_agent.isnot(None)).all()
    return jsonify({liste.as_dict()['id_secteur']: liste.as_dict() for liste in data})
