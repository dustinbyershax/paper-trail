REPOSITORY TREE
```
paper-trail/
├── .dev.env
├── .gitignore
├── README.md
├── requirements.txt
├── app/
└── ├── __init__.py
    ├── config.py
    ├── main.py
    └── templates/
        ├──.gitkeep
        ├── donor_search.html
        └── index.html
└── bin/
    ├── bootstrap.sql
    ├── build_fec_map.py
    ├── load_sql.py
    ├── populate_bills.py
    ├── populate_donors_and_donations.py
    ├── populate_industries.py
    ├── populate_politicians.py
    ├── populate_votes.py
    └── sql_data.tar.bz2
└── frontend/
    ├── src/
    ├── package.json
    ├── vite.config.ts
    └── README.md
```

## Local dev set up instructions

**todo** add postgres install or container install instructions and .env

Create and activate virtual environment

`python -m venv env`

linux/mac   
`source env/bin/activate`  

windows  
`source env/Scripts/activate`

install requirements  
`pip install -r requirements.txt`  

rename `.dev.env` > `.env` and update with your local values.

launch application
`python -m app.main`

## Frontend Development

The frontend is a React 19.2 TypeScript application built with Vite.

### Setup
```bash
cd frontend
pnpm install
pnpm run dev  # Development server on http://localhost:5173
```

### Development Workflow
1. Start Flask backend: `python -m app.main` (port 5001)
2. Start Vite dev server: `cd frontend && pnpm run dev` (port 5173)
3. Open http://localhost:5173 in browser

**Note:** Flask runs on port 5001 to avoid conflicts with macOS AirPlay Receiver.

See `frontend/README.md` for detailed documentation.

## Running Tests

The project uses [pytest](https://docs.pytest.org/) for testing. The test suite includes comprehensive unit tests for all API endpoints, with fixtures for database setup and test data seeding.

### Prerequisites for Testing

Before running tests, you need:

1. A PostgreSQL database server running (same as for development)
2. A separate test database that will be automatically created
3. Your `.env` file configured with database credentials

The test suite will automatically:
- Create a test database named `paper_trail_test`
- Run the database schema creation from `bin/bootstrap.sql`
- Seed test data before each test
- Clean up data between tests to ensure isolation

### Running the Tests

With your virtual environment activated and requirements installed:

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests for a specific file
pytest tests/test_api_bills.py

# Run a specific test class or function
pytest tests/test_api_bills.py::TestBillSubjects::test_get_subjects_returns_list

# Run tests with coverage report
pytest --cov=app --cov-report=html

# Run tests and show print statements
pytest -s
```

### Test Structure

The test suite is organized as follows:

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── fixtures/
│   └── seed_data.py        # Test data seeding functions
├── test_api_bills.py       # Tests for /api/bills endpoints
├── test_api_donations.py   # Tests for /api/donations endpoints
├── test_api_donors.py      # Tests for /api/donors endpoints
├── test_api_politicians.py # Tests for /api/politicians endpoints
└── test_api_votes.py       # Tests for /api/votes endpoints
```

### Key Test Fixtures

The test suite provides several pytest fixtures (defined in `conftest.py`):

- `client`: A Flask test client for making API requests
- `db_connection`: A database connection for direct database operations
- `seed_test_data`: Automatically seeds comprehensive test data before each test
- `clean_db`: Automatically cleans all tables between tests for isolation
- `setup_test_db`: Creates the test database schema once per test session

### Test Database Safety

The test suite includes multiple safety checks to prevent accidentally running tests against production data:

- Tests automatically use a separate database named `paper_trail_test`
- The `TESTING` environment variable is set to force test database usage
- Runtime checks verify the correct database is being used before tests run

### Troubleshooting Tests

If tests fail to run:

1. Ensure PostgreSQL is running and accessible
2. Verify your `.env` file has correct database credentials
3. Make sure your database user has permissions to create databases
4. Check that the `bin/bootstrap.sql` file exists and is valid
5. Try running tests with `-v` flag for more detailed output

### Pod Containers for deployment

**Note:** Update port mappings to 5001 if deploying with the development port configuration.

```bash
echo "paper-trail build image"
podman build -t paper-trail -f Dockerfile

echo "Create pod pod-paper-trail"
podman pod create -p 5000:5001 --name=pod-paper-trail \
&& \
podman pod start pod-paper-trail

# untar the pg_dump.tar.bz2 file before mounting it to the pg container.
podman run -d --pod=pod-paper-trail \
    --name=paper_trail_db \
    -v paper-trail-data:/var/lib/postgresql/data \
    -v ./bin/paper-trail-dump:/paper-trail-dump:ro \ 
    --secret DB_NAME,type=env,target=POSTGRES_DB \
    --secret DB_HOST,type=env,target=POSTGRES_SERVER \
    --secret DB_PORT,type=env,target=POSTGRES_PORT \
    --secret DB_USER,type=env,target=POSTGRES_USER \
    --secret DB_PASSWORD,type=env,target=POSTGRES_PASSWORD \
    docker.io/postgres:latest


# -p 5000:5000 only needed when local container used, otherwise pod exposes it above.
podman run --rm -d --pod=pod-paper-trail --name=paper-trail \
    --secret DB_NAME,type=env,target=DB_NAME \
    --secret DB_HOST,type=env,target=DB_HOST \
    --secret DB_PORT,type=env,target=DB_PORT \
    --secret DB_USER,type=env,target=DB_USER \
    --secret DB_PASSWORD,type=env,target=DB_PASSWORD \
    paper-trail

```

Restore db:

```
cd bin
tar -xvf pg-dump.tar.bz2 
```

This will give you the dump file paper-trail-dump which you can then copy to your postgres db. If using a container, you can copy it into the container then then restore `psql postres < paper-trail-dump` 
