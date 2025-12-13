from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
import uuid

from db import db

class CuisinesRecipes(db.Model):
    __tablename__ = "CuisinesRecipes"

    cuisine_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Cuisines.cuisine_id"), primary_key=True)
    recipe_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Recipes.recipe_id"), primary_key=True)

    cuisine = db.relationship("Cuisines", back_populates="recipes")
    recipe = db.relationship("Recipes", back_populates="cuisines")

    def __init__(self, cuisine_id, recipe_id):
        self.cuisine_id = cuisine_id
        self.recipe_id = recipe_id

    def new_recipe_cuisine_obj():
        return CuisinesRecipes(None, None)


class CuisinesRecipesSchema(ma.Schema):
    class Meta:
        fields = ['recipe', 'cuisine']

    cuisine = ma.fields.Nested("CuisinesSchema", exclude=['recipes'])
    recipe = ma.fields.Nested("RecipesSchema", exclude=['cuisines', 'directions', 'images'])


cuisine_recipe_schema = CuisinesRecipesSchema()
cuisines_recipes_schema = CuisinesRecipesSchema(many=True)