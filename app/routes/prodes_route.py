from flask_restx import Namespace, Resource
from app.service.prodes_service import *
from app.utils import is_valid_uuid, serialize_for_json

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
        result = is_valid_prodes_data(uuid)
        is_valid = bool(result)
        return {"uuid": uuid, "is_valid": is_valid, "data": serialize_for_json(result) if result else None}

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
        if prodes_data:
            return serialize_for_json(prodes_data)
        else:
            return {"error": f"prodes data not found for uuid: {uuid}"}, 404