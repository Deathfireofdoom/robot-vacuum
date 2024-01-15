from flask import Blueprint
from .health import health_blueprint
from .tibber_developer_test import tibber_developer_test_blueprint
from .migrate import migrate_blueprint


api_blueprint = Blueprint("api", __name__)
api_blueprint.register_blueprint(health_blueprint, url_prefix="/health")
api_blueprint.register_blueprint(
    tibber_developer_test_blueprint, url_prefix="/tibber-developer-test"
)
api_blueprint.register_blueprint(migrate_blueprint, url_prefix="/migrate")
