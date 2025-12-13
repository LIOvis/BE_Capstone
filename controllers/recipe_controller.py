from flask import jsonify, request

from models.recipe_ingredient_xref import RecipesIngredients, recipe_ingredient_schema
from models.cuisine_recipe_xref import CuisinesRecipes, cuisine_recipe_schema
from lib.authenticate import authenticate_return_auth, authenticate
from models.recipe import Recipes, recipe_schema, recipes_schema
from util.reflection import populate_object
from models.ingredient import Ingredients
from models.cuisine import Cuisines
from models.user import Users
from db import db


@authenticate_return_auth
def add_recipe(auth_info):
    post_data = request.form if request.form else request.json
    
    new_recipe = Recipes.new_recipe_obj()

    populate_object(new_recipe, post_data)

    if 'user_id' in post_data:
        if post_data.get('user_id') != auth_info.user_id and auth_info.user.role != 'Super Admin':
            return jsonify({"message":  "forbidden: higher role required to add a recipe to another user"}), 403
    else:
            new_recipe.user_id = auth_info.user_id



    try:
        db.session.add(new_recipe)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to add recipe"}), 400
    
    return jsonify({"message": "recipe added", "result": recipe_schema.dump(new_recipe)}), 201
    

@authenticate_return_auth
def add_ingredient_to_recipe(recipe_id, auth_info):
    post_data = request.form if request.form else request.json
    recipe_query = db.session.query(Recipes).filter(Recipes.recipe_id == recipe_id).first()
    ingredient_query = db.session.query(Ingredients).filter(Ingredients.ingredient_id == post_data.get('ingredient_id')).first()

    if not recipe_query:
        return jsonify({"message": "recipe not found"}), 404

    if not ingredient_query:
        return jsonify({"message": "ingredient not found"}), 404
    
    if ingredient_query.is_active == False:
        return jsonify({"message": "cannot add an inactive ingredient"}), 400

    if recipe_query.user_id != auth_info.user_id and auth_info.user.role != 'Super Admin':
        return jsonify({"message":  "forbidden: higher role required to add an ingredient to another user's recipe"}), 403
    
    new_recipe_ingredient = RecipesIngredients.new_recipe_ingredient_obj()

    populate_object(new_recipe_ingredient, post_data)

    new_recipe_ingredient.recipe_id = recipe_id

    try:
        db.session.add(new_recipe_ingredient)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to add ingredient to recipe"}), 400
    
    return jsonify({"message": "ingredient added to recipe", "result": recipe_ingredient_schema.dump(new_recipe_ingredient)}), 201


@authenticate_return_auth
def add_cuisine_to_recipe(recipe_id, auth_info):
    post_data = request.form if request.form else request.json
    recipe_query = db.session.query(Recipes).filter(Recipes.recipe_id == recipe_id).first()
    cuisine_query = db.session.query(Cuisines).filter(Cuisines.cuisine_id == post_data.get('cuisine_id')).first()

    if not recipe_query:
        return jsonify({"message": "recipe not found"}), 404

    if not cuisine_query:
        return jsonify({"message": "cuisine not found"}), 404
    
    if cuisine_query.is_active == False:
        return jsonify({"message": "cannot add an inactive cuisine"}), 400

    if recipe_query.user_id != auth_info.user_id and auth_info.user.role != 'Super Admin':
        return jsonify({"message":  "forbidden: higher role required to add a cuisine to another user's recipe"}), 403
    
    new_recipe_cuisine = CuisinesRecipes.new_recipe_cuisine_obj()

    populate_object(new_recipe_cuisine, post_data)

    new_recipe_cuisine.recipe_id = recipe_id

    try:
        db.session.add(new_recipe_cuisine)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to add cuisine to recipe"}), 400
    
    return jsonify({"message": "cuisine added to recipe", "result": cuisine_recipe_schema.dump(new_recipe_cuisine)}), 201


@authenticate_return_auth
def get_all_recipes(auth_info):
    query = db.session.query(Recipes).all()

    recipes = recipes_schema.dump(query)

    if auth_info.user.role == "User":
        active_recipes = []
        for recipe in recipes:
            if recipe["is_active"] == True or recipe["created_by"]["user_id"] == auth_info.user_id:
                active_recipes.append(recipe)
        recipes = active_recipes

    return jsonify({"message": "recipes found", "results": recipes}), 200
    

@authenticate_return_auth
def get_recipe_by_id(recipe_id, auth_info):
    query = db.session.query(Recipes).filter(Recipes.recipe_id == recipe_id).first()

    if not query:
        return jsonify({"message": "recipe not found"}), 404
    
    if auth_info.user.role == "User" and query.is_active == False: 
        return jsonify({"message": "forbidden: higher role required to view inactive recipe"})
    
    return jsonify({"message": "recipe found", "result": recipe_schema.dump(query)}), 200


@authenticate_return_auth
def get_recipes_by_ingredient(ingredient_id, auth_info):
    ingredient_query = db.session.query(Ingredients).filter(Ingredients.ingredient_id == ingredient_id).all()

    if not ingredient_query:
        return jsonify({"message": "ingredient not found"}), 404

    query = db.session.query(Recipes).filter(Recipes.ingredients.any(ingredient_id=ingredient_id)).all()

    recipes = recipes_schema.dump(query)

    if auth_info.user.role == "User":
        active_recipes = []
        for recipe in recipes:
            if recipe["is_active"] == True or recipe["created_by"]["user_id"] == auth_info.user_id:
                active_recipes.append(recipe)
        recipes = active_recipes

    return jsonify({"message": "recipes found", "results": recipes}), 200


@authenticate_return_auth
def get_recipes_by_cuisine(cuisine_id, auth_info):
    cuisine_query = db.session.query(Cuisines).filter(Cuisines.cuisine_id == cuisine_id).all()

    if not cuisine_query:
        return jsonify({"message": "cuisine not found"}), 404
    
    query = db.session.query(Recipes).filter(Recipes.cuisines.any(cuisine_id=cuisine_id)) .all()

    recipes = recipes_schema.dump(query)

    if auth_info.user.role == "User":
        active_recipes = []
        for recipe in recipes:
            if recipe["is_active"] == True or recipe["created_by"]["user_id"] == auth_info.user_id:
                active_recipes.append(recipe)
        recipes = active_recipes

    return jsonify({"message": "recipes found", "results": recipes}), 200


@authenticate_return_auth
def get_recipes_by_user(user_id, auth_info):
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if not user_query:
        return jsonify({"message": "user not found"}), 404
    
    query = db.session.query(Recipes).filter(Recipes.user_id == user_id).all()

    recipes = recipes_schema.dump(query)

    if auth_info.user.role == "User":
        active_recipes = []
        for recipe in recipes:
            recipe_query = db.session.query(Recipes).filter(Recipes.recipe_id == recipe["recipe_id"]).first()
            if recipe_query.is_active == True or recipe_query.user_id == auth_info.user_id:
                active_recipes.append(recipe)
        recipes = active_recipes

    return jsonify({"message": "recipes found", "results": recipes}), 200


@authenticate_return_auth
def update_recipe_by_id(recipe_id, auth_info):
    post_data = request.form if request.form else request.json
    query = db.session.query(Recipes).filter(Recipes.recipe_id == recipe_id).first()

    if not query:
        return jsonify({"message": "recipe not found"}), 404

    if auth_info.user.role != 'Super Admin' and auth_info.user_id != query.user_id:
        return jsonify({"message": "forbidden: higher role required to update another user's recipe"}), 403
    
    populate_object(query, post_data)

    try:
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to update recipe"}), 400

    return jsonify({"message": "recipe updated", "result": recipe_schema.dump(query)}), 200


@authenticate_return_auth
def delete_recipe_by_id(recipe_id, auth_info):
    query = db.session.query(Recipes).filter(Recipes.recipe_id == recipe_id).first()
    
    if not query:
        return jsonify({"message": "recipe not found"}), 404

    if auth_info.user.role != "Super Admin" and auth_info.user_id != query.user_id:
        return jsonify({"message": "forbidden: higher role required to delete another user's recipe"}), 403
    
    try:
        db.session.delete(query)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete recipe"}), 400

    return jsonify({"message": "recipe deleted"}), 200


@authenticate_return_auth
def delete_ingredient_from_recipe(recipe_id, ingredient_id, auth_info):
    query = db.session.query(RecipesIngredients).filter(RecipesIngredients.recipe_id == recipe_id, RecipesIngredients.ingredient_id == ingredient_id).first()
    
    if not query:
        return jsonify({"message": "ingredient not found in recipe"}), 404

    if auth_info.user.role != "Super Admin" and auth_info.user_id != query.recipe.user_id:
        return jsonify({"message": "forbidden: higher role required to delete an ingredient from another user's recipe"}), 403
    
    try:
        db.session.delete(query)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete ingredient from recipe"}), 400

    return jsonify({"message": "ingredient deleted from recipe"}), 200


@authenticate_return_auth
def delete_cuisine_from_recipe(recipe_id, cuisine_id, auth_info):
    query = db.session.query(CuisinesRecipes).filter(CuisinesRecipes.recipe_id == recipe_id, CuisinesRecipes.cuisine_id == cuisine_id).first()
    
    if not query:
        return jsonify({"message": "cuisine not found in recipe"}), 404

    if auth_info.user.role != "Super Admin" and auth_info.user_id != query.recipe.user_id:
        return jsonify({"message": "forbidden: higher role required to delete a cuisine from another user's recipe"}), 403
    
    try:
        db.session.delete(query)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete cuisine from recipe"}), 400

    return jsonify({"message": "cuisine deleted from recipe"}), 200
