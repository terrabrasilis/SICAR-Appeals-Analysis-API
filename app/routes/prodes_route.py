from flask_restx import Namespace, Resource
from app.service.prodes_service import *
from app.schemas.prodes_schema import ProdesValidateDataRequestSchema
from marshmallow import ValidationError

from app.models.prodes import *

api = Namespace('prodes', description='Operações relacionadas ao PRODES')
validate_response = get_validate_prodes_response_model(api)
prodes_data_response = get_prodes_data_response_model(api)
error_response = get_error_response_model(api)
error_response_404 = get_error_response_model_404(api)

prodes_validate_schema = ProdesValidateDataRequestSchema()

@api.route('/validate/<string:uuid>')
@api.doc(params={'uuid': 'UUID do dado PRODES'})
class ValidateProdes(Resource):
    @api.response(200, 'Success', validate_response)
    @api.response(400, 'UUID inválido', error_response)
    def get(self, uuid):
        """Valida se o UUID informado é válido e se existe dado PRODES correspondente."""
        try:
            data = prodes_validate_schema.load({"uuid": uuid})
            return validate_prodes_data(str(data["uuid"]))
        except ValidationError as err:
            return {"errors": err.messages}, 400

@api.route('/<string:uuid>')
@api.doc(params={'uuid': 'UUID do dado PRODES'})
class GetProdesByUUID(Resource):

    @api.response(200, 'Success', prodes_data_response)
    @api.response(400, 'UUID inválido', error_response)
    @api.response(404, 'Dado não encontrado', error_response_404)
    def get(self, uuid):
        """Obtém dados PRODES pelo UUID informado."""
        try:
            data = prodes_validate_schema.load({"uuid": uuid})
            prodes_data = get_prodes_data_by_uuid(str(data["uuid"]))

            if prodes_data:
                return prodes_data, 200

            return {
                "error": f"Dado PRODES não encontrado para UUID: {uuid}"
            }, 404

        except ValidationError as err:
            return {
                "errors": err.messages
            }, 400