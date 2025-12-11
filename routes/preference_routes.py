from flask import Blueprint

import controllers

preference = Blueprint('preference', __name__)

@preference.route('/preference', methods=["POST"])
def add_user_preference_route():
    return controllers.add_user_preference()

@preference.route('/preferences', methods=["GET"])
def get_all_user_preferences_route():
    return controllers.get_all_user_preferences()

@preference.route('/preference/<user_id>', methods=["GET"])
def get_user_preference_by_id_route(user_id):
    return controllers.get_user_preference_by_id(user_id)

@preference.route('/preference/<user_id>', methods=["PUT"])
def update_user_preference_by_id_route(user_id):
    return controllers.update_user_preference_by_id(user_id)

@preference.route('/preference/delete/<user_id>', methods=["DELETE"])
def delete_user_preference_by_id_route(user_id):
    return controllers.delete_user_preference_by_id(user_id)


