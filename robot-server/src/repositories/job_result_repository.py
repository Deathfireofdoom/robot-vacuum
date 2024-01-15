from src.db.db import transaction_scope

from src.models.job_results import JobResult

from src.utils.logger import get_logger

log = get_logger(__name__)

MIGRATION_FILES = {
    "1": {
        "up": """
        CREATE TABLE IF NOT EXISTS job_results (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT NOW(),
            commands INT NOT NULL,
            result INT NOT NULL,
            duration DECIMAL NOT NULL
        );
        """,
        "down": "DROP TABLE job_results CASCADE;",
    }
}


class JobResultRepository:
    @staticmethod
    def insert_job_result(job_result: JobResult) -> JobResult:
        sql = """INSERT INTO job_results (commands, result, duration) VALUES (%s, %s, %s) RETURNING id, timestamp"""
        parameters = [job_result.commands, job_result.result, job_result.duration]

        with transaction_scope() as cursor:
            cursor.execute(sql, parameters)
            _id, timestamp = cursor.fetchone()

        job_result._id = _id
        job_result.timestamp = timestamp.isoformat()

        return job_result

    @staticmethod
    def _migrate(version: str, direction: str):
        """
        # NOTE: this is only a dev-tool-function, nothing that should be done in the real world.
        """
        sql = MIGRATION_FILES[version][direction]

        with transaction_scope() as cursor:
            cursor.execute(sql)
