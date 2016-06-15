from server import db
from geoalchemy2 import Geometry

from shapely.wkb import loads

from shapely.geometry import asShape
from geoalchemy2.shape import to_shape, from_shape

from geojson import Feature

class PqData(db.Model):
    __tablename__ = 'perimetres_quietude'
    __table_args__ = {'schema':'pq'}
    r = db.Column(db.Integer, primary_key=True)
    code_sp = db.Column(db.Unicode)
    code_etat = db.Column(db.Unicode)
    zone_pnc = db.Column(db.Unicode)
    massifs = db.Column(db.Unicode)
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
