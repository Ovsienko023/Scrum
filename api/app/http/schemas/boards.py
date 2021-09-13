from marshmallow import Schema, fields, validate


class SchemaCreateBoard(Schema):
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1),
    )
