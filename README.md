<!-- <div align="center"> -->
<table align="center">
  <tr>
    <td valign="middle"><img src="frontend/public/favicon.svg" alt="Paper Trail Logo" width="80"></td>
    <td valign="middle"><h1>Project: Paper Trail</h1></td>
  </tr>
</table>

<p align="center">
  <strong>Track the money behind political votes</strong>
  <br />
  A comprehensive platform for exploring relationships between campaign donations and congressional voting records.
  <br />
  🏛️ Politicians • 💰 Donations • 🗳️ Votes • 📊 Analysis
</p>

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## About

Paper Trail connects the dots between political contributions and legislative actions. Search for politicians or donors, explore voting records, and discover donation patterns to understand the financial influences on congressional decision-making.

## Features

- ✨ **Politician Search** - Find members of Congress by name and view their profiles
- 🗳️ **Vote History** - Browse voting records with filtering by bill type and subject
- 💵 **Donation Tracking** - See who's funding campaigns and how much
- 🏢 **Industry Analysis** - Analyze donation patterns by industry sector
- 📊 **Topic Filtering** - Connect donations to specific policy areas (Health, Finance, Technology, etc.)
- 🔍 **Donor Profiles** - Explore individual and organizational donors

## Tech Stack

**Frontend:**
- React 19.2 with TypeScript
- Vite for fast builds and HMR
- TanStack Query for data fetching
- React Router for navigation
- Tailwind CSS 4 for styling
- shadcn/ui components

**Backend:**
- Flask (Python 3.13)
- PostgreSQL 16
- psycopg2 for database connectivity

**DevOps:**
- Docker & Docker Compose
- Multi-stage production builds
- Hot reload for development

---

## Quick Start

### 🐳 Docker Compose (Recommended)

The easiest way to get started is using Docker Compose, which handles all dependencies automatically.

**Prerequisites:**
- Docker and Docker Compose installed
- (Optional) Congress.gov API key

**Setup:**
```bash
# Clone the repository
git clone <repository-url>
cd paper-trail

# Copy environment template
cp .env.docker .env

# (Optional) Add your Congress.gov API key to .env
# CONGRESS_GOV_API_KEY=your_key_here

# Start all services (database, backend, frontend)
docker compose up
```

That's it! The application will be available at:
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:5001
- **Database:** localhost:5432

Press `Ctrl+C` to stop all services.

**Useful Commands:**
```bash
# Start in detached mode (background)
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down

# Rebuild after code changes
docker compose up --build

# Stop and remove volumes (reset database)
docker compose down -v
```

**Hot Reload:**
Both backend and frontend support hot reload in Docker Compose:
- ⚡ Backend: Flask auto-reloads on Python file changes
- ⚡ Frontend: Vite auto-reloads on TypeScript/React file changes

---

## Development

### 💻 Local Development (Without Docker)

If you prefer to run services locally without Docker:

**Prerequisites:**
- Python 3.13+
- Node.js 24+ (LTS)
- PostgreSQL 16+
- pnpm

**Backend Setup:**
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install Python dependencies
pip install -r requirements.txt

# Copy environment template
cp .dev.env .env
# Update .env with your PostgreSQL credentials
```

**Frontend Setup:**
```bash
cd frontend
pnpm install
```

**Running Locally:**
```bash
# Terminal 1: Start backend
python -m app.main  # Runs on port 5001

