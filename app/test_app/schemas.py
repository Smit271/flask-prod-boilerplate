from marshmallow import Schema, fields, validate

class TestModelSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
