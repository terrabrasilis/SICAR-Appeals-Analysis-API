from flask_restx import fields

def get_validate_response_model(api):
    return api.model('ValidateSicarResponse', {
        'cod_imovel': fields.String(description='Código do imóvel'),
        'is_valid': fields.Boolean(description='Se o dado SICAR é válido'),
        'error': fields.String(description='Mensagem de erro', required=False)
    })

def get_sicar_data_response_model(api):
    return api.model('SicarDataResponse', {
        "properties": fields.Raw(description='Propriedades do dado SICAR'),
        "type": fields.String(description='No formato GeoJSON (definido pela especificação oficial), geometria + propriedades (attributes) = feature', required=False, example='Feature'),
        "geometry": fields.Raw(description='Geometria do dado SICAR'),
        'error': fields.String(description='Mensagem de erro', required=False)
    })

def get_sicar_intersects_response_model(api):
    properties_model = api.model('SicarIntersectsProperties', {
        "cod_imovel": fields.String(description='Código do imóvel'),
        "uuid": fields.String(description='UUID do dado PRODES'),
        "intersects": fields.Boolean(description='Se as geometrias intersectam')
    })
    return api.model('SicarIntersectsProdesResponse', {
        "properties": fields.Nested(properties_model),
        "type": fields.String(description='No formato GeoJSON (definido pela especificação oficial), geometria + propriedades (attributes) = feature', required=False, example='Feature'),
        "geometry": fields.Raw(description='Geometria da interseção, se houver'),
        'error': fields.String(description='Mensagem de erro', required=False)
    })