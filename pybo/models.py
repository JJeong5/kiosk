from pybo import db
from datetime import datetime

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coffee = db.Column(db.Integer, nullable=False)
    greentea = db.Column(db.Integer, nullable=False)
    bananamilk = db.Column(db.Integer, nullable=False)
    picnic = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='주문 접수 중')
    order_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))