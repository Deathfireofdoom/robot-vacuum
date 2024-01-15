from flask import jsonify
from . import health_blueprint


@health_blueprint.route("", methods=["GET"])
def get_general_health():
    return jsonify({"message": "api is reachable"})
