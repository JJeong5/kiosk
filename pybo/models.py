from pybo import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coffee = db.Column(db.Integer, nullable=False)
    greentea = db.Column(db.Integer, nullable=False)
    bananamilk = db.Column(db.Integer, nullable=False)
    picnic = db.Column(db.Integer, nullable=False)