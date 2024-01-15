from flask import jsonify, request
from dataclasses import asdict

from . import tibber_developer_test_blueprint

from src.models.job import Job
from src.robot.robot import Robot

from src.utils.logger import get_logger

log = get_logger("tibber-endpoint")


@tibber_developer_test_blueprint.route("/enter-path", methods=["POST"])
def post_job():
    body = request.get_json()
    if not body:
        return jsonify({"message": "body is missing"}), 400

    try:
        job = Job.from_dict(_dict=body)
    except TypeError as e:
        log.warning(e)
        return jsonify({"message": "bad payload"}), 400
    except ValueError as e:
        log.warning(e)
        return jsonify({"message": "bad payload"}), 400

    try:
        robot = Robot()
        job_result = robot.handle_job(job=job)

        return jsonify(asdict(job_result)), 200
    
    except Exception as e:
        log.warning(e)
        return jsonify ({'message': 'server error'}), 500
