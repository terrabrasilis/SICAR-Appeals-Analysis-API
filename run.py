from flask import Flask
from flask_restx import Api
from app.routes.sicar_route import api as sicar_ns
from app.routes.prodes_route import api as prodes_ns

app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='SICAR & PRODES API',
    description='API para análise de recursos SICAR e PRODES',
    doc='/docs'
)

api.add_namespace(sicar_ns, path='/sicar')
api.add_namespace(prodes_ns, path='/prodes')