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
        "geometry": fields.Raw(description='Geometria do dado SICAR'),
        'error': fields.String(description='Mensagem de erro', required=False)
    })
