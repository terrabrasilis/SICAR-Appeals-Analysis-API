from flask_restx import fields

def get_validate_prodes_response_model(api):
    return api.model('ValidateProdesResponse', {
        'uuid': fields.String(description='UUID informado'),
        'is_valid': fields.Boolean(description='Se o dado PRODES é válido'),
        'biome': fields.String(description='Bioma onde o dado PRODES foi encontrado', required=False, example='cerrado'),
        'layer': fields.String(description='Camada onde o dado PRODES foi encontrado', required=False, example='residual'),
        'error': fields.String(description='Mensagem de erro', required=False)
    })

def get_prodes_data_response_model(api):
    return api.model('ProdesDataResponse', {
        "properties": fields.Raw(description='Propriedades do dado PRODES, exceto a geometria'),
        "geometry": fields.Raw(description='Geometria do dado PRODES em formato GeoJSON'),
        'error': fields.String(description='Mensagem de erro', required=False)
    })
