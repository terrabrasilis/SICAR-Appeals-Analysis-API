

from flask import request
from flask_restx import Namespace, Resource
from app.schemas.sicar_schema import ValidadeSicarRequestSchema, SicarIntersectsProdesRequestSchema
from app.service.sicar_service import validate_sicar_data, get_sicar_data_by_cod_imovel, sicar_intersects_prodes
from app.models.sicar import *

from marshmallow import ValidationError

api = Namespace('sicar', description='Operações relacionadas ao SICAR')

validate_response = get_validate_response_model(api)
sicar_data_response = get_sicar_data_response_model(api)
sicar_intersects_prodes_response = get_sicar_intersects_response_model(api)
error_response = get_error_response_model(api)
sicar_intersects_error_response = get_sicar_intersects_response_error_model(api)
sicar_error_404_response = get_error_response_model_404(api)

sicar_schema = ValidadeSicarRequestSchema()
sicar_intersects_schema = SicarIntersectsProdesRequestSchema()

@api.route('/validate/<string:cod_imovel>')
@api.doc(params={'cod_imovel': 'Código do imóvel'})
class ValidateSicar(Resource):

    @api.response(200, 'Success', validate_response)
    @api.response(400, 'Código do imóvel inválido', error_response)
    def get(self, cod_imovel):
        """Valida se o código do imóvel informado é válido no SICAR."""
        try:
            data = sicar_schema.load({"cod_imovel": cod_imovel})
            is_valid = validate_sicar_data(data["cod_imovel"])
            return {
                "cod_imovel": data["cod_imovel"],
                "is_valid": is_valid
            }
        except ValidationError as err:
            return {"errors": err.messages}, 400

@api.route('/<string:cod_imovel>')
@api.doc(params={'cod_imovel': 'Código do imóvel'})
class GetSicarByCodImovel(Resource):
    @api.response(200, 'Success', sicar_data_response)
    @api.response(400, 'Código do imóvel inválido', error_response)
    @api.response(404, 'Dado não encontrado', sicar_error_404_response)
    def get(self, cod_imovel):
        """Obtém dados SICAR pelo código do imóvel informado."""
        try:
            data = sicar_schema.load({"cod_imovel": cod_imovel})
            sicar_data = get_sicar_data_by_cod_imovel(data["cod_imovel"])
            if sicar_data:
                return sicar_data, 200
            return {"error": "Dado não encontrado para o código do imóvel informado."}, 404
        except ValidationError as err:
            return {"errors": err.messages}, 400
        
@api.route('/geometries_intersects')
@api.doc(params={'cod_imovel': 'Código do imóvel', 'uuid': 'UUID do dado PRODES'})
class SicarIntersectsProdes(Resource):

    @api.response(200, 'Success', sicar_intersects_prodes_response)
    @api.response(400, 'Invalid input', sicar_intersects_error_response)
    def get(self):
        """Verifica se a geometria do SICAR intersecta com a geometria do PRODES."""

        try:
            cod_imovel = request.args.get('cod_imovel')
            uuid = request.args.get('uuid')

            data = sicar_intersects_schema.load({
                "cod_imovel": cod_imovel,
                "uuid": uuid
            })

            intersects = sicar_intersects_prodes(
                data["cod_imovel"],
                str(data["uuid"])
            )

            return intersects

        except ValidationError as err:
            return {"errors": err.messages}, 400