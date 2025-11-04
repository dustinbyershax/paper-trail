This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Paper Trail is a Flask-based web application for tracking political campaign donations and correlating them with voting records. It combines FEC donation data, Congress.gov legislative data, and voting records to provide insights into the relationship between political donations and legislative actions.

## Architecture

### Database Schema
The application uses PostgreSQL with a custom schema (`pt`) containing five main tables:
- **Politicians**: Legislators and political figures (PoliticianID, FirstName, LastName, Party, State, Chamber, District, IsActive, Role)
- **Bills**: Legislation from Congress 108-119 (BillID, BillNumber, Title, DateIntroduced, Congress, Subjects)
- **Donors**: Campaign contributors with industry classification (DonorID, Name, DonorType, Employer, Industry, City, State)
- **Donations**: Individual contributions linking donors to politicians (DonationID, DonorID, PoliticianID, Amount, Date, ContributionType)
- **Votes**: Roll call votes linking politicians to bills (VoteID, PoliticianID, BillID, Vote)
- **fec_politician_map**: Maps FEC candidate IDs to internal PoliticianID

All database queries set `search_path TO pt, public` to use the custom schema.

### Application Structure
- **app/main.py**: Flask application with all API routes and database queries
- **app/config.py**: Configuration loader using python-dotenv for database credentials and API keys
- **app/templates/**: HTML frontend files (index.html for politician lookup, donor_search.html for donor queries)
- **bin/**: Data population scripts that load external data into PostgreSQL

### Key Features
- **Topic-to-Industry Mapping**: `TOPIC_INDUSTRY_MAP` in main.py maps bill subjects to donor industries for correlation analysis
- **Pagination**: Vote history API supports pagination (10 votes per page) with filtering by bill type and subject
- **Filtering**: Bills can be filtered by type (hr, s, hjres, sjres) and subjects array
- **Case Sensitivity**: Database uses lowercase table names in some queries (donations, votes) and mixed case in others (Politicians, Bills, Donors) - be careful when writing queries

## Development Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv env

# Activate (Linux/Mac)
source env/bin/activate

# Activate (Windows)
source env/Scripts/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .dev.env .env
# Edit .env with your PostgreSQL credentials and CONGRESS_GOV_API_KEY
```

### Running the Application
```bash
# Development mode
python -m app.main

# Production mode (via Docker)
podman build -t paper-trail -f Dockerfile
```

The app runs on port 5000 by default (configurable via PORT env var). Debug mode is controlled by FLASK_DEBUG env var.

### Database Setup
```bash
# Initialize schema
psql -U <user> -d <database> -f bin/bootstrap.sql

# Or extract and load pre-populated data
tar -xvf bin/sql_data.tar.bz2
python bin/load_sql.py
```

### Data Population Scripts (bin/)
These scripts fetch and load data from external sources:
- **populate_politicians.py**: Fetches Congress member data from Congress.gov API (Congresses 108-119)
- **populate_bills.py**: Downloads bill data from bulk.data.gov ZIP files
- **populate_votes.py**: Downloads roll call vote records
- **populate_donors_and_donations.py**: Processes FEC contribution data
- **populate_industries.py**: Maps donors to industry classifications
- **build_fec_map.py**: Creates politician-to-FEC candidate ID mappings

All populate scripts import `app.config` for database connection parameters and require `CONGRESS_GOV_API_KEY` in .env.

## API Routes

### Search Endpoints
- `GET /api/politicians/search?name=<query>` - Search politicians (min 2 chars)
- `GET /api/donors/search?name=<query>` - Search donors (min 3 chars)

### Politician Data
- `GET /api/politician/<politician_id>/votes?page=1&sort=desc&type[]=hr&subject[]=Health` - Paginated vote history with filters
- `GET /api/politician/<politician_id>/donations/summary` - Donation totals by industry
- `GET /api/politician/<politician_id>/donations/summary/filtered?topic=<topic>` - Industry-filtered donations by bill topic

### Donor Data
- `GET /api/donor/<donor_id>/donations` - All donations from a specific donor

### Reference Data
- `GET /api/bills/subjects` - List all unique bill subjects for filtering

## Deployment

### Container Deployment
The application is designed for Podman/Kubernetes pod deployment:
- **paper-trail container**: Flask app running on gunicorn (4 workers, 120s timeout)
- **paper_trail_db container**: PostgreSQL database
- Containers share a pod network on port 5000
- Database credentials passed via Podman secrets
- Persistent volume: `paper-trail-data` for PostgreSQL data

See README.md for complete pod creation commands.

## Important Notes

- Database connection uses psycopg2 with `psycopg2.extras.DictCursor` for dict-like row access
- Table name casing is inconsistent: use `Politicians`, `Bills`, `Donors` for some operations and lowercase `donations`, `votes` for others (check existing queries)
- Bills.subjects is a PostgreSQL array column - use `&&` operator for array containment queries and `UNNEST()` for flattening
- FEC data files are large (ignored in .gitignore) and stored in /contributions/, /votes/, /bills/ directories
- The app expects Python 3.13 syntax (Alpine-based Docker image)
- gunicorn serves the production app (not Flask's dev server)
