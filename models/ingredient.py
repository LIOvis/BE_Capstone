from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
import uuid

from db import db

class Ingredients(db.Model):
    __tablename__ = "Ingredients"

    ingredient_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ingredient_name = db.Column(db.String(), unique=True, nullable=False)
    is_active = db.Column(db.Boolean(), default=True)

    recipes = db.relationship("RecipesIngredients", back_populates="ingredient", cascade="all")

    def __init__(self, ingredient_name, is_active=True):
        self.ingredient_name = ingredient_name
        self.is_active = is_active

    def new_ingredient_obj():
        return Ingredients(None, True)


class IngredientsSchema(ma.Schema):
    class Meta:
        fields = ['ingredient_id', 'ingredient_name', 'is_active', 'recipes']

    ingredient_id = ma.fields.UUID()
    ingredient_name = ma.fields.String(required=True)
    is_active = ma.fields.Boolean(dump_default=True)

    recipes = ma.fields.Nested("RecipesIngredientsSchema", exclude=['ingredient'], many=True)


ingredient_schema = IngredientsSchema()
ingredients_schema = IngredientsSchema(many=True)