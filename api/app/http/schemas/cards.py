from marshmallow import Schema, fields, validate, validates, ValidationError
from app.native.estimation import EstimationTime
from app.http.constants import STATUSES, PRIORITIES


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
    priority = fields.Str(
        required=True,
        validate=validate.OneOf(PRIORITIES),
    )
    board_id = fields.UUID(
        required=True,
    )
    estimation = fields.Str(
        required=True,
        validate=validate.Length(min=2)
    )

    @validates("estimation")
    def validate_estimation(self, value):
        valid_name = ["h", "d", "w", "m"]
        for row in value:
            if (not row.isdigit()) and (row not in valid_name):
                raise ValidationError("Value error: cannot be converted to hours.")


class SchemaUpdateCard(Schema):
    card_id = fields.Int(
        required=True,
        validate=validate.Range(min=1),
    )
    title = fields.Str(
        required=False,
        validate=validate.Length(min=1),
        missing=None,
    )
    description = fields.Str(
        required=False,
        validate=validate.Length(min=1),
        missing=None,
    )
    developer_id = fields.UUID(
        required=False,
        missing=None,
    )
    priority = fields.Str(
        required=False,
        validate=validate.OneOf(PRIORITIES),
        missing=None,
    )
    status = fields.Str(
        required=False,
        validate=validate.OneOf(STATUSES),
        missing=None,
    )
    board_id = fields.UUID(
        required=False,
        missing=None,
    )
    estimation = fields.Str(
        required=False,
        validate=validate.Length(min=2),
        missing=None,
    )

    @validates("estimation")
    def validate_estimation(self, value) -> int or None:
        if not value:
            return None
        valid_name = ["h", "d", "w", "m"]
        for row in value:
            if (not row.isdigit()) and (row not in valid_name):
                raise ValidationError("Value error: cannot be converted to hours.")


class SchemaGetReport(Schema):
    board_id = fields.UUID(
        required=False,
        missing=None,
    )
    priority = fields.Str(
        required=False,
        validate=validate.OneOf(PRIORITIES),
        missing=None,
    )
    status = fields.Str(
        required=False,
        validate=validate.OneOf(STATUSES),
        missing=None,
    )
    developer_id = fields.UUID(
        required=False,
        missing=None,
    )


class SchemaRemoveCard(Schema):
    card_id = fields.Int(
        required=True,
        validate=validate.Range(min=1),
    )
