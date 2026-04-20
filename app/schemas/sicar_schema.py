from marshmallow import Schema, fields, validate

class ValidadeSicarRequestSchema(Schema):
    cod_imovel = fields.Str(
        required=True,
        validate=validate.Length(min=10),
        metadata={"description": "Código do imóvel a ser validado no SICAR"}
    )
    
class SicarIntersectsProdesRequestSchema(Schema):
    cod_imovel = fields.Str(
        required=True,
        validate=validate.Length(min=10),
        metadata={"description": "Código do imóvel do SICAR"}
    )
    uuid = fields.UUID(
        required=True,
        metadata={"description": "UUID do dado PRODES para comparação"}
    )