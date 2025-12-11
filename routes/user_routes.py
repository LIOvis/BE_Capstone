from flask import Blueprint

import controllers

user = Blueprint('user', __name__)

@user.route('/user', methods=["POST"])
def add_user_route():
    return controllers.add_user()

@user.route('/users', methods=["GET"])
def get_all_users_route():
    return controllers.get_all_users()

@user.route('/user/<user_id>', methods=["GET"])
def get_user_by_id_route(user_id):
    return controllers.get_user_by_id(user_id)

@user.route('/user/profile', methods=["GET"])
def get_logged_in_user_route():
    return controllers.get_logged_in_user()

@user.route('/user/<user_id>', methods=["PUT"])
def update_user_by_id_route(user_id):
    return controllers.update_user_by_id(user_id)

@user.route('/user/delete/<user_id>', methods=["DELETE"])
def delete_user_by_id_route(user_id):
    return controllers.delete_user_by_id(user_id)


