# Copy .env and setup files
cp $CONDUCTOR_ROOT_PATH/.env . && cp -r $CONDUCTOR_ROOT_PATH/.claude .

# Install dependencies
python3 -m venv .venv
# Activate the virtual environment
source .venv/bin/activate
uv pip install -r requirements.txt