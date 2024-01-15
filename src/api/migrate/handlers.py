from flask import jsonify
from . import migrate_blueprint

from src.repositories.job_result_repository import JobResultRepository

from src.utils.logger import get_logger

log = get_logger("migrate")


@migrate_blueprint.route("/<version>/<direction>", methods=["GET"])
def migrate(version, direction):
    # The logging is not perfect, since it will theory upgrade "down" to version - 1, not "down" to version.
    log.info(f"migrating to version {version} direction {direction}")

    job_result_repository = JobResultRepository()
    job_result_repository._migrate(version=version, direction=direction)

    return jsonify({"message": f"successful migrated {direction} to {version}"})
