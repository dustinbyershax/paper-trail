# Agent 5: Backend & DevOps Integration Specialist

**Agent Type:** `backend-ts-expert` + Docker knowledge
**Duration:** 4-6 hours
**Dependencies:** Checkpoints 2, 3, 4 passed (All frontend work complete)
**Can Start:** After Agents 2, 3, and 4 complete their work

## Overview

Integrate the React frontend with Flask backend and create production Docker build. This involves modifying Flask to serve React static files, adding CORS for development, and creating a multi-stage Docker build.

**Critical:** Must ensure NO breaking changes to API endpoints - all 135 Phase 0 tests must still pass.

---

## Prerequisites

Before starting, verify:
- ✅ Agent 2 (Politician Search) complete
- ✅ Agent 3 (Donor Search) complete
- ✅ Agent 4 (Shared Components) complete
- ✅ Frontend builds successfully: `cd frontend && npm run build`
- ✅ Flask backend running and all tests passing

---

## Part A: Backend Integration

### Task 1: Add CORS Support

Flask needs CORS enabled in development so the Vite dev server (port 5173) can call the API (port 5000).

**Steps:**

1. **Add flask-cors to requirements.txt**

Open `requirements.txt` and add:
```
flask-cors>=4.0.0
```

2. **Install flask-cors**

```bash
pip install flask-cors
# OR if using uv:
uv pip install flask-cors
```

3. **Update app/main.py to enable CORS in development**

Add CORS configuration at the top of the file (after Flask app creation):

```python
from flask import Flask, send_from_directory, abort
from flask_cors import CORS
import os

# ... existing imports and app creation ...

# Enable CORS in development only
if os.getenv('FLASK_ENV') == 'development':
    CORS(app)
    print("CORS enabled for development")

# ... rest of the code ...
```

**Verify:**
- [ ] flask-cors added to requirements.txt
- [ ] flask-cors installs without errors
- [ ] CORS only enabled when FLASK_ENV=development
- [ ] CORS disabled in production (when FLASK_ENV not set or != 'development')

---

### Task 2: Modify Flask Routes

Remove template routes and add static file serving for React app.

**Steps:**

1. **Configure static folder**

At the top of `app/main.py` where Flask app is created, update static folder configuration:

```python
import os
from flask import Flask, send_from_directory, abort

# Use absolute path for static folder
static_folder = os.path.join(os.path.dirname(__file__), '../frontend/dist')
app = Flask(__name__, static_folder=static_folder)
```

2. **Remove old template routes**

Find and REMOVE these routes (or comment them out):
```python
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/donor_search.html')
def donor_search():
    return render_template('donor_search.html')

@app.route('/feedback.html')
def feedback():
    return render_template('feedback.html')
```

3. **Add catch-all route for React**

Add this NEW route at the END of all other routes (IMPORTANT: must be last):

```python
# Serve React app for all non-API routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    """
    Serve React app static files and handle client-side routing.

    - API routes are handled by specific @app.route decorators above
    - Static files (JS, CSS, images) are served if they exist
    - All other routes return index.html for client-side routing
    """
    # Don't interfere with API routes
    # (path won't have leading slash here)
    if path.startswith('api'):
        abort(404)

    # Serve static files if they exist
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)

    # Default to index.html for client-side routing
    return send_from_directory(app.static_folder, 'index.html')
```

4. **Verify all API routes remain unchanged**

Check that ALL these routes still exist and are ABOVE the catch-all route:
- `/api/politicians/search`
- `/api/donors/search`
- `/api/donor/<id>/donations`
- `/api/politician/<id>/votes`
- `/api/politician/<id>/donations/summary`
- `/api/politician/<id>/donations/summary/filtered`
- `/api/bills/subjects`

**IMPORTANT:** The catch-all route MUST be last, otherwise it will intercept API routes.

**Verify:**
- [ ] Static folder configured to `../frontend/dist`
- [ ] Old template routes removed
- [ ] Catch-all route added (LAST)
- [ ] All 7 API routes unchanged and ABOVE catch-all
- [ ] No syntax errors

---

### Task 3: Test Backend Integration

**Steps:**

1. **Build React app**

```bash
cd frontend
npm run build
```

This creates `frontend/dist/` with production build.

2. **Start Flask in development mode**

```bash
# Set FLASK_ENV for development (enables CORS)
export FLASK_ENV=development

# Start Flask
flask run
# OR
python -m app.main
```

3. **Test routes**

Open browser and test:
- [ ] `http://localhost:5000/` - Should serve React app (Politician Search)
- [ ] `http://localhost:5000/donor_search` - Should serve React app (Donor Search)
- [ ] `http://localhost:5000/feedback` - Should serve React app (Feedback)
- [ ] All pages load without 404 errors
- [ ] Navigation between pages works
- [ ] Browser refresh on any page works (client-side routing)

4. **Test API endpoints**

Use curl or browser to verify API still works:
```bash
# Test politician search
curl "http://localhost:5000/api/politicians/search?q=biden"

# Test donor search
curl "http://localhost:5000/api/donors/search?q=google"

# Test bill subjects
curl "http://localhost:5000/api/bills/subjects"
```

All should return JSON data.

5. **Test development workflow**

Test the full development workflow:

a. Keep Flask running
b. In another terminal, start Vite dev server:
```bash
cd frontend
npm run dev
```
c. Open `http://localhost:5173` (Vite dev server)
d. Verify API calls work through Vite proxy
e. Verify hot module reload works

---

## ✅ VERIFICATION CHECKPOINT 5A (Backend Integration)

**CRITICAL:** This checkpoint must pass before proceeding to Docker.

### Functional Tests
- [ ] React app builds successfully (`npm run build`)
- [ ] Flask serves React app at root URL
- [ ] Client-side routing works (all routes serve index.html)
- [ ] Browser refresh works on any route (no 404)
- [ ] All 7 API endpoints still functional
- [ ] API returns correct JSON data
- [ ] CORS enabled in development (Vite can call API)
- [ ] CORS disabled in production

### Test Suite
- [ ] Run full test suite: `pytest tests/ -v`
- [ ] All 135 tests MUST pass
- [ ] No new test failures
- [ ] No breaking changes to API

### Code Quality
- [ ] No Python syntax errors
- [ ] flask-cors in requirements.txt
- [ ] Catch-all route is LAST
- [ ] API routes ABOVE catch-all route
- [ ] Code follows existing style

### Browser Testing (REQUIRED)
**Use MCP Chrome DevTools to verify Flask serves React correctly:**

1. **Build React App:**
   ```bash
   cd frontend && pnpm run build
   # Should create frontend/dist directory
   ```

2. **Start Flask in Production Mode:**
   ```bash
   # Stop any running dev servers first
   source .venv/bin/activate
   FLASK_ENV=production python -m app.main
   # Should serve on port 5001, CORS should be disabled
   ```

3. **Test Integrated Application:**
   - [ ] Navigate to http://localhost:5001/ (Flask root)
   - [ ] Verify React app loads (not "Hello World" or Flask template)
   - [ ] Test all routes:
     - http://localhost:5001/ - Politician Search
     - http://localhost:5001/donor_search - Donor Search
     - http://localhost:5001/feedback - Feedback page
   - [ ] Refresh browser on each route (should NOT 404)
   - [ ] Test politician search functionality
   - [ ] Test donor search functionality
   - [ ] Verify all API calls work (check Network tab)
   - [ ] Check console for errors (should be none)
   - [ ] Verify CORS errors do NOT appear

4. **Test Development Mode (Optional but Recommended):**
   ```bash
   # Stop Flask
   # Terminal 1: Start Flask in dev mode
   FLASK_ENV=development python -m app.main

   # Terminal 2: Start Vite dev server
   cd frontend && pnpm run dev
   ```
   - [ ] Navigate to http://localhost:5173
   - [ ] Verify Vite dev server can call Flask API on port 5001
   - [ ] No CORS errors should appear
   - [ ] All functionality works

**Why This Testing is Critical:**
- Ensures Flask catch-all route works correctly
- Verifies static file serving from frontend/dist
- Confirms client-side routing doesn't break on refresh
- Tests CORS configuration for dev/prod modes
- Validates integration between React and Flask

**If ANY tests fail, STOP and fix before proceeding.**

---

## Part B: Docker Build

### Task 4: Update Dockerfile with Multi-Stage Build

Create a multi-stage Dockerfile that builds React in Node.js, then copies artifacts to Python container.

**Steps:**

1. **Read current Dockerfile**

Open `Dockerfile` and review current structure.

2. **Replace with multi-stage build**

```dockerfile
# Stage 1: Build React app
FROM node:24-alpine AS react-builder

WORKDIR /app/frontend

# Copy package files
COPY frontend/package*.json ./

# Install dependencies (including devDependencies for build)
RUN npm ci --only=production=false

# Copy frontend source
COPY frontend/ ./

# Build React app
RUN npm run build

# Stage 2: Python/Flask stage
FROM python:3.13-alpine

WORKDIR /app

# Copy React build output from Stage 1
COPY --from=react-builder /app/frontend/dist ./frontend/dist

# Python setup (keep existing configuration)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Copy requirements and install dependencies
COPY requirements.txt .

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    postgresql-dev \
    python3-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps \
    && rm -rf /var/cache/apk/* /tmp/*

# Copy application code
COPY app/ ./app/

# Create non-root user
RUN adduser -D -u 1000 flaskuser && \
    chown -R flaskuser:flaskuser /app

USER flaskuser

# Expose port
EXPOSE 5000

# Start gunicorn (keep existing configuration)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app", "--workers", "4", "--access-logfile", "-", "--error-logfile", "-", "--timeout", "120"]
```

**Key Changes:**
- Stage 1: Node.js 24 for React build
- Stage 2: Python 3.13 (existing)
- Copy React dist from Stage 1
- Keep all existing Python configuration
- FLASK_ENV=production (CORS disabled)

**Verify:**
- [ ] Dockerfile uses multi-stage build
- [ ] Stage 1 builds React correctly
- [ ] Stage 2 copies React artifacts
- [ ] Existing Python config preserved
- [ ] FLASK_ENV=production set
- [ ] No syntax errors

---

### Task 5: Update .dockerignore

Create or update `.dockerignore` to exclude unnecessary files from Docker build.

**If .dockerignore doesn't exist, create it:**

```
# Git
.git
.gitignore

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/
.pytest_cache/
.coverage
htmlcov/

# Frontend - node_modules (npm ci will reinstall)
frontend/node_modules/

# Frontend - build artifacts (npm run build will recreate)
frontend/dist/
frontend/.vite/

# Frontend - misc
frontend/.DS_Store

# Temp files
.tmp/

# Environment
.env
.env.*

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

**Verify:**
- [ ] `.dockerignore` exists
- [ ] Excludes `frontend/node_modules/`
- [ ] Excludes `frontend/dist/`
- [ ] Excludes `.tmp/`
- [ ] Includes Python and general exclusions

---

### Task 6: Test Docker Build

**Steps:**

1. **Build Docker image**

```bash
podman build -t paper-trail -f Dockerfile .
```

Watch for:
- Stage 1 (React build) completes successfully
- Stage 2 (Python) copies React artifacts
- No errors during build
- Reasonable build time

2. **Verify React artifacts in image**

```bash
podman run --rm paper-trail ls -la /app/frontend/dist/
```

Should show React build files:
- index.html
- assets/ directory
- vite.svg or other assets

3. **Run container**

```bash
# Stop any existing container
podman stop paper-trail 2>/dev/null || true
podman rm paper-trail 2>/dev/null || true

# Run new container
podman run -d \
  --name paper-trail \
  -p 5000:5000 \
  -e DB_HOST=your_db_host \
  -e DB_NAME=your_db_name \
  -e DB_USER=your_db_user \
  -e DB_PASSWORD=your_db_password \
  paper-trail

# View logs
podman logs -f paper-trail
```

4. **Test container**

Open browser and test:
- [ ] `http://localhost:5000/` - React app loads
- [ ] `http://localhost:5000/donor_search` - React app loads
- [ ] `http://localhost:5000/api/bills/subjects` - API returns JSON
- [ ] All navigation works
- [ ] No console errors

5. **Check container logs**

```bash
podman logs paper-trail
```

Look for:
- Gunicorn started successfully
- No errors
- No CORS warnings (CORS should be disabled in production)

6. **Stop container**

```bash
podman stop paper-trail
podman rm paper-trail
```

---

## ✅ VERIFICATION CHECKPOINT 5B (Docker Build)

### Build Tests
- [ ] Docker build completes successfully
- [ ] No build errors in either stage
- [ ] React build stage (Stage 1) succeeds
- [ ] Python stage (Stage 2) succeeds
- [ ] Build time is reasonable (< 10 minutes)

### Image Tests
- [ ] React artifacts present in `/app/frontend/dist/`
- [ ] Image size is reasonable (< 500MB)
- [ ] Multi-stage build reduces final image size

### Container Tests
- [ ] Container starts without errors
- [ ] React app loads at root URL
- [ ] All routes work (client-side routing)
- [ ] API endpoints functional
- [ ] No errors in container logs
- [ ] CORS disabled (production mode)

### Production Readiness
- [ ] FLASK_ENV=production set
- [ ] Gunicorn configured correctly
- [ ] Non-root user (flaskuser)
- [ ] Proper security settings

---

## Integration with Other Agents

### What You Receive
From Agents 2, 3, 4:
- Complete React application in `frontend/`
- Production build works: `npm run build`
- All pages functional

### What You Provide
To Final Integration:
- Modified Flask backend serving React
- CORS configuration
- Multi-stage Dockerfile
- Updated .dockerignore
- Working production container

---

## Files to Modify

```
.
├── Dockerfile                    # Multi-stage build
├── .dockerignore                # Build exclusions
├── requirements.txt             # Add flask-cors
└── app/
    └── main.py                  # CORS + static serving
```

---

## Rollback Plan

If integration fails:

1. **Restore app/main.py**
```bash
git checkout app/main.py
```

2. **Restore Dockerfile**
```bash
git checkout Dockerfile
```

3. **Remove flask-cors**
```bash
git checkout requirements.txt
pip uninstall flask-cors
```

4. **Backend works again with templates**

---

## Common Issues and Solutions

### Issue 1: API routes return 404
**Cause:** Catch-all route is before API routes
**Solution:** Move catch-all route to LAST position

### Issue 2: Client-side routing doesn't work
**Cause:** Catch-all route not returning index.html
**Solution:** Verify catch-all logic returns index.html for non-existent paths

### Issue 3: CORS errors in development
**Cause:** CORS not enabled or wrong configuration
**Solution:** Ensure `FLASK_ENV=development` set and CORS configured

### Issue 4: Docker build fails at React stage
**Cause:** Node.js version or npm issues
**Solution:** Verify Node.js 24-alpine in Dockerfile

### Issue 5: Tests fail after changes
**Cause:** Breaking change to API
**Solution:** Review changes, ensure API routes unchanged

---

## Tips

1. **Test incrementally** - Backend first, then Docker
2. **Keep API unchanged** - No breaking changes allowed
3. **Verify tests pass** - Run test suite after each change
4. **Check logs** - Container logs reveal issues
5. **Use .dockerignore** - Speeds up build, reduces size
6. **CORS only in dev** - Security requirement for production
7. **Catch-all route LAST** - Critical for routing to work

---

## Timeline

**Estimated Duration:** 4-6 hours

**Part A (Backend):** 2-3 hours
**Part B (Docker):** 2-3 hours

---

## Notes

- NO breaking changes to API allowed
- All 135 Phase 0 tests must still pass
- CORS only in development (security)
- Multi-stage build optimizes image size
- Catch-all route must be last
- Test both development and production modes
- Document any issues for future reference
