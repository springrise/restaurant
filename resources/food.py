from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional, # it let you add into any endpoint that the jwt can or cannot be present, then inside the endpoint, you can choose what to do if it is present or not
    get_jwt_identity,#its going to give us whatever we saved in the access token as the identity
    fresh_jwt_required
)
from models.food import FoodModel


class Food(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required #fresh or non-fresh
    def get(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        food = FoodModel.find_by_name(name)
        if food:
            return food.json()
        return {'message': 'Food not found'}, 404

    @jwt_required
    def post(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        if FoodModel.find_by_name(name):
            return {'message': "A food with name '{}' already exists.".format(name)}, 400

        data = Food.parser.parse_args()

        food = FoodModel(name, **data)

        try:
            food.save_to_db()
        except:
            return {"message": "An error occurred inserting the food."}, 500

        return food.json(), 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        food = FoodModel.find_by_name(name)
        if food:
            food.delete_from_db()
            return {'message': 'Food deleted.'}
        return {'message': 'Food not found.'}, 404

    @jwt_required
    def put(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        data = Food.parser.parse_args()

        food = FoodModel.find_by_name(name)

        if food:
            food.price = data['price']
        else:
            food = FoodModel(name, **data)

        food.save_to_db()

        return food.json()


class FoodList(Resource):
    def get(self):
        foods = [food.json() for food in FoodModel.find_all()]
        return {'food': foods}, 200