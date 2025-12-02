from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
import uuid

from db import db

class RecipesIngredients(db.Model):
    __tablename__ = "RecipesIngredients"

    recipe_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Recipes.recipe_id"), primary_key=True)
    ingredient_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Ingredients.ingredient_id"), primary_key=True)
    measurement = db.Column(db.String(), nullable=False)

    recipe = db.relationship("Recipes", back_populates="ingredients")
    ingredient = db.relationship("Ingredients", back_populates="recipes")

    def __init__(self, recipe_id, ingredient_id, measurement):
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id
        self.measurement = measurement

    def new_user_preference_obj():
        return RecipesIngredients("", "", "")


class RecipesIngredientsSchema(ma.Schema):
    class Meta:
        fields = ['measurement', 'recipe', 'ingredient']

    measurement = ma.fields.String(required=True)

    recipe = ma.fields.Nested("RecipesSchema", exclude=['ingredients', 'directions'])
    ingredient = ma.fields.Nested("IngredientsSchema", exclude=['recipes'])


recipe_ingredient_schema = RecipesIngredientsSchema()
recipes_ingredients_schema = RecipesIngredientsSchema(many=True)