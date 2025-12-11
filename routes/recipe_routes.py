from flask import Blueprint

import controllers

recipe = Blueprint('recipe', __name__)

@recipe.route('/recipe', methods=["POST"])
def add_recipe_route():
    return controllers.add_recipe()

@recipe.route('/recipe/<recipe_id>/ingredient', methods=["POST"])
def add_ingredient_to_recipe_route(recipe_id):
    return controllers.add_ingredient_to_recipe(recipe_id)

@recipe.route('/recipe/<recipe_id>/cuisine', methods=["POST"])
def add_cuisine_to_recipe_route(recipe_id):
    return controllers.add_cuisine_to_recipe(recipe_id)

@recipe.route('/recipes', methods=["GET"])
def get_all_recipes_route():
    return controllers.get_all_recipes()

@recipe.route('/recipe/<recipe_id>', methods=["GET"])
def get_recipe_by_id_route(recipe_id):
    return controllers.get_recipe_by_id(recipe_id)

@recipe.route('/recipes/ingredient/<ingredient_id>', methods=["GET"])
def get_recipes_by_ingredient_route(ingredient_id):
    return controllers.get_recipes_by_ingredient(ingredient_id)

@recipe.route('/recipes/cuisine/<cuisine_id>', methods=["GET"])
def get_recipes_by_cuisine_route(cuisine_id):
    return controllers.get_recipes_by_cuisine(cuisine_id)

@recipe.route('/recipes/user/<user_id>', methods=["GET"])
def get_recipes_by_user_route(user_id):
    return controllers.get_recipes_by_user(user_id)

@recipe.route('/recipe/<recipe_id>', methods=["PUT"])
def update_recipe_by_id_route(recipe_id):
    return controllers.update_recipe_by_id(recipe_id)

@recipe.route('/recipe/delete/<recipe_id>', methods=["DELETE"])
def delete_recipe_by_id_route(recipe_id):
    return controllers.delete_recipe_by_id(recipe_id)

@recipe.route('/recipe/delete/<recipe_id>/ingredient/<ingredient_id>', methods=["DELETE"])
def delete_ingredient_from_recipe_route(recipe_id, ingredient_id):
    return controllers.delete_ingredient_from_recipe(recipe_id, ingredient_id)

@recipe.route('/recipe/delete/<recipe_id>/cuisine/<cuisine_id>', methods=["DELETE"])
def delete_cuisine_from_recipe_route(recipe_id, cuisine_id):
    return controllers.delete_cuisine_from_recipe(recipe_id, cuisine_id)


