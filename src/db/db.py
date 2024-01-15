import os
import psycopg2
from psycopg2 import OperationalError
from contextlib import contextmanager

from src.utils.logger import get_logger

log = get_logger(__name__)


def _get_connection_from_env():
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB", "dev")
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")

    return psycopg2.connect(
        host=host,
        port=port,
        dbname=db_name,
        user=user,
        password=password,
    )


@contextmanager
def transaction_scope():
    """
    context manager to easy do transactions.

    with transaction_scope() as cursor:
        cursor.execute(sql, params)

    """
    conn = None
    try:
        conn = _get_connection_from_env()
        log.info("connected successfully")
        conn.autocommit = False

        log.info("starting transaction")
        with conn.cursor() as cursor:
            yield cursor

        log.info("commiting transaction")
        conn.commit()

    except OperationalError as e:
        log.error(f"database operation failed: {e}")
        if conn:
            log.warning("rolling back transaction.")
            conn.rollback()
        raise

    finally:
        if conn:
            log.info("closing connection")
            conn.close()
