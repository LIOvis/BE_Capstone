from flask import Blueprint

import controllers

cuisine = Blueprint('cuisine', __name__)

@cuisine.route('/cuisine', methods=["POST"])
def add_cuisine_route():
    return controllers.add_cuisine()

@cuisine.route('/cuisines', methods=["GET"])
def get_all_cuisines_route():
    return controllers.get_all_cuisines()

@cuisine.route('/cuisine/<cuisine_id>', methods=["GET"])
def get_cuisine_by_id_route(cuisine_id):
    return controllers.get_cuisine_by_id(cuisine_id)

@cuisine.route('/cuisine/<cuisine_id>', methods=["PUT"])
def update_cuisine_by_id_route(cuisine_id):
    return controllers.update_cuisine_by_id(cuisine_id)

@cuisine.route('/cuisine/delete/<cuisine_id>', methods=["DELETE"])
def delete_cuisine_by_id_route(cuisine_id):
    return controllers.delete_cuisine_by_id(cuisine_id)


