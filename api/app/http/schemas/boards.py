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


class SchemaUpdateBoard(Schema):
    board_id = fields.UUID(
        required=True,
    )

    title = fields.Str(
        required=True,
        validate=validate.Length(min=1),
    )


class SchemaRemoveBoard(Schema):
    board_id = fields.UUID(
        required=True,
    )
