from flask import jsonify, request

from models.user_preference import UsersPreferences, user_preference_schema, users_preferences_schema
from lib.authenticate import authenticate_return_auth, authenticate
from util.reflection import populate_object
from db import db


@authenticate_return_auth
def add_user_preference(auth_info):
    post_data = request.form if request.form else request.json

    if 'user_id' in post_data and (post_data.get("user_id") != str(auth_info.user_id) and auth_info.user.role != "Super Admin"):
        return jsonify({"message": "forbidden: higher role required to add user preferences to another user"}), 403
    
    new_user_preference = UsersPreferences.new_user_preference_obj()

    populate_object(new_user_preference, post_data)

    try:
        db.session.add(new_user_preference)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to add user preferences"}), 400
    
    return jsonify({"message": "user preferences added", "result": user_preference_schema.dump(new_user_preference)}), 201
    

@authenticate_return_auth
def get_all_user_preferences(auth_info):
    query = db.session.query(UsersPreferences).all()

    if auth_info.user.role == 'User':
        return jsonify({"message": "forbidden: higher role required"}), 403

    return jsonify({"message": "users preferences found", "results": users_preferences_schema.dump(query)}), 200
    

@authenticate_return_auth
def get_user_preference_by_id(user_id, auth_info):
    query = db.session.query(UsersPreferences).filter(UsersPreferences.user_id == user_id).first()

    if auth_info.user.role == 'User':
        return jsonify({"message": "forbidden: higher role required"}), 403

    if not query:
        return jsonify({"message": "user preferences not found"}), 404
    
    return jsonify({"message": "user preferences found", "result": user_preference_schema.dump(query)}), 200


@authenticate_return_auth
def update_user_preference_by_id(user_id, auth_info):
    post_data = request.form if request.form else request.json
    query = db.session.query(UsersPreferences).filter(UsersPreferences.user_id == user_id).first()

    if auth_info.user.role != 'Super Admin' and auth_info.user_id != user_id:
        return jsonify({"message": "forbidden: higher role required to update another user's preferences"}), 403

    if not query:
        return jsonify({"message": "user preferences not found"}), 404
    
    populate_object(query, post_data)

    try:
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to update user preferences"}), 400

    return jsonify({"message": "user preferences updated", "result": user_preference_schema.dump(query)}), 200


@authenticate_return_auth
def delete_user_preference_by_id(user_id, auth_info):
    query = db.session.query(UsersPreferences).filter(UsersPreferences.user_id == user_id).first()

    if auth_info.user.role != 'Super Admin' and auth_info.user_id != user_id:
        return jsonify({"message": "forbidden: higher role required to delete another user's preferences"}), 403    
    
    if not query:
        return jsonify({"message": "user preferences not found"}), 404
    
    try:
        db.session.delete(query)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete user preferences"}), 400

    return jsonify({"message": "user preferences deleted"}), 200