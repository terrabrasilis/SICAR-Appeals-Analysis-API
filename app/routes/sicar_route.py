

from flask import request
from flask_restx import Namespace, Resource
from app.service.sicar_service import *
from app.models.sicar import get_validate_response_model, get_sicar_data_response_model

api = Namespace('sicar', description='Operações relacionadas ao SICAR')

validate_response = get_validate_response_model(api)
sicar_data_response = get_sicar_data_response_model(api)

@api.route('/validate/<string:cod_imovel>')
@api.doc(params={'cod_imovel': 'Código do imóvel'})
class ValidateSicar(Resource):
    @api.response(200, 'Success', validate_response)
    def get(self, cod_imovel):
        """Valida se o código do imóvel informado é válido no SICAR."""
        is_valid = validate_sicar_data(cod_imovel)
        return {"cod_imovel": cod_imovel, "is_valid": is_valid}

@api.route('/<string:cod_imovel>')
@api.doc(params={'cod_imovel': 'Código do imóvel'})
class GetSicarByCodImovel(Resource):
    @api.response(200, 'Success', sicar_data_response)
    @api.response(404, 'Dado não encontrado', sicar_data_response)
    def get(self, cod_imovel):
        """Obtém dados SICAR pelo código do imóvel informado."""
        sicar_data = get_sicar_data_by_cod_imovel(cod_imovel)
        return sicar_data if sicar_data else {"error": "Dado não encontrado para o código do imóvel informado."}, 404
        
@api.route('/geometries_intersects')
@api.doc(params={'cod_imovel': 'Código do imóvel', 'uuid': 'UUID do dado PRODES'})
class SicarIntersectsProdes(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Invalid input')
    def get(self):
        """Verifica se a geometria do SICAR intersecta com a geometria do PRODES."""
        cod_imovel = request.args.get('cod_imovel')
        uuid = request.args.get('uuid')

        if not cod_imovel or not uuid:
            return {"error": "Tanto cod_imovel quanto uuid são obrigatórios."}, 400

        intersects = sicar_intersects_prodes(cod_imovel, uuid)
        return intersects