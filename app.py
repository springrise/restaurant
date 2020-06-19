from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from blacklist import BLACKLIST
from models.user import UserModel
from resources.order import Order, OrderTrack, OrderList, UserOrders
from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout
from resources.food import Food, FoodList, FoodCategoryList

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True  # enable blacklist feature
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = [
    "access",
    "refresh",
]
app.secret_key = "SECRET_KEY"

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()
    UserModel('bahareh', '12345', 'admin').save_to_db()


jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):  # Remember identity is what we define when creating the access token
    user = User.get(identity)
    if user['role'] == 'admin':  # instead of hard-coding, we should read from a file or database to get a list of admins instead
        return {"is_admin": True}
    return {"is_admin": False}


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return (
        decrypted_token["jti"] in BLACKLIST
    )  # Here we blacklist particular JWTs that have been created in the past.


# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(
    error
):  # we have to keep the argument here, since it's passed in by the caller internally
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return (
        jsonify(
            {"description": "The token is not fresh.", "error": "fresh_token_required"}
        ),
        401,
    )


@jwt.revoked_token_loader
def revoked_token_callback():
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )


api.add_resource(Food, "/food/<string:name>")
api.add_resource(FoodList, "/foods")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(Order, "/order")
api.add_resource(OrderTrack, "/order/<int:_id>")
api.add_resource(OrderList, "/orders")
api.add_resource(FoodCategoryList, "/categories")
api.add_resource(UserOrders, "/userorders/<int:user_id>")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
