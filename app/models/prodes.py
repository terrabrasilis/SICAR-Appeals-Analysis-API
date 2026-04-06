from flask_restx import fields

def get_validate_prodes_response_model(api):
    return api.model('ValidateProdesResponse', {
        'uuid': fields.String(description='UUID informado'),
        'is_valid': fields.Boolean(description='Se o dado PRODES é válido'),
        'data': fields.Raw(description='Dados PRODES', required=False),
        'error': fields.String(description='Mensagem de erro', required=False)
    })

def get_prodes_data_response_model(api):
    return api.model('ProdesDataResponse', {
        'uuid': fields.String(description='UUID consultado', required=False),
        'table': fields.String(
            description='Tabela de origem do dado (ex: prodes_cerrado, prodes_amazonia, etc.)',
            required=False
        ),
        'biome': fields.String(description='Bioma consultado', required=False),
        'data': fields.Raw(
            description='Payload retornado pela tabela de origem (estrutura pode variar)',
            required=False
        ),
        'error': fields.String(description='Mensagem de erro', required=False)
    })
