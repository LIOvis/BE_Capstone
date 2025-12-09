from flask import jsonify, request

from models.ingredient import Ingredients, ingredient_schema, ingredients_schema
from lib.authenticate import authenticate_return_auth, authenticate
from util.reflection import populate_object
from db import db


@authenticate
def add_ingredient():
    post_data = request.form if request.form else request.json
    
    new_ingredient = Ingredients.new_ingredient_obj()

    populate_object(new_ingredient, post_data)

    try:
        db.session.add(new_ingredient)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "unable to add ingredient", "error": str(e)}), 400
    
    return jsonify({"message": "ingredient added", "result": ingredient_schema.dump(new_ingredient)}), 201
    

@authenticate_return_auth
def get_all_ingredients(auth_info):
    query = db.session.query(Ingredients).all()

    ingredients = ingredients_schema.dump(query)

    if auth_info.user.role == "User":
        for ingredient in ingredients:
            active_recipes = []
            for recipe in ingredient.recipes:
                if recipe.is_active == "True":
                    active_recipes.append(recipe)
            ingredient.recipes = active_recipes

    return jsonify({"message": "ingredients found", "results": ingredients}), 200
    

@authenticate_return_auth
def get_ingredient_by_id(ingredient_id, auth_info):
    query = db.session.query(Ingredients).filter(Ingredients.ingredient_id == ingredient_id).first()

    if not query:
        return jsonify({"message": "ingredient not found"}), 404
    
    ingredient = ingredient_schema.dump(query)
    
    if auth_info.user.role == "User": 
        active_recipes = []
        for recipe in ingredient.recipes:
            if recipe.is_active == "True":
                active_recipes.append(recipe)
        ingredient.recipes = active_recipes
    
    return jsonify({"message": "ingredient found", "result": ingredient}), 200


@authenticate_return_auth
def update_ingredient_by_id(ingredient_id, auth_info):
    post_data = request.form if request.form else request.json
    query = db.session.query(Ingredients).filter(Ingredients.ingredient_id == ingredient_id).first()

    if auth_info.user.role == 'User':
        return jsonify({"message": "forbidden: higher role required"}), 403

    if not query:
        return jsonify({"message": "ingredient not found"}), 404
    
    populate_object(query, post_data)

    try:
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to update ingredient"}), 400

    return jsonify({"message": "ingredient updated", "result": ingredient_schema.dump(query)}), 200


@authenticate_return_auth
def delete_ingredient_by_id(ingredient_id, auth_info):
    query = db.session.query(Ingredients).filter(Ingredients.ingredient_id == ingredient_id).first()

    if auth_info.user.role != "Super Admin":
        return jsonify({"message": "forbidden: higher role required"}), 403
    
    if not query:
        return jsonify({"message": "ingredient not found"}), 404
    
    try:
        db.session.delete(query)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete ingredient"}), 400

    return jsonify({"message": "ingredient deleted"}), 200