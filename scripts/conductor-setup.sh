# Copy .env and setup files
cp $CONDUCTOR_ROOT_PATH/.env . && cp $CONDUCTOR_ROOT_PATH/.claude/ .

# Install dependencies
python -m venv .venv
# Activate the virtual environment
source .venv/bin/activate
uv pip install -r requirements.txt