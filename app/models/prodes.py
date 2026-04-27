from flask_restx import fields

def get_validate_prodes_response_model(api):
    return api.model('ValidateProdesResponse', {
        'uuid': fields.String(description='UUID informado'),
        'is_valid': fields.Boolean(description='Se o dado PRODES é válido'),
        'biome': fields.String(description='Bioma onde o dado PRODES foi encontrado', required=False, example='cerrado'),
        'layer': fields.String(description='Camada onde o dado PRODES foi encontrado', required=False, example='residual')
    })

def get_prodes_data_response_model(api):
    return api.model('ProdesDataResponse', {
        "properties": fields.Raw(description='Propriedades do dado PRODES, exceto a geometria'),
        "type": fields.String(description='No formato GeoJSON (definido pela especificação oficial), geometria + propriedades (attributes) = feature', required=False, example='Feature'),
        "geometry": fields.Raw(description='Geometria do dado PRODES em formato GeoJSON')
    })

# Novo modelo de erro padronizado
def get_error_response_model(api):
    return api.model('ErrorResponse', {
        'errors': fields.Nested(api.model('FieldErrors', {
            'uuid': fields.List(fields.String, description='Lista de erros relacionados ao campo uuid')
        }))
    })
    
def get_error_response_model_404(api):
    return api.model('ErrorResponse404', {
        'error': fields.String(description='Mensagem de erro para recurso não encontrado')
    })