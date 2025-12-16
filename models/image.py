from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
import uuid

from db import db

class Images(db.Model):
    __tablename__ = "Images"

    image_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), unique=True, nullable=False)
    file_path = db.Column(db.String(), nullable=False)
    recipe_id = db.Column(UUID(as_uuid= True), db.ForeignKey("Recipes.recipe_id"), nullable=True)

    recipe = db.relationship("Recipes", back_populates="images")

    def __init__(self, name, file_path, recipe_id):
        self.name = name
        self.file_path = file_path
        self.recipe_id = recipe_id

    def new_image_obj():
        return Images(None, None, None)


class ImagesSchema(ma.Schema):
    class Meta:
        fields = ['image_id', 'name', 'file_path', 'recipe']

    image_id = ma.fields.UUID()
    name = ma.fields.String(required=True)
    file_path = ma.fields.String(required=True)

    recipe = ma.fields.Nested("RecipesSchema", exclude=['images', 'directions', 'ingredients', 'cuisines'])


image_schema = ImagesSchema()
images_schema = ImagesSchema(many=True)