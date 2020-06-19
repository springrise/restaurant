from db import db


class OrderItemModel(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))

    food = db.relationship('FoodModel')
    order = db.relationship('OrderModel')

    def __init__(self, food_id, order_id):
        self.food_id = food_id
        self.order_id = order_id

    def json(self):
        return {
            'items_id': self.id,
            'food_id': self.food_id,
            'order_id': self.order_id
        }

    @classmethod
    def find_by_order_id(cls, order_id):
        return cls.query.filter_by(order_id=order_id)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
