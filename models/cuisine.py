from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
import uuid

from db import db

class Cuisines(db.Model):
    __tablename__ = "Cuisines"

    cuisine_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cuisine_name = db.Column(db.String(), unique=True, nullable=False)
    is_active = db.Column(db.Boolean(), default=True)

    recipes = db.relationship("CuisinesRecipes", back_populates="cuisine", cascade="all")

    def __init__(self, cuisine_name, is_active=True):
        self.cuisine_name = cuisine_name
        self.is_active = is_active

    def new_cuisine_obj():
        return Cuisines(None, True)


class CuisinesSchema(ma.Schema):
    class Meta:
        fields = ['cuisine_id', 'cuisine_name', 'is_active', 'recipes']

    cuisine_id = ma.fields.UUID()
    cuisine_name = ma.fields.String(required=True)
    is_active = ma.fields.Boolean(dump_default=True)

    recipes = ma.fields.Nested("CuisinesRecipesSchema", exclude=['cuisine', 'recipe.ingredients'], many=True)


cuisine_schema = CuisinesSchema()
cuisines_schema = CuisinesSchema(many=True)