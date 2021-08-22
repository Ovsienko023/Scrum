from marshmallow import Schema, fields


class SchemaCreateUser(Schema):
    name = fields.Str()
    password = fields.Date()
