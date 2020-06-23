from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity
from datetime import datetime

from models.food import FoodModel
from models.order import OrderModel


class Order(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('food_id',
                        type=list,
                        required=True,
                        location='json',
                        help="every order need a list of food id!"
                        )

    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        data = Order.parser.parse_args()

        foods = [FoodModel.find_by_id(food).json() for food in data['food_id']]
        total_price = sum([food['price'] for food in foods])
        status = 'submitted.'
        created_at = datetime.now()
        order = OrderModel(user_id, total_price, status, created_at, created_at)

        try:
            order.save_to_db()
        except:
            return {"message": "An error occurred inserting the food."}, 500

        return order.json(), 201


class OrderTrack(Resource):
    @jwt_required
    def get(self, _id):
        user_id = get_jwt_identity()
        order = OrderModel.find_by_user_order_id(_id, user_id)
        if order:
            return order.json()
        return {'message': 'Order not found!'}, 404

    @jwt_required
    def put(self, _id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        parser = reqparse.RequestParser()
        parser.add_argument('food_id',
                            type=list,
                            required=True,
                            location='json',
                            help="every order need a list of food id!"
                            )
        data = Order.parser.parse_args()

        order = OrderModel.find_by_id(_id)

        if order:
            foods = [FoodModel.find_by_id(food).json() for food in data['food_id']]
            total_price = sum([food['price'] for food in foods])
            order.total_price = total_price
            order.updated_at = datetime.now()
        else:
            return {'message': 'Order not found'}, 404

        try:
            order.save_to_db()
        except:
            return {"message": "An error occurred inserting the food."}, 500

        return order.json(), 201
    @jwt_required
    def delete(self, _id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        order = OrderModel.find_by_id(_id)

        if order:
            order.delete_from_db()
            return {'message': 'Order deleted'}
        return {'message': 'order not found.'}, 404


class OrderList(Resource):

    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return{'message': 'admin privilege required.'}, 401

        orders = [order.json() for order in OrderModel.find_all()]
        return {'orders': orders},200


class UserOrders(Resource):
    @jwt_required
    def get(self,_id):
        user_id = get_jwt_identity()
        order = OrderModel.find_by_user_order_id(_id, user_id)
        if order:
            return order.json(), 200
        return {'userorder': 'order not found'}, 404