# Terminal 2: Start frontend
cd frontend
pnpm run dev        # Runs on port 5173
```

Open http://localhost:5173 in your browser.

**Note:** Flask runs on port 5001 to avoid conflicts with macOS AirPlay Receiver.

See [`frontend/README.md`](frontend/README.md) for detailed frontend documentation.

### 📁 Project Structure

```
paper-trail/
├── app/                    # Flask backend
│   ├── config.py          # Configuration management
│   ├── main.py            # API routes and app initialization
│   └── static/            # Built React app (production)
├── frontend/              # React frontend
│   ├── src/               # TypeScript source code
│   ├── public/            # Static assets
│   └── vite.config.ts     # Vite configuration
├── bin/                   # Database scripts and dumps
├── tests/                 # Backend test suite
├── docker-compose.yml     # Development orchestration
├── Dockerfile            # Production multi-stage build
└── Dockerfile.dev        # Development backend image
```

---

## Testing

### 🧪 Running Tests

The project uses [pytest](https://docs.pytest.org/) with comprehensive unit tests for all API endpoints.

**Prerequisites:**

Before running tests, you need:

1. A PostgreSQL database server running (same as for development)
2. A separate test database that will be automatically created
3. Your `.env` file configured with database credentials

The test suite will automatically:
- Create a test database named `paper_trail_test`
- Restore the database schema from `bin/pg-dump.tar.bz2` (schema only, no data)
- Seed test data before each test
- Clean up data between tests to ensure isolation

**Running the Tests:**

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

**Test Structure:**

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

**Key Test Fixtures:**

- `client`: A Flask test client for making API requests
- `db_connection`: A database connection for direct database operations
- `seed_test_data`: Automatically seeds comprehensive test data before each test
- `clean_db`: Automatically cleans all tables between tests for isolation
- `setup_test_db`: Creates the test database schema once per test session

**Test Database Safety:**

The test suite includes multiple safety checks to prevent accidentally running tests against production data:
- ✅ Tests automatically use a separate database named `paper_trail_test`
- ✅ The `TESTING` environment variable is set to force test database usage
- ✅ Runtime checks verify the correct database is being used before tests run

**Troubleshooting:**

If tests fail to run:
1. Ensure PostgreSQL is running and accessible
2. Verify your `.env` file has correct database credentials
3. Make sure your database user has permissions to create databases
4. Check that the `bin/bootstrap.sql` file exists and is valid
5. Try running tests with `-v` flag for more detailed output

---

## Deployment

### 🚀 Docker Production Build

The project includes a multi-stage Dockerfile that builds both frontend and backend into a single production image:

```bash
# Build production image
docker build -t paper-trail:latest .

# Run production container
docker run -d \
  -p 5000:5000 \
  -e DB_HOST=your-db-host \
  -e DB_NAME=your-db-name \
  -e DB_USER=your-db-user \
  -e DB_PASSWORD=your-db-password \
  -e CONGRESS_GOV_API_KEY=your-api-key \
  paper-trail:latest
```

The production build:
- Stage 1: Builds React frontend with Node 24 + pnpm
- Stage 2: Combines frontend build with Flask backend
- Serves frontend from Flask's static folder
- Uses gunicorn with 4 workers for production

### 🔧 Podman Deployment

For Podman-based deployments:

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

**Database Restoration:**

```bash
# Extract database dump
cd bin
tar -xvf pg-dump.tar.bz2

# Restore to PostgreSQL
psql postgres < paper-trail-dump
```

For containerized databases, copy the dump into the container first:
```bash
# Copy dump to container
podman cp paper-trail-dump paper_trail_db:/tmp/

# Restore inside container
podman exec -it paper_trail_db psql -U paper_trail_user postgres < /tmp/paper-trail-dump
```

---

## Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Run tests** to ensure everything works (`pytest`)
5. **Commit your changes** (`git commit -m 'Add amazing feature'`)
6. **Push to your branch** (`git push origin feature/amazing-feature`)
7. **Open a Pull Request**

### Development Guidelines

- Follow existing code style and formatting
- Write tests for new features
- Update documentation as needed
- Keep commits focused and descriptive
- Ensure all tests pass before submitting PR

### Reporting Issues

Found a bug or have a feature request? [Open an issue](https://github.com/Operation-Hope/paper-trail/issues) with:
- Clear description of the problem/feature
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Screenshots if applicable

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

## Acknowledgments

- Campaign finance data from the Federal Election Commission (FEC)
- Congressional voting data from Congress.gov
- Industry categorization based on OpenSecrets methodology

---

**Questions or feedback?** [Open an issue](https://github.com/Operation-Hope/paper-trail/issues) or reach out to the maintainers. 
