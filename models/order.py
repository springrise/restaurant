from db import db

class OrderModel(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float(precision=2))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'))

    user = db.relationship('UserModel')
    food = db.relationship('FoodModel')

    def __init__(self, user_id, food_id, price):
        self.price = price
        self.user_id = user_id
        self.food_id = food_id

    def json(self):
        return {
            'order_id': self.id,
            'price': self.price,
            'user_id': self.user_id,
            'food_id': self.food_id
        }

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