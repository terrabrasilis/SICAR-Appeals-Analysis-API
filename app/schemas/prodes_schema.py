from marshmallow import Schema, fields, validate

class ProdesValidateDataRequestSchema(Schema):
    uuid = fields.UUID(
        required=True,
        metadata={"description": "UUID do dado PRODES a ser validado"}
    )