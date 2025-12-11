from flask import Blueprint

import controllers

image = Blueprint('image', __name__)

@image.route('/image', methods=["POST"])
def add_image_route():
    return controllers.add_image()

@image.route('/images', methods=["GET"])
def get_all_images_route():
    return controllers.get_all_images()

@image.route('/image/<image_id>', methods=["GET"])
def get_image_by_id_route(image_id):
    return controllers.get_image_by_id(image_id)

@image.route('/image/delete/<image_id>', methods=["DELETE"])
def delete_image_by_id_route(image_id):
    return controllers.delete_image_by_id(image_id)


