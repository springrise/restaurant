from db import db


class OrderModel(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float(precision=2))
    status = db.Column(db.String(80))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('UserModel')


    items = db.relationship('OrderItemModel', lazy='dynamic')

    def __init__(self, user_id, total_price, status):
        self.total_price = total_price
        self.user_id = user_id
        self.status = status

    def json(self):
        return {
            'order_id': self.id,
            'total_price': self.total_price,
            'user_id': self.user_id,
            'status': self.status
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id)

    @classmethod
    def find_by_user_order_id(cls, _id, user_id):
        return cls.query.filter_by(user_id=user_id).filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
