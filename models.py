from app import db

class Sheet(db.Model):
    __tablename__ = 'sheet'

    sheet_label = db.Column(db.String(), primary_key=True)
    iteration = db.Column(db.Integer, unique=True)
    avgmoe = db.Column(db.DECIMAL())
    avgsg = db.Column(db.DECIMAL())
    avgmc = db.Column(db.DECIMAL())
    avgvel = db.Column(db.DECIMAL())
    avgupt = db.Column(db.DECIMAL())
    pkdensity = db.Column(db.DECIMAL())
    effvel = db.Column(db.ARRAY(db.DECIMAL()))
    lvel = db.Column(db.ARRAY(db.DECIMAL()))
    rvel = db.Column(db.ARRAY(db.DECIMAL()))
    lupt = db.Column(db.ARRAY(db.DECIMAL()))
    rupt = db.Column(db.ARRAY(db.DECIMAL()))
    sg = db.Column(db.ARRAY(db.DECIMAL()))
    mc = db.Column(db.ARRAY(db.DECIMAL()))

