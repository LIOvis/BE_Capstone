from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
import uuid

from db import db

class Cuisines(db.Model):
    __tablename__ = "Cuisines"

    cuisine_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cuisine_name = db.Column(db.String(), unique=True, nullable=False)

    recipes = db.relationship("CuisinesRecipes", back_populates="cuisine", cascade="all")

    def __init__(self, cuisine_name):
        self.cuisine_name = cuisine_name

    def new_user_preference_obj():
        return Cuisines("")


class CuisinesSchema(ma.Schema):
    class Meta:
        fields = ['cuisine_id', 'cuisine_name', 'recipes']

    cuisine_id = ma.fields.UUID()
    cuisine_name = ma.fields.String(required=True)

    recipes = ma.fields.Nested("CuisinesRecipesSchema", exclude=['cuisine'], many=True)


cuisine_schema = CuisinesSchema()
cuisines_schema = CuisinesSchema(many=True)