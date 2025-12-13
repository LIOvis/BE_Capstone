from flask import jsonify, request

from models.cuisine import Cuisines, cuisine_schema, cuisines_schema
from lib.authenticate import authenticate_return_auth, authenticate
from util.reflection import populate_object
from db import db


@authenticate_return_auth
def add_cuisine(auth_info):
    if auth_info.user.role != 'User':
        post_data = request.form if request.form else request.json
        
        new_cuisine = Cuisines.new_cuisine_obj()

        populate_object(new_cuisine, post_data)

        try:
            db.session.add(new_cuisine)
            db.session.commit()

        except:
            db.session.rollback()
            return jsonify({"message": "unable to add cuisine"}), 400
        
        return jsonify({"message": "cuisine added", "result": cuisine_schema.dump(new_cuisine)}), 201
    
    return jsonify({"message": "forbidden: higher force rank required"}), 403


@authenticate_return_auth
def get_all_cuisines(auth_info):
    query = db.session.query(Cuisines).all()

    cuisines = cuisines_schema.dump(query)

    if auth_info.user.role == "User":
        for cuisine in cuisines:
            active_recipes = []
            for recipe in cuisine["recipes"]:
                if recipe["is_active"] == True or recipe["created_by"]["user_id"] == auth_info.user_id:
                    active_recipes.append(recipe)
            cuisine["recipes"] = active_recipes

    return jsonify({"message": "cuisines found", "results": cuisines}), 200
    

@authenticate_return_auth
def get_cuisine_by_id(cuisine_id, auth_info):
    query = db.session.query(Cuisines).filter(Cuisines.cuisine_id == cuisine_id).first()

    if not query:
        return jsonify({"message": "cuisine not found"}), 404
    
    cuisine = cuisine_schema.dump(query)
    
    if auth_info.user.role == "User": 
        active_recipes = []
        for recipe in cuisine["recipes"]:
            if recipe["is_active"] == True or recipe["created_by"]["user_id"] == auth_info.user_id:
                active_recipes.append(recipe)
        cuisine["recipes"] = active_recipes
    
    return jsonify({"message": "cuisine found", "result": cuisine}), 200


@authenticate_return_auth
def update_cuisine_by_id(cuisine_id, auth_info):
    post_data = request.form if request.form else request.json
    query = db.session.query(Cuisines).filter(Cuisines.cuisine_id == cuisine_id).first()

    if auth_info.user.role == 'User':
        return jsonify({"message": "forbidden: higher role required"}), 403

    if not query:
        return jsonify({"message": "cuisine not found"}), 404
    
    populate_object(query, post_data)

    try:
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to update cuisine"}), 400

    return jsonify({"message": "cuisine updated", "result": cuisine_schema.dump(query)}), 200


@authenticate_return_auth
def delete_cuisine_by_id(cuisine_id, auth_info):
    query = db.session.query(Cuisines).filter(Cuisines.cuisine_id == cuisine_id).first()

    if auth_info.user.role != "Super Admin":
        return jsonify({"message": "forbidden: higher role required"}), 403
    
    if not query:
        return jsonify({"message": "cuisine not found"}), 404
    
    try:
        db.session.delete(query)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete cuisine"}), 400

    return jsonify({"message": "cuisine deleted"}), 200