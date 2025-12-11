from flask import Blueprint

import controllers

ingredient = Blueprint('ingredient', __name__)

@ingredient.route('/ingredient', methods=["POST"])
def add_ingredient_route():
    return controllers.add_ingredient()

@ingredient.route('/ingredients', methods=["GET"])
def get_all_ingredients_route():
    return controllers.get_all_ingredients()

@ingredient.route('/ingredient/<ingredient_id>', methods=["GET"])
def get_ingredient_by_id_route(ingredient_id):
    return controllers.get_ingredient_by_id(ingredient_id)

@ingredient.route('/ingredient/<ingredient_id>', methods=["PUT"])
def update_ingredient_by_id_route(ingredient_id):
    return controllers.update_ingredient_by_id(ingredient_id)

@ingredient.route('/ingredient/delete/<ingredient_id>', methods=["DELETE"])
def delete_ingredient_by_id_route(ingredient_id):
    return controllers.delete_ingredient_by_id(ingredient_id)


