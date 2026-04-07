from flask_restx import Namespace, Resource
from app.service.prodes_service import *
from app.utils import is_valid_uuid

from app.models.prodes import get_validate_prodes_response_model, get_prodes_data_response_model

api = Namespace('prodes', description='Operações relacionadas ao PRODES')
validate_response = get_validate_prodes_response_model(api)
prodes_data_response = get_prodes_data_response_model(api)

@api.route('/validate/<string:uuid>')
@api.doc(params={'uuid': 'UUID do dado PRODES'})
class ValidateProdes(Resource):
    @api.response(200, 'Success', validate_response)
    @api.response(400, 'UUID inválido', validate_response)
    def get(self, uuid):
        """Valida se o UUID informado é válido e se existe dado PRODES correspondente."""
        is_uuid = is_valid_uuid(uuid)
        if not is_uuid:
            return {"error": f"Invalid UUID format: {uuid}"}, 400
        return validate_prodes_data(uuid)

@api.route('/<string:uuid>')
@api.doc(params={'uuid': 'UUID do dado PRODES'})
class GetProdesByUUID(Resource):
    @api.response(200, 'Success', prodes_data_response)
    @api.response(400, 'UUID inválido', prodes_data_response)
    @api.response(404, 'Dado não encontrado', prodes_data_response)
    def get(self, uuid):
        """Obtém dados PRODES pelo UUID informado."""
        is_uuid = is_valid_uuid(uuid)
        if not is_uuid:
            return {"error": f"Invalid UUID format: {uuid}"}, 400
        prodes_data = get_prodes_data_by_uuid(uuid)
        return prodes_data if prodes_data else {"error": f"Dado PRODES não encontrado para UUID: {uuid}"}, 404