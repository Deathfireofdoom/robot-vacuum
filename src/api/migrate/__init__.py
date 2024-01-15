from flask import Blueprint

migrate_blueprint = Blueprint("migrate", __name__)


from . import handlers
