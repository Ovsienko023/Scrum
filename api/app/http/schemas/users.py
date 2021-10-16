from marshmallow import Schema, fields, validate


class SchemaCreateUser(Schema):
    display_name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=256),
    )
    login = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=256),
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=256),
    )
