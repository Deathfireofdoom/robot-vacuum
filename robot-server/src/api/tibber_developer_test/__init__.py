from flask import Blueprint

tibber_developer_test_blueprint = Blueprint("tibber-developer-test", __name__)


from . import handlers
