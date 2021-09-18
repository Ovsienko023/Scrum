from marshmallow import Schema, fields, validate


class SchemaGetCard(Schema):
    card_id = fields.Int(
        required=True,
        validate=validate.Range(min=1),
    )


class SchemaCreateCard(Schema):
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1),
    )
    description = fields.Str(
        required=False,
        validate=validate.Length(min=1),
        missing=None,
    )
    developer_id = fields.UUID(
        required=True,
    )
    priority_id = fields.UUID(
        required=True,
    )
    status_id = fields.UUID(
        required=True,
    )
    board_id = fields.UUID(
        required=True,
    )
    creator_id = fields.UUID(
        required=True,
    )
    estimates_time = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )
