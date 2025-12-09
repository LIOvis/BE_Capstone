from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
import uuid

from db import db

class Recipes(db.Model):
    __tablename__ = "Recipes"

    recipe_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"))
    recipe_name = db.Column(db.String(), nullable=False)
    prep_time = db.Column(db.Integer())
    cook_time = db.Column(db.Integer())
    directions = db.Column(db.String(), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)

    created_by = db.relationship("Users", back_populates="recipes")
    cuisines = db.relationship("CuisinesRecipes", back_populates="recipe", cascade="all"),
    ingredients = db.relationship("RecipesIngredients", back_populates="recipe", cascade="all")
    images = db.relationship("Images", backpopulates="recipe", cascade="all")


    def __init__(self, user_id, recipe_name, prep_time, cook_time, directions, is_active=True):
        self.user_id = user_id
        self.recipe_name = recipe_name
        self.prep_time = prep_time
        self.cook_time = cook_time
        self.directions = directions
        self.is_active = is_active

    def new_recipe_obj():
        return Recipes("", "", None, None, "", True)


class RecipesSchema(ma.Schema):
    class Meta:
        fields = ['recipe_id', 'recipe_name', 'prep_time', 'cook_time', 'directions', 'is_active', 'created_by', 'cuisines', 'ingredients', 'images']

    recipe_id = ma.fields.UUID()
    recipe_name = ma.fields.String(required=True)
    prep_time = ma.fields.Integer()
    cook_time = ma.fields.Integer()
    directions = ma.fields.String(required=True)
    is_active = ma.fields.Boolean(dump_default=True)

    created_by = ma.fields.Nested("UsersSchema", only=['user_id', 'username', 'preferences'])
    cuisines = ma.fields.Nested("CuisinesRecipesSchema", exclude=['recipe'], many=True)
    ingredients = ma.fields.Nested("RecipesIngredientsSchema", exclude=['recipe'], many=True)
    images = ma.fields.Nested("ImagesSchema", exclude=['recipe'], many=True)


recipe_schema = RecipesSchema()
recipes_schema = RecipesSchema(many=True)