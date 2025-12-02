from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
import uuid

from db import db

class UserPreferences(db.Model):
    __tablename__ = "UsersPreferences"

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), primary_key=True, default=uuid.uuid4)
    display_name = db.Column(db.String())
    dark_mode = db.Column(db.Boolean(), default=True)

    user = db.relationship("Users", back_populates="preferences")


    def __init__(self, display_name, dark_mode=True):
        self.display_name = display_name
        self.dark_mode = dark_mode

    def new_user_preference_obj():
        return UserPreferences(None, True)


class UserPreferencesSchema(ma.Schema):
    class Meta:
        fields = ['user_id', 'display_name', 'dark_mode', 'user']

    user_id = ma.fields.UUID()
    display_name = ma.fields.String()
    dark_mode = ma.fields.Boolean(dump_default=True)

    user = ma.fields.Nested("UsersSchema", exclude=['user_id', 'preferences'])


user_preference_schema = UserPreferencesSchema()
user_preferences_schema = UserPreferencesSchema(many=True)