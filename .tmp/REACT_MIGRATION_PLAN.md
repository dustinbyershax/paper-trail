# React Migration Plan - Paper Trail

**Migration Goal**: Convert Flask template-based frontend to React 19.2 TypeScript SPA with Tailwind CSS 4

**Status**: ✅ Phase 1 - COMPLETE | Phase 2 - Planning

---

## Technology Stack

- **React**: 19.2.0
- **TypeScript**: 5.9.2
- **Tailwind CSS**: 4.0.0 (latest 4.x with Oxide engine)
- **shadcn/ui**: Installed (33 components, "new-york" style)
- **Radix UI**: Complete primitive library (via shadcn/ui)
- **Vite**: 7.1.12
- **React Router**: 7.9.5
- **Chart.js & react-chartjs-2**: 4.5.1 & 5.3.1
- **Node.js**: 24+ (LTS, required for React 19.2 and TypeScript 5.9.2)
- **pnpm**: 10.19.0 (package manager)

---

## Current State Analysis

### Frontend
- 3 HTML templates with inline JavaScript:
  - `app/templates/index.html` - Politician search (836 lines)
  - `app/templates/donor_search.html` - Donor search (252 lines)
  - `feedback.html` route exists but template missing

### Backend
- Flask app serving templates and API endpoints
- 7 API endpoints under `/api/*`:
  - `/api/politicians/search`
  - `/api/donors/search`
  - `/api/donor/<id>/donations`
  - `/api/politician/<id>/votes`
  - `/api/politician/<id>/donations/summary`
  - `/api/politician/<id>/donations/summary/filtered`
  - `/api/bills/subjects`

### Deployment
- Podman pod with single Flask container
- Port 5000 exposed
- Dockerfile with Python 3.13-alpine base

---

## Phase 0: Pre-Migration Testing (Address GitHub Issue #12)

**Goal**: Establish comprehensive test baseline to ensure no breaking changes during React migration

**Status**: ✅ COMPLETE (on `update-test-base` branch)

**Completion Summary:**
- Created `paper_trail_test` database with full schema
- Added critical database safety mechanism to prevent production data corruption
- Rewrote all API endpoint tests (135 tests total, all passing)
- Added 24 SQL injection tests proving parameterization works
- Added comprehensive edge case coverage (Unicode, special chars, very long inputs)
- All tests passing in 5.69s
- Work completed on `update-test-base` branch, ready to merge

**Note:** Original Phase 0 tasks below have been superseded by comprehensive test rewrite completed in TEST_IMPROVEMENT_PLAN.md phases 1-3.

### Tasks

#### 0.0 Verify React 19 Dependencies
- [ ] Create test Node.js 24 project: `mkdir .tmp/react19-test && cd .tmp/react19-test`
- [ ] Initialize test project: `npm create vite@latest . -- --template react-ts`
- [ ] Install target dependencies:
  ```bash
  npm install react@19.2.0 react-dom@19.2.0
  npm install react-router-dom@^7.0.0
  npm install chart.js@^4.4.0 react-chartjs-2@^5.3.0
  npm install -D tailwindcss@4.0.0
  ```
- [ ] Verify no peer dependency conflicts
- [ ] Test that Chart.js + react-chartjs-2 render correctly with React 19.2
- [ ] Test that react-router-dom works with React 19.2
- [ ] Document any version adjustments needed
- [ ] Clean up test project: `rm -rf .tmp/react19-test`

**Success Criteria**:
- ✅ All dependencies install without peer dependency errors
- ✅ Chart.js renders with react-chartjs-2
- ✅ React Router navigation works

#### 0.1 Setup Testing Framework & Database Strategy
- [ ] Add testing dependencies to `requirements.txt`:
  - `pytest>=8.0.0`
  - `pytest-flask>=1.3.0`
  - `pytest-cov>=4.1.0` (code coverage)
  - `responses>=0.24.0` (HTTP mocking if needed)
- [ ] Create `tests/` directory structure
- [ ] Create `tests/__init__.py`
- [ ] Create `tests/conftest.py` with:
  - Flask test client setup
  - Database connection configuration (uses existing database in read-only mode)
  - Real database queries against actual data (no mocking)
  - Pytest fixtures for common test data lookups
- [ ] Document database test strategy:
  - Tests use the real production database in read-only mode
  - No test database needed - we're only testing API reads
  - Tests verify API responses match actual database content
  - No data modification tests (all endpoints are read-only)

**Files to Create**:
- `tests/__init__.py`
- `tests/conftest.py`

**Files to Modify**:
- `requirements.txt`

#### 0.2 Test Politicians API Endpoint
- [ ] Create `tests/test_politicians_api.py`
- [ ] Test `/api/politicians/search`:
  - [ ] Valid search query returns results
  - [ ] Short query (< 2 chars) returns empty array
  - [ ] Case-insensitive search works
  - [ ] Special characters handled correctly
  - [ ] SQL injection attempts fail safely
  - [ ] Empty query handling
  - [ ] Database error handling

**Test Cases for SQL Injection**:
```python
# Test payloads to verify parameterized queries work
test_payloads = [
    "'; DROP TABLE Politicians--",
    "' OR '1'='1",
    "' UNION SELECT * FROM--",
    "'; DELETE FROM Politicians--",
    "' OR 1=1--"
]
```

**Files to Create**:
- `tests/test_politicians_api.py`

#### 0.3 Test Donors API Endpoint
- [ ] Create `tests/test_donors_api.py`
- [ ] Test `/api/donors/search`:
  - [ ] Valid search query returns results
  - [ ] Query < 3 chars returns empty array
  - [ ] Case-insensitive search
  - [ ] Response format matches expected structure (lowercase keys)
  - [ ] SQL injection attempts fail safely
  - [ ] Database error handling

**Files to Create**:
- `tests/test_donors_api.py`

#### 0.4 Test Donations API Endpoints
- [ ] Create `tests/test_donations_api.py`
- [ ] Test `/api/donor/<id>/donations`:
  - [ ] Valid donor ID returns donation history
  - [ ] Invalid donor ID handling
  - [ ] Response format validation
  - [ ] Date formatting correctness
  - [ ] Amount formatting correctness
- [ ] Test `/api/politician/<id>/donations/summary`:
  - [ ] Valid politician ID returns summary
  - [ ] Industry grouping correctness
  - [ ] Total amount calculations
  - [ ] Null industry handling
- [ ] Test `/api/politician/<id>/donations/summary/filtered`:
  - [ ] Valid topic parameter works
  - [ ] Invalid topic returns empty array
  - [ ] Topic-to-industry mapping correctness
  - [ ] SQL injection attempts fail safely

**Files to Create**:
- `tests/test_donations_api.py`

#### 0.5 Test Votes API Endpoint
- [ ] Create `tests/test_votes_api.py`
- [ ] Test `/api/politician/<id>/votes`:
  - [ ] Pagination works correctly
  - [ ] Default page returns first page
  - [ ] Sort order (ASC/DESC) works
  - [ ] Bill type filtering works
  - [ ] Bill subject filtering works
  - [ ] Multiple filter combinations
  - [ ] Invalid sort order defaults to DESC
  - [ ] Edge cases: page 0, negative page, very high page
  - [ ] SQL injection attempts fail safely

**Files to Create**:
- `tests/test_votes_api.py`

#### 0.6 Test Bills API Endpoint
- [ ] Create `tests/test_bills_api.py`
- [ ] Test `/api/bills/subjects`:
  - [ ] Returns unique subjects array
  - [ ] Handles null/empty subjects correctly
  - [ ] Response is properly sorted
  - [ ] Database error handling

**Files to Create**:
- `tests/test_bills_api.py`

#### 0.7 Test Template Routes (Baseline Capture)
- [ ] Create `tests/test_template_routes.py`
- [ ] Test `/` route:
  - [ ] Returns valid HTML
  - [ ] Contains expected content (header, search form)
  - [ ] Status code 200
- [ ] Test `/donor_search.html` route:
  - [ ] Returns valid HTML
  - [ ] Contains expected content
  - [ ] Status code 200
- [ ] Test `/feedback.html` route:
  - [ ] Handles missing template gracefully
  - [ ] Current behavior documented

**Files to Create**:
- `tests/test_template_routes.py`

#### 0.8 Configuration & Documentation
- [ ] Create `pytest.ini` or update `pyproject.toml`:
  ```ini
  [pytest]
  testpaths = tests
  python_files = test_*.py
  python_classes = Test*
  python_functions = test_*
  addopts = -v --tb=short --cov=app --cov-report=term-missing
  ```
- [ ] Update `.gitignore` to exclude test coverage reports:
  - `.coverage`
  - `htmlcov/`
  - `.pytest_cache/`
- [ ] Document test database setup in README

**Files to Create**:
- `pytest.ini` or update `pyproject.toml`

**Files to Modify**:
- `.gitignore`

#### 0.9 Run Test Suite & Document
- [ ] Run full test suite: `pytest tests/ -v --cov=app`
- [ ] Generate coverage report
- [ ] Document baseline test results
- [ ] Create `tests/README.md` with test running instructions
- [ ] Verify all SQL injection tests pass (confirm parameterized queries work)

**Files to Create**:
- `tests/README.md`
- `tests/BASELINE_RESULTS.md` (document initial test results)

**Success Criteria**:
- ✅ All API endpoints have unit tests
- ✅ SQL injection tests pass (confirming parameterized queries)
- ✅ Test coverage > 80% for API endpoints
- ✅ All tests pass before migration begins

---

## Phase 1: React Project Setup

**Status**: ✅ COMPLETE (2025-11-04)

**Completed Work:**
- ✅ Vite React TypeScript project initialized
- ✅ All dependencies installed with exact versions verified
- ✅ Tailwind CSS 4 configured (CSS-first, no config file)
- ✅ shadcn/ui components installed (33 components)
- ✅ TypeScript configured with strict mode
- ✅ React Router 7 setup with placeholder pages
- ✅ Vite configured with API proxy
- ✅ Build system verified (production build: 387.88 kB)
- ✅ Development server working (port 5173)
- ✅ Documentation created (frontend/README.md)
- ✅ All using pnpm as package manager

**shadcn/ui Components Installed:**
alert-dialog, avatar, badge, breadcrumb, button, calendar, card, checkbox, command, dialog, dropdown-menu, hover-card, input, kbd, label, navigation-menu, pagination, popover, progress, radio-group, scroll-area, select, separator, sheet, sidebar, skeleton, slider, sonner, switch, table, tabs, toggle, toggle-group, tooltip

### Original Tasks (All Complete ✅)

#### 1.1 Initialize Vite React TypeScript Project
- [x] Create `frontend/` directory
- [x] Initialize with Vite TypeScript template
- [x] Verify React 19.2.0 and TypeScript 5.9.2 are installed
- [x] Configure Vite build output to `dist/` (default)
- [x] ✨ BONUS: Install shadcn/ui component library with 33 components

#### 1.2 Install Dependencies
- [x] Update `frontend/package.json` with exact versions (using pnpm):
  ```json
  {
    "dependencies": {
      "react": "19.2.0",
      "react-dom": "19.2.0",
      "react-router-dom": "^7.0.0",
      "chart.js": "^4.4.0",
      "react-chartjs-2": "^5.3.0"
    },
    "devDependencies": {
      "typescript": "5.9.2",
      "@types/react": "^19.0.0",
      "@types/react-dom": "^19.0.0",
      "tailwindcss": "4.0.0",
      "vite": "^5.4.0",
      "@vitejs/plugin-react": "^4.3.0"
    }
  }
  ```
- [ ] Run `npm install` to install dependencies
- [ ] Verify all packages install without conflicts

**Files to Modify**:
- `frontend/package.json`

#### 1.3 Configure Tailwind CSS 4
- [ ] Tailwind CSS 4 already included in package.json dependencies
- [ ] Update `frontend/src/index.css` with Tailwind directives:
  ```css
  @import "tailwindcss";
  ```
- [ ] Note: Tailwind 4 doesn't require config files - it uses CSS-first configuration
- [ ] Test Tailwind compilation works: `npm run dev`

**Files to Modify**:
- `frontend/src/index.css`

#### 1.4 Configure TypeScript
- [ ] Update `frontend/tsconfig.json` for React 19:
  ```json
  {
    "compilerOptions": {
      "target": "ES2020",
      "useDefineForClassFields": true,
      "lib": ["ES2020", "DOM", "DOM.Iterable"],
      "module": "ESNext",
      "skipLibCheck": true,
      "moduleResolution": "bundler",
      "allowImportingTsExtensions": true,
      "resolveJsonModule": true,
      "isolatedModules": true,
      "noEmit": true,
      "jsx": "react-jsx",
      "strict": true,
      "noUnusedLocals": true,
      "noUnusedParameters": true,
      "noFallthroughCasesInSwitch": true
    },
    "include": ["src"],
    "references": [{ "path": "./tsconfig.node.json" }]
  }
  ```
- [ ] Verify TypeScript compilation works: `npm run build`

**Files to Modify**:
- `frontend/tsconfig.json`

#### 1.5 Setup React Router
- [ ] Install react-router-dom (already in package.json)
- [ ] Create basic router structure in `App.tsx`
- [ ] Test router setup works

**Files to Modify**:
- `frontend/src/App.tsx`

#### 1.6 Configure Vite
- [ ] Update `frontend/vite.config.ts`:
  ```typescript
  import { defineConfig } from 'vite'
  import react from '@vitejs/plugin-react'

  export default defineConfig({
    plugins: [react()],
    build: {
      outDir: 'dist',
      sourcemap: true,
    },
    server: {
      port: 5173,
      proxy: {
        '/api': {
          target: 'http://localhost:5000',
          changeOrigin: true,
        },
      },
    },
  })
  ```
- [ ] Test dev server works: `npm run dev`

**Files to Modify**:
- `frontend/vite.config.ts`

#### 1.7 Update .gitignore
- [ ] Add frontend build artifacts:
  ```
  frontend/node_modules/
  frontend/dist/
  frontend/.vite/
  frontend/.DS_Store
  ```

**Files to Modify**:
- `.gitignore`

#### 1.8 Document Development Workflow
- [ ] Create `frontend/README.md` with development instructions:
  ```markdown
  # Frontend Development

  ## Development Setup

  1. Ensure Node.js 24+ is installed
  2. Install dependencies: `npm install`
  3. Start development server: `npm run dev`

  ## Development Workflow

  For local development, you need to run TWO servers simultaneously:

  1. **Backend (Flask)**: `flask run` or `python -m app.main`
     - Runs on: http://localhost:5000
     - Serves: API endpoints at `/api/*`

  2. **Frontend (Vite)**: `npm run dev` (from frontend/ directory)
     - Runs on: http://localhost:5173
     - Serves: React app with HMR
     - Proxies: API calls to localhost:5000

  ### Startup Order
  1. Start Flask backend first
  2. Then start Vite dev server
  3. Open browser to http://localhost:5173

  ## Building for Production

  ```bash
  npm run build
  ```

  Build output goes to `dist/` which Flask will serve in production.
  ```
- [ ] Update root `README.md` with development workflow section

**Files to Create**:
- `frontend/README.md`

**Files to Modify**:
- `README.md`

**Success Criteria**:
- ✅ React project initializes successfully
- ✅ All dependencies install without conflicts
- ✅ TypeScript compilation works
- ✅ Tailwind CSS 4 compiles correctly
- ✅ Dev server runs without errors

---

## Phase 2: TypeScript Type Definitions

**Status**: ⏳ Not Started

### Tasks

#### 2.1 Create API Response Types
- [ ] Create `frontend/src/types/api.ts`
- [ ] Define interfaces for all API responses:
  ```typescript
  export interface Politician {
    politicianid: string;
    firstname: string;
    lastname: string;
    party: string;
    state: string;
    role?: string;
    isactive: boolean;
  }

  export interface Donor {
    donorid: number;
    name: string;
    donortype: string;
    employer?: string;
    state?: string;
  }

  export interface Donation {
    amount: number;
    date: string;
    firstname: string;
    lastname: string;
    party: string;
    state: string;
  }

  export interface DonationSummary {
    industry: string;
    totalamount: number;
  }

  export interface Vote {
    voteid: number;
    vote: 'Yea' | 'Nay' | 'Present' | 'Not Voting';
    billnumber: string;
    title: string;
    dateintroduced: string;
    subjects: string[];
  }

  export interface VotePagination {
    currentPage: number;
    totalPages: number;
    totalVotes: number;
  }

  export interface VoteResponse {
    pagination: VotePagination;
    votes: Vote[];
  }
  ```

**Files to Create**:
- `frontend/src/types/api.ts`

**Success Criteria**:
- ✅ All API response shapes have TypeScript interfaces
- ✅ Types are exported and reusable
- ✅ Types match actual API responses

---

## Phase 3: Component Conversion

**Status**: ⏳ Not Started

### Tasks

#### 3.1 Create Shared Components
- [ ] Create `frontend/src/components/Header.tsx`:
  - [ ] Logo and title
  - [ ] Navigation links
  - [ ] Disclaimer banner
  - [ ] TypeScript props interface
- [ ] Create `frontend/src/components/LoadingSpinner.tsx`:
  - [ ] Reusable spinner component
  - [ ] Optional message prop
- [ ] Create `frontend/src/components/DonationChart.tsx`:
  - [ ] Chart.js integration with TypeScript
  - [ ] **REQUIRED**: Register Chart.js components before use:
    ```typescript
    import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
    ChartJS.register(ArcElement, Tooltip, Legend);
    ```
  - [ ] Doughnut chart component using react-chartjs-2
  - [ ] Legend rendering
  - [ ] TypeScript props for data

**Files to Create**:
- `frontend/src/components/Header.tsx`
- `frontend/src/components/LoadingSpinner.tsx`
- `frontend/src/components/DonationChart.tsx`

#### 3.2 Create API Service Layer & Environment Configuration
- [ ] Create `frontend/src/config/env.ts`:
  - [ ] API base URL configuration:
    ```typescript
    // In development: use Vite proxy (relative URLs work via proxy)
    // In production: use relative URLs (Flask serves from same origin)
    export const API_BASE_URL = '';  // Empty string for relative URLs
    ```
  - [ ] No environment variables needed (same-origin in both dev and prod)
- [ ] Create `frontend/src/services/api.ts`:
  - [ ] Centralized API functions using API_BASE_URL
  - [ ] Typed fetch functions for each endpoint
  - [ ] Error handling
  - [ ] TypeScript return types
  ```typescript
  import { API_BASE_URL } from '../config/env';

  export const api = {
    searchPoliticians: (query: string): Promise<Politician[]> => { ... },
    searchDonors: (query: string): Promise<Donor[]> => { ... },
    getDonorDonations: (donorId: number): Promise<Donation[]> => { ... },
    getPoliticianVotes: (politicianId: string, params: VoteParams): Promise<VoteResponse> => { ... },
    getDonationSummary: (politicianId: string): Promise<DonationSummary[]> => { ... },
    getFilteredDonationSummary: (politicianId: string, topic: string): Promise<DonationSummary[]> => { ... },
    getBillSubjects: (): Promise<string[]> => { ... },
  }
  ```

**Files to Create**:
- `frontend/src/config/env.ts`
- `frontend/src/services/api.ts`

#### 3.3 Convert PoliticianSearch Page
- [ ] Create `frontend/src/pages/PoliticianSearch.tsx`
- [ ] Convert search functionality:
  - [ ] Search input and button
  - [ ] Results display
  - [ ] Loading states
  - [ ] Error handling
- [ ] Convert detail view functionality:
  - [ ] Politician details display
  - [ ] Donation chart with filtering
  - [ ] Vote record with pagination
  - [ ] Vote filtering (bill type, subject, sort)
  - [ ] Subject tag interactions
- [ ] Use TypeScript throughout
- [ ] Convert all inline styles to Tailwind classes
- [ ] Preserve all existing functionality

**Files to Create**:
- `frontend/src/pages/PoliticianSearch.tsx`
- `frontend/src/components/PoliticianCard.tsx`
- `frontend/src/components/PoliticianDetails.tsx`
- `frontend/src/components/VoteRecord.tsx`
- `frontend/src/components/VoteFilters.tsx`

#### 3.4 Convert DonorSearch Page
- [ ] Create `frontend/src/pages/DonorSearch.tsx`
- [ ] Convert search functionality:
  - [ ] Search input and button
  - [ ] Results display
  - [ ] Loading states
- [ ] Convert detail view:
  - [ ] Donor details
  - [ ] Contribution history
  - [ ] Date and amount formatting
- [ ] Use TypeScript throughout
- [ ] Convert all inline styles to Tailwind classes
- [ ] Preserve all existing functionality

**Files to Create**:
- `frontend/src/pages/DonorSearch.tsx`
- `frontend/src/components/DonorCard.tsx`
- `frontend/src/components/DonorDetails.tsx`
- `frontend/src/components/ContributionHistory.tsx`

#### 3.5 Create Feedback Page
- [ ] Create `frontend/src/pages/Feedback.tsx`
- [ ] Basic placeholder page (since template is missing)
- [ ] Follow same design patterns as other pages

**Files to Create**:
- `frontend/src/pages/Feedback.tsx`

#### 3.6 Setup React Router
- [ ] Update `frontend/src/App.tsx`:
  - [ ] Setup React Router with routes:
    - `/` → PoliticianSearch
    - `/donor_search` → DonorSearch
    - `/feedback` → Feedback
  - [ ] Add Header component to all pages
  - [ ] Handle 404 routes

**Files to Modify**:
- `frontend/src/App.tsx`

#### 3.7 Create Custom Hooks
- [ ] Create `frontend/src/hooks/usePoliticianSearch.ts`:
  - [ ] Search logic
  - [ ] State management
  - [ ] TypeScript types
- [ ] Create `frontend/src/hooks/useDonorSearch.ts`
- [ ] Create `frontend/src/hooks/useVotes.ts`:
  - [ ] Pagination logic
  - [ ] Filtering logic
  - [ ] Sorting logic

**Files to Create**:
- `frontend/src/hooks/usePoliticianSearch.ts`
- `frontend/src/hooks/useDonorSearch.ts`
- `frontend/src/hooks/useVotes.ts`

**Success Criteria**:
- ✅ All templates converted to React components
- ✅ All functionality preserved
- ✅ TypeScript used throughout (no `any` types)
- ✅ Tailwind CSS 4 used instead of CDN
- ✅ Components are reusable and well-structured

---

## Phase 4: Flask Integration

**Status**: ⏳ Not Started

### Tasks

#### 4.1 Modify Flask Routes & Add CORS
- [ ] Add CORS support for development:
  - [ ] Add `flask-cors` to `requirements.txt`
  - [ ] Install: `pip install flask-cors`
- [ ] Update `app/main.py`:
  - [ ] Add CORS configuration for development:
    ```python
    from flask_cors import CORS
    import os

    # Enable CORS in development only
    if os.getenv('FLASK_ENV') == 'development':
        CORS(app)
    ```
  - [ ] Remove template routes:
    - Remove `@app.route('/')` template rendering
    - Remove `@app.route('/donor_search.html')` template rendering
    - Remove `@app.route('/feedback.html')` template rendering
  - [ ] Add static file serving:
    ```python
    from flask import send_from_directory, abort
    import os

    # Use absolute path for static folder
    static_folder = os.path.join(os.path.dirname(__file__), '../frontend/dist')
    app = Flask(__name__, static_folder=static_folder)

    # Serve React app for all non-API routes
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react(path):
        # Don't interfere with API routes (path won't have leading slash)
        if path.startswith('api'):
            abort(404)

        # Serve static files if they exist
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)

        # Default to index.html for client-side routing
        return send_from_directory(app.static_folder, 'index.html')
    ```
  - [ ] Verify all `/api/*` routes remain unchanged
  - [ ] Test API routes still work

**Files to Modify**:
- `requirements.txt`
- `app/main.py`

#### 4.2 Test Flask Integration
- [ ] Build React app: `cd frontend && npm run build`
- [ ] Test Flask serves React correctly:
  - [ ] `/` serves React app
  - [ ] `/donor_search` serves React app (client-side routing)
  - [ ] `/feedback` serves React app
  - [ ] `/api/*` routes still work
- [ ] Verify no 404 errors for client-side routes

**Success Criteria**:
- ✅ Flask serves React static files correctly
- ✅ All API routes remain functional
- ✅ Client-side routing works
- ✅ No breaking changes to API

---

## Phase 5: Build Process & Dockerfile

**Status**: ⏳ Not Started

### Tasks

#### 5.1 Update Dockerfile with Multi-Stage Build
- [ ] Modify `Dockerfile`:
  ```dockerfile
  # Stage 1: Build React app
  FROM node:24-alpine AS react-builder
  WORKDIR /app/frontend
  COPY frontend/package*.json ./
  RUN npm ci --only=production=false
  COPY frontend/ ./
  RUN npm run build

  # Stage 2: Python/Flask stage
  FROM python:3.13-alpine
  WORKDIR /app
  
  # Copy React build output
  COPY --from=react-builder /app/frontend/dist ./frontend/dist
  
  # Python setup (existing)
  ENV PYTHONDONTWRITEBYTECODE 1
  ENV PYTHONUNBUFFERED 1
  ENV FLASK_ENV=production

  COPY requirements.txt .
  RUN apk add --no-cache --virtual .build-deps \
      gcc \
      musl-dev \
      postgresql-dev \
      python3-dev \
      && pip install --no-cache-dir -r requirements.txt \
      && apk del .build-deps \
      && rm -rf /var/cache/apk/* /tmp/*

  COPY app/ ./app/

  RUN adduser -D -u 1000 flaskuser && \
      chown -R flaskuser:flaskuser /app

  USER flaskuser

  CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app", "--workers", "4", "--access-logfile", "-", "--error-logfile", "-", "--timeout", "120"]
  EXPOSE 5000
  ```
- [ ] Test Docker build: `podman build -t paper-trail -f Dockerfile`
- [ ] Verify React build artifacts are in final image
- [ ] Test container runs correctly

**Files to Modify**:
- `Dockerfile`

#### 5.2 Update .dockerignore
- [ ] Add frontend build artifacts that shouldn't be copied:
  ```
  frontend/node_modules/
  frontend/dist/
  frontend/.vite/
  ```
- [ ] Ensure only source files are copied, not build artifacts

**Files to Modify**:
- `.dockerignore` (create if doesn't exist)

**Success Criteria**:
- ✅ Docker build completes successfully
- ✅ React build artifacts are in final image
- ✅ Container runs and serves React app
- ✅ Multi-stage build reduces final image size

---

## Phase 6: Testing & Validation

**Status**: ⏳ Not Started

### Tasks

#### 6.1 Run Test Suite
- [ ] Execute all Phase 0 tests: `pytest tests/ -v`
- [ ] Verify all API tests still pass (no breaking changes)
- [ ] Verify SQL injection tests still pass
- [ ] Document any test failures

#### 6.2 Manual Testing
- [ ] Test all user flows:
  - [ ] Politician search → view details → view votes → filter votes
  - [ ] Politician search → view donations → filter by subject
  - [ ] Donor search → view donation history
  - [ ] Navigation between pages
  - [ ] Browser back/forward buttons work
- [ ] Test responsive design (mobile/tablet/desktop)
- [ ] Test in multiple browsers:
  - [ ] Chrome/Edge
  - [ ] Firefox
  - [ ] Safari
- [ ] Verify API calls work correctly
- [ ] Check browser console for errors

**Success Criteria**:
- ✅ All Phase 0 tests pass
- ✅ All user flows work correctly
- ✅ No console errors

---

## Phase 7: Cleanup

**Status**: ⏳ Not Started

### Tasks

#### 7.1 Remove Old Template Files
- [ ] Delete `app/templates/index.html`
- [ ] Delete `app/templates/donor_search.html`
- [ ] Keep templates directory if Flask requires it
- [ ] Update `.gitignore` if needed

**Files to Remove**:
- `app/templates/index.html`
- `app/templates/donor_search.html`

#### 7.2 Update Documentation
- [ ] Update `README.md`:
  - [ ] Add frontend setup instructions:
    ```bash
    # Frontend setup
    cd frontend
    npm install
    npm run dev  # Development server
    npm run build  # Production build
    ```
  - [ ] Update deployment instructions
  - [ ] Add testing instructions
  - [ ] Document new project structure
- [ ] Create `frontend/README.md` if needed
- [ ] Update any architecture documentation

**Files to Modify**:
- `README.md`

#### 7.3 Final Checks
- [ ] Run linter/formatter on all files
- [ ] Verify no console errors
- [ ] Check for unused dependencies
- [ ] Review all TypeScript types (no `any`)
- [ ] Verify production build works

**Success Criteria**:
- ✅ Old templates removed
- ✅ Documentation updated
- ✅ Code is clean and formatted
- ✅ No unused dependencies

---

## Deployment Checklist

Before deploying:

- [ ] All Phase 0 tests pass
- [ ] All components work correctly
- [ ] API endpoints unchanged and functional
- [ ] Docker build succeeds
- [ ] Container runs correctly
- [ ] Manual testing complete
- [ ] Documentation updated
- [ ] Code reviewed
- [ ] Production build tested locally

---

## Rollback Plan

Since still in development, rollback is straightforward:

1. **Git Rollback**: Revert commits to restore templates
2. **Restore Files**: Old templates available in git history
3. **Database**: No changes to database or API

---

## Future Enhancements (Post-Migration)

- [ ] Add nginx reverse proxy for better static file serving
- [ ] Implement code splitting for better performance
- [ ] Add React error boundaries
- [ ] Add React testing (Jest + React Testing Library)
- [ ] Add E2E testing (Playwright/Cypress)
- [ ] Optimize bundle size
- [ ] Add service worker for offline support
- [ ] Add analytics integration

---

## Notes

- All API routes remain at `/api/*` - no changes
- Flask static folder uses absolute path for reliability
- React Router handles all client-side routing
- TypeScript strict mode enabled
- Tailwind CSS 4 uses CSS-first configuration (no config files needed)
- Node.js 24+ (LTS) required for build (not runtime)
- CORS only enabled in development mode
- API calls use relative URLs in both dev and production

---

## Progress Tracking

**Last Updated**: 2025-11-03

**Current Phase**: Phase 1 - React Project Setup

**Completed Phases**:
- ✅ Phase 0 - Pre-Migration Testing (all 135 tests passing on `update-test-base` branch)

**Blockers**: None

**Next Steps**: Begin Phase 1.1 - Initialize Vite React TypeScript Project

