from db import db


class FoodModel(db.Model):
    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    orders = db.relationship('OrderModel', lazy='dynamic')

    def __init__(self, name, price):
        self.name = name
        self.price = price
        # self.user_id = user_id

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            # 'store_id': self.user_id
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()