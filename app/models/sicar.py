from flask_restx import fields

def get_validate_response_model(api):
    return api.model('ValidateSicarResponse', {
        'cod_imovel': fields.String(description='Código do imóvel'),
        'geometry': fields.String(description='Geometria do imóvel no formato WKB', required=False),
        'is_valid': fields.Boolean(description='Se o dado SICAR é válido'),
        'error': fields.String(description='Mensagem de erro', required=False)
    })

def get_sicar_data_response_model(api):
    return api.model('SicarDataResponse', {
        'cod_imovel': fields.String(description='Código do imóvel'),
        'status_imo': fields.String(description='Status do imóvel'),
        'dat_criaca': fields.String(description='Data de criação'),
        'data_atual': fields.String(description='Data atual'),
        'area': fields.Float(description='Área do imóvel'),
        'condicao': fields.String(description='Condição do imóvel'),
        'uf': fields.String(description='Unidade federativa'),
        'municipio': fields.String(description='Município'),
        'cod_munici': fields.String(description='Código do município'),
        'm_fiscal': fields.String(description='Matrícula fiscal'),
        'tipo_imove': fields.String(description='Tipo de imóvel'),
        'geometry': fields.String(description='Geometria do imóvel no formato WKB', required=False),
        'error': fields.String(description='Mensagem de erro', required=False)
    })
