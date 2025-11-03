"""Pytest fixtures and configuration for test suite.

Provides Flask app client fixture and database connection utilities.
"""

import os
import pytest
import psycopg2
import psycopg2.extras
from pathlib import Path
from app.main import app as flask_app
from app import config


@pytest.fixture(scope="session")
def setup_test_db():
    """Create test database schema once per test session."""
    # Set TESTING environment variable
    os.environ["TESTING"] = "true"

    # Connect to test database
    conn = psycopg2.connect(**config.conn_params)
    conn.autocommit = True
    cursor = conn.cursor()

    try:
        # Create pt schema if it doesn't exist
        cursor.execute("CREATE SCHEMA IF NOT EXISTS pt;")

        # Set search path
        cursor.execute("SET search_path TO pt, public;")

        # Drop existing tables if they exist (clean slate)
        cursor.execute("""
            DROP TABLE IF EXISTS pt.fec_politician_map CASCADE;
            DROP TABLE IF EXISTS pt.Votes CASCADE;
            DROP TABLE IF EXISTS pt.Donations CASCADE;
            DROP TABLE IF EXISTS pt.Donors CASCADE;
            DROP TABLE IF EXISTS pt.Bills CASCADE;
            DROP TABLE IF EXISTS pt.Politicians CASCADE;
        """)

        # Run bootstrap.sql to create schema
        bootstrap_path = Path(__file__).parent.parent / "bin" / "bootstrap.sql"
        with open(bootstrap_path, "r") as f:
            bootstrap_sql = f.read()

        # Execute schema creation
        cursor.execute(bootstrap_sql)

        print("Test database schema created successfully")

    except Exception as e:
        print(f"Error setting up test database: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

    yield

    # Teardown: optionally drop schema after all tests
    # (Commented out to allow inspection after tests)
    # conn = psycopg2.connect(**config.conn_params)
    # conn.autocommit = True
    # cursor = conn.cursor()
    # cursor.execute("DROP SCHEMA IF EXISTS pt CASCADE;")
    # cursor.close()
    # conn.close()


@pytest.fixture
def db_connection(setup_test_db):
    """Provide a database connection for tests."""
    os.environ["TESTING"] = "true"
    conn = psycopg2.connect(**config.conn_params)
    cursor = conn.cursor()
    cursor.execute("SET search_path TO pt, public;")
    conn.commit()
    cursor.close()

    yield conn

    conn.close()


@pytest.fixture
def seed_test_data(db_connection):
    """Seed comprehensive test data before each test."""
    cursor = db_connection.cursor()

    try:
        # Import seed data function
        from tests.fixtures.seed_data import seed_all_data

        seed_all_data(cursor)
        db_connection.commit()
    except Exception as e:
        db_connection.rollback()
        raise e
    finally:
        cursor.close()

    return db_connection


@pytest.fixture(autouse=True)
def clean_db(setup_test_db, request):
    """Clean all tables before each test to ensure isolation."""
    # Skip cleanup for the setup_test_db fixture itself
    if request.node.name == "setup_test_db":
        yield
        return

    conn = psycopg2.connect(**config.conn_params)
    conn.autocommit = True
    cursor = conn.cursor()

    try:
        cursor.execute("SET search_path TO pt, public;")

        # Disable foreign key checks temporarily
        cursor.execute("SET session_replication_role = 'replica';")

        # Truncate all tables
        cursor.execute("""
            TRUNCATE TABLE pt.fec_politician_map CASCADE;
            TRUNCATE TABLE pt.Votes CASCADE;
            TRUNCATE TABLE pt.Donations CASCADE;
            TRUNCATE TABLE pt.Donors CASCADE;
            TRUNCATE TABLE pt.Bills CASCADE;
            TRUNCATE TABLE pt.Politicians CASCADE;
        """)

        # Re-enable foreign key checks
        cursor.execute("SET session_replication_role = 'origin';")

    finally:
        cursor.close()
        conn.close()

    yield


@pytest.fixture
def app():
    """Create and configure a Flask app instance for testing."""
    os.environ["TESTING"] = "true"
    flask_app.config.update(
        {
            "TESTING": True,
        }
    )
    yield flask_app


@pytest.fixture
def client(app):
    """Create a test client for the Flask app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner for the Flask app."""
    return app.test_cli_runner()
