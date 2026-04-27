from flask_restx import fields

def get_validate_response_model(api):
    return api.model('ValidateSicarResponse', {
        'cod_imovel': fields.String(description='Código do imóvel'),
        'is_valid': fields.Boolean(description='Se o dado SICAR é válido')
    })

def get_sicar_data_response_model(api):
    return api.model('SicarDataResponse', {
        "properties": fields.Raw(description='Propriedades do dado SICAR'),
        "type": fields.String(description='No formato GeoJSON (definido pela especificação oficial), geometria + propriedades (attributes) = feature', required=False, example='Feature'),
        "geometry": fields.Raw(description='Geometria do dado SICAR')
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
        "geometry": fields.Raw(description='Geometria da interseção, se houver')
    })

def get_error_response_model_404(api):
    return api.model('SicarErrorResponse404', {
        'error': fields.String(description='Mensagem de erro')
    }) 

def get_error_response_model(api):
    return api.model('SicarErrorResponse', {
        'errors': fields.Nested(api.model('FieldErrors', {
            'cod_imovel': fields.List(fields.String, description='Lista de erros relacionados ao campo cod_imovel')
        }))
    })
    
def get_sicar_intersects_response_error_model(api):
    return api.model('SicarIntersectsErrorResponse', {
        'errors': fields.Nested(api.model('FieldErrors', {
            'cod_imovel': fields.List(fields.String, description='Lista de erros relacionados ao campo cod_imovel'),
            'uuid': fields.List(fields.String, description='Lista de erros relacionados ao campo uuid')
        }))
    })