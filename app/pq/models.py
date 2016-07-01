#coding: utf8

from server import db
from geoalchemy2 import Geometry

from shapely.wkb import loads

from shapely.geometry import asShape
from geoalchemy2.shape import to_shape, from_shape

from geojson import Feature

class PqData(db.Model):
    __tablename__ = 'v_perimetres_quietude'
    __table_args__ = {'schema':'pq'}
    r = db.Column(db.Integer, primary_key=True)
    code_sp = db.Column(db.Unicode)
    code_etat = db.Column(db.Unicode)
    max_etat_annee = db.Column(db.Integer)
    zone_pnc = db.Column(db.Unicode)
    massifs = db.Column(db.Unicode)
    id_secteur = db.Column(db.Unicode)
    qtd_nom = db.Column(db.Unicode)
    geom =  db.Column('geom', Geometry('MULTIPOLYGON', srid=4326))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def as_geofeature(self):
        geometry = to_shape(self.geom)
        feature = Feature(
                id=self.r,
                geometry=geometry,
                properties= {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name!='geom'}
            )
        return feature

class Communes(db.Model):
    __tablename__ = 'communes'
    __table_args__ = {'schema':'lim_admin'}
    code_insee= db.Column(db.Integer, primary_key=True)
    geom =  db.Column('geom_4326', Geometry('MULTIPOLYGON', srid=4326))
    geom_buffer =  db.Column('geom_buffer', Geometry('MULTIPOLYGON', srid=4326))
    nom_com =  db.Column(db.Unicode)

    def as_dict(self):
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
        }

    def as_geofeature(self):
        geometry = to_shape(self.geom)
        feature = Feature(
                id=self.code_insee,
                geometry=geometry
            )
        return feature

class CommunesEmprises(db.Model):
    __tablename__ = 'v_communes_emprise'
    __table_args__ = {'schema':'lim_admin'}
    code_insee= db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Unicode)
    st_xmax = db.Column(db.Unicode)
    st_xmin= db.Column(db.Unicode)
    st_ymax = db.Column(db.Unicode)
    st_ymin= db.Column(db.Unicode)

    def as_dict(self):
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
        }

class ContactMassifs(db.Model):
    __tablename__ = 'contact_massifs'
    __table_args__ = {'schema':'pq'}
    id= db.Column(db.Integer, primary_key=True)
    nom_massif = db.Column(db.Unicode)
    nom_agent = db.Column(db.Unicode)
    tel_portable = db.Column(db.Unicode)
    tel_fixe = db.Column(db.Unicode)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class ContactDt(db.Model):
    __tablename__ = 'contact_dt'
    __table_args__ = {'schema':'pq'}
    id= db.Column(db.Integer, primary_key=True)
    nom_massif = db.Column(db.Unicode)
    nom_dt = db.Column(db.Unicode)
    tel_portable = db.Column(db.Unicode)
    tel_fixe = db.Column(db.Unicode)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ContactSecteurs(db.Model):
    __tablename__ = 'contact_secteurs'
    __table_args__ = {'schema':'pq'}
    id= db.Column(db.Integer, primary_key=True)
    id_secteur = db.Column(db.Integer)
    nom_agent = db.Column(db.Unicode)
    tel_portable = db.Column(db.Unicode)
    tel_fixe = db.Column(db.Unicode)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
