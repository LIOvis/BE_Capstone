from flask_bcrypt import generate_password_hash
from flask import jsonify, request

from models.user import Users, user_schema, users_schema
from lib.authenticate import authenticate_return_auth, authenticate
from util.reflection import populate_object
from db import db



def add_user():
    post_data = request.form if request.form else request.json

    new_user = Users.new_user_obj()

    populate_object(new_user, post_data)
    
    if 'password' in post_data:
        new_user.password = generate_password_hash(new_user.password).decode('utf8')

    if 'role' in post_data:
        if new_user.role not in ['User', 'Admin', 'Super Admin']:
            return jsonify({"message": "role must be User, Admin, or Super Admin (case sensitive)"}), 400

    try:
        db.session.add(new_user)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "unable to add user", "error": str(e)}), 400
    
    return jsonify({"message": "user added", "result": user_schema.dump(new_user)}), 201
    

@authenticate_return_auth
def get_all_users(auth_info):
    query = db.session.query(Users).all()

    if auth_info.user.role == "User":
        query = db.session.query(Users).filter(Users.is_active == True)

        users = users_schema.dump(query)

        for user in users:
            active_recipes = []
            for recipe in user.recipes:
                if recipe.is_active == True:
                    active_recipes.append(recipe)
            user["recipes"] = active_recipes

        return jsonify({"message": "users found", "results": users})

    return jsonify({"message": "users found", "results": users_schema.dump(query)}), 200
    

@authenticate_return_auth
def get_user_by_id(user_id, auth_info):
    query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if user_id != auth_info.user_id and auth_info.user.role == 'User':
        return jsonify({"message": "forbidden: higher role required to view another user"}), 403

    if not query:
        return jsonify({"message": "user not found"}), 404
        
    return jsonify({"message": "user found", "result": user_schema.dump(query)}), 200


@authenticate_return_auth
def get_logged_in_user(auth_info):
    query = db.session.query(Users).filter(Users.user_id == auth_info.user_id)

    return jsonify ({"message": "user profile found", "result": user_schema.dump(query)})


@authenticate_return_auth
def update_user_by_id(user_id, auth_info):
    post_data = request.form if request.form else request.json
    query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if auth_info.user.role == 'User':
        return jsonify({"message": "forbidden: higher role required to update another user"}), 403

    if not query:
        return jsonify({"message": "user not found"}), 404
    
    if 'role' in post_data:
        if auth_info.user.role != "Super Admin":
            return jsonify({"message": "forbidden: higher role required to change a user's role"}), 400
        
        if post_data.get("role") not in ['User', 'Admin', 'Super Admin']:
            return jsonify({"message": "role must be User, Admin, or Super Admin (case sensitive)"}), 400
    
    populate_object(query, post_data)

    try:
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to update user"}), 400

    return jsonify({"message": "user updated", "result": user_schema.dump(query)}), 200


@authenticate_return_auth
def delete_user_by_id(user_id, auth_info):
    query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if auth_info.user_id != user_id and auth_info.user.role != "Super Admin":
        return jsonify({"message": "forbidden: higher role required to delete another user"}), 403
    
    if not query:
        return jsonify({"message": "user not found"}), 404
    
    try:
        db.session.delete(query)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete user"}), 400

    return jsonify({"message": "user deleted"}), 200