from marshmallow import Schema, fields, validate


class SchemaGetBoard(Schema):
    board_id = fields.UUID(
        required=True,
    )


class SchemaCreateBoard(Schema):
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1),
    )
