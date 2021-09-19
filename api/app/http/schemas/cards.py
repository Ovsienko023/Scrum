from marshmallow import Schema, fields, validate, validates, ValidationError
from app.native.estimation import EstimationTime


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

        hours = EstimationTime().convert_to_hours(times=value)
        return hours
