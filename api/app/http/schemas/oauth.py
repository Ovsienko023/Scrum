from marshmallow import Schema, fields, validate


class SchemaGetToken(Schema):
    login = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=256),
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=256),
    )
