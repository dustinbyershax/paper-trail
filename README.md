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

### Pod Containers for deployment

**Note:** Update port mappings to 5001 if deploying with the development port configuration.

```bash
echo "paper-trail build image"
podman build -t paper-trail -f Dockerfile

echo "Create pod pod-paper-trail"
podman pod create -p 5000:5001 --name=pod-paper-trail \
&& \
podman pod start pod-paper-trail

podman run -d --pod=pod-paper-trail \
    --name=paper_trail_db \
    -v paper-trail-data:/var/lib/postgresql/data \
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
