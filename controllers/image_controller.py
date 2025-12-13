from flask import current_app, jsonify, request
import os

from models.image import Images, image_schema, images_schema
from lib.authenticate import authenticate_return_auth, authenticate
from util.reflection import populate_object
from models.recipe import Recipes
from db import db


@authenticate_return_auth
def add_image(auth_info):
    if 'image' not in request.files:
        return jsonify({"message": "image is required"}), 400
    
    image_file = request.files["image"]

    if image_file.filename == '':
        return jsonify({"message": "no selected image file"}), 400
    
    post_data = request.form if request.form else request.json

    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_file.filename)
    image_file.save(file_path)

    image_data = {"name": str(image_file.filename), "file_path": str(file_path), "recipe_id": post_data.get("recipe_id")}

    recipe_query = db.session.query(Recipes).filter(Recipes.recipe_id == image_data["recipe_id"]).first()

    if not recipe_query:
        return jsonify({"message": "recipe not found"}), 404
    
    if auth_info.user.role != "Super Admin" and recipe_query.user_id != auth_info.user_id:
        return jsonify({"message": "forbidden: higher role required to add an image to another user's recipe"}), 403
    
    new_image = Images.new_image_obj()

    populate_object(new_image, image_data)

    try:
        db.session.add(new_image)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to add image"}), 400
    
    return jsonify({"message": "image added", "result": image_schema.dump(new_image)}), 201
    

@authenticate_return_auth
def get_all_images(auth_info):
    query = db.session.query(Images).all()

    images = images_schema.dump(query)
    images_list = []

    if auth_info.user.role == "User":
        for image in images:
            if image["recipe"]["is_active"] == True or image["recipe"]["user_id"] == auth_info.user_id:
                images_list.append(image)
    else:
        images_list = images

    return jsonify({"message": "images found", "results": images_list}), 200
    

@authenticate_return_auth
def get_image_by_id(image_id, auth_info):
    query = db.session.query(Images).filter(Images.image_id == image_id).first()

    if not query:
        return jsonify({"message": "image not found"}), 404
    
    if auth_info.user.role == "User" and query.recipe.is_active == False:
        return ({"message": "forbidden: higher role required to view images from another user's inactive recipe"}), 403
    
    return jsonify({"message": "image found", "result": image_schema.dump(query)}), 200


@authenticate_return_auth
def delete_image_by_id(image_id, auth_info):
    query = db.session.query(Images).filter(Images.image_id == image_id).first()

    if auth_info.user.role != "Super Admin" and query.recipe.user_id != auth_info.user_id:
        return jsonify({"message": "forbidden: higher role required to delete an image from another user's recipe"}), 403
    
    if not query:
        return jsonify({"message": "image not found"}), 404
    
    try:
        db.session.delete(query)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete image"}), 400

    return jsonify({"message": "image deleted"}), 200