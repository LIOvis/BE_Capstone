from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import marshmallow as ma
import uuid

from db import db

class Users(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    date_joined = db.Column(db.Date(), default=datetime.today().date())
    role = db.Column(db.String(), default="User")
    is_active = db.Column(db.Boolean(), default=True)

    preferences = db.relationship("UsersPreferences", back_populates="user", cascade="all", uselist=False)
    recipes = db.relationship("Recipes", back_populates="created_by", cascade="all")
    auth = db.relationship("AuthTokens", back_populates="user", cascade="all")

    def __init__(self, username, email, password, date_joined=datetime.today().date(), role="User", is_active=True):
        self.username = username
        self.email = email
        self.password = password
        self.date_joined = date_joined
        self.role = role
        self.is_active = is_active

    def new_user_obj():
        return Users("", "", "", datetime.today().now(), "User", True)


class UsersSchema(ma.Schema):
    class Meta:
        fields = ['user_id', 'username', 'email', 'date_joined', 'role', 'is_active', 'preferences', 'recipes']

    user_id = ma.fields.UUID()
    username = ma.fields.String(required=True)
    email = ma.fields.String(required=True)
    date_joined = ma.fields.Date(dump_default=datetime.today().date())
    role = ma.fields.String(dump_default="User")
    is_active = ma.fields.Boolean(dump_default=True)

    preferences = ma.fields.Nested("UsersPreferencesSchema", only=['display_name'])
    recipes = ma.fields.Nested("RecipesSchema", many=True, exclude=['created_by'])

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
