#coding: utf8

'''
routes relatives aux application, utilisateurs et à l'authentification
'''
from flask import Blueprint, Flask, request, jsonify,  Response
from server import db,get_app
from . import models
from ..login import routes as fnauth

from geojson import Feature, FeatureCollection, dumps

import pprint

routes = Blueprint('pq', __name__)

@routes.route('/', methods=['GET'])
@fnauth.check_auth()
def pq():
    data = models.PqData.query.all()
    return jsonify(FeatureCollection([liste.as_geofeature() for liste in data]))
