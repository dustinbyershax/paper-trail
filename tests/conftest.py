"""Pytest fixtures and configuration for test suite.

Provides Flask app client fixture and database connection utilities.
"""

import os
from pathlib import Path
from subprocess import run

import pytest
import psycopg2

# CRITICAL: Set TESTING environment variable BEFORE importing config
# This ensures config.py uses the test database
os.environ["TESTING"] = "true"

from app.main import app as flask_app
from app import config


# Test database configuration
DUMP_ARCHIVE = Path(__file__).parent.parent / "bin" / "pg-dump.tar.bz2"

# Test tables in dependency order (for DROP/TRUNCATE operations)
TABLES = [
    "pt.fec_politician_map",
    "pt.Votes",
    "pt.Donations",
    "pt.Donors",
    "pt.Bills",
    "pt.Politicians",
]


def verify_test_database():
    """Ensure we're using the test database to prevent data loss."""
    if config.conn_params["dbname"] != "paper_trail_test":
        raise RuntimeError(
            f"SAFETY: Tests attempted to use '{config.conn_params['dbname']}'. "
            "Only 'paper_trail_test' is allowed. Set TESTING=true in environment."
        )


def restore_schema_from_dump(cursor):
    """Extract and restore database schema from pg_dump archive."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        # Extract dump file
        run(["tar", "-xjf", str(DUMP_ARCHIVE), "-C", tmpdir], check=True, capture_output=True)
        dump_file = Path(tmpdir) / "paper-trail-dump"

        if not dump_file.exists():
            raise FileNotFoundError(
                f"Expected 'paper-trail-dump' in {DUMP_ARCHIVE}"
            )

        # Read SQL dump and parse statements
        with dump_file.open() as f:
            dump_content = f.read()

        # Parse SQL statements from dump (schema only, no data)
        schema_statements = []
        current_statement = []
        in_data_section = False

        for line in dump_content.split("\n"):
            # Skip COPY data sections
            if line.startswith("COPY ") or line.startswith("\\copy "):
                in_data_section = True
                continue
            if line.strip() == "\\.":
                in_data_section = False
                continue
            if in_data_section:
                continue

            # Skip comments and empty lines at statement boundaries
            stripped = line.strip()
            if not stripped or stripped.startswith("--"):
                if stripped.endswith(";"):
                    # End of statement with comment
                    if current_statement:
                        statement = "\n".join(current_statement).strip()
                        if statement:
                            schema_statements.append(statement)
                        current_statement = []
                continue

            # Accumulate statement lines
            current_statement.append(line)

            # Execute when we hit a semicolon
            if stripped.endswith(";"):
                statement = "\n".join(current_statement).strip()
                if statement:
                    # Replace public schema with pt schema
                    statement = statement.replace("public.", "pt.")
                    # Only include schema creation statements
                    if any(
                        statement.upper().startswith(cmd)
                        for cmd in [
                            "CREATE TABLE",
                            "ALTER TABLE",
                            "CREATE INDEX",
                            "CREATE UNIQUE INDEX",
                            "CREATE SEQUENCE",
                            "ALTER SEQUENCE",
                        ]
                    ):
                        schema_statements.append(statement)
                current_statement = []

        # Execute schema statements in order
        for statement in schema_statements:
            # Skip OWNER TO statements (roles may not exist in test environment)
            if "OWNER TO" in statement.upper():
                continue

            try:
                cursor.execute(statement)
            except psycopg2.Error as e:
                # Ignore "already exists" and "does not exist" errors for robustness
                error_str = str(e).lower()
                if "already exists" not in error_str and "does not exist" not in error_str:
                    raise


@pytest.fixture(scope="session")
def setup_test_db():
    """Create test database schema once per test session."""
    verify_test_database()

    conn = psycopg2.connect(**config.conn_params)
    conn.autocommit = True
    cursor = conn.cursor()

    try:
        # Create schema
        cursor.execute("CREATE SCHEMA IF NOT EXISTS pt")
        cursor.execute("SET search_path TO pt, public")

        # Drop existing tables
        for table in TABLES:
            cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")

        # Restore schema from dump
        restore_schema_from_dump(cursor)

        print("Test database schema created successfully")

    finally:
        cursor.close()
        conn.close()

    yield

    # Teardown: optionally drop schema after all tests
    # (Commented out to allow inspection after tests)


@pytest.fixture
def db_connection(setup_test_db):
    """Provide a database connection for tests."""
    conn = psycopg2.connect(**config.conn_params)
    cursor = conn.cursor()
    cursor.execute("SET search_path TO pt, public")
    conn.commit()
    cursor.close()

    yield conn

    conn.close()


@pytest.fixture
def clean_db(db_connection):
    """Clear all tables before test to ensure isolation.

    Use this fixture when you need a clean database state.
    """
    cursor = db_connection.cursor()

    try:
        cursor.execute(
            f"TRUNCATE TABLE {', '.join(TABLES)} RESTART IDENTITY CASCADE"
        )
        db_connection.commit()
    finally:
        cursor.close()

    yield db_connection


@pytest.fixture
def seed_test_data(clean_db):
    """Seed comprehensive test data before test.

    Automatically cleans database first via clean_db dependency.
    """
    from tests.fixtures.seed_data import seed_all_data

    cursor = clean_db.cursor()

    try:
        seed_all_data(cursor)
        clean_db.commit()
    except Exception as e:
        clean_db.rollback()
        raise
    finally:
        cursor.close()

    return clean_db


@pytest.fixture
def app():
    """Create and configure a Flask app instance for testing."""
    flask_app.config["TESTING"] = True
    return flask_app


@pytest.fixture
def client(app):
    """Create a test client for the Flask app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner for the Flask app."""
    return app.test_cli_runner()
