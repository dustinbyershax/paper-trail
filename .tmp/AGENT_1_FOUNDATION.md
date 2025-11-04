# Agent 1: Foundation Architect

**Agent Type:** `typescript-pro` or `frontend-ts-expert`
**Duration:** 2-3 hours
**Branch:** `feature/refactor-plain-css+html+js-react-Phase1` (current)
**Status:** BLOCKING - Must complete before any parallel work can begin

## Overview

This phase creates the foundational infrastructure that all other agents depend on. Quality here is critical - all parallel work streams will build on these foundations.

---

## Tasks

### 1. Verify React 19 Dependencies

Create a test project to validate all dependency versions work together without conflicts.

**Steps:**
- [ ] Create test directory: `mkdir -p .tmp/react19-test && cd .tmp/react19-test`
- [ ] Initialize test project: `npm create vite@latest . -- --template react-ts`
- [ ] Install target dependencies:
  ```bash
  npm install react@19.2.0 react-dom@19.2.0
  npm install react-router-dom@^7.0.0
  npm install chart.js@^4.4.0 react-chartjs-2@^5.3.0
  npm install -D tailwindcss@4.0.0
  ```
- [ ] Verify no peer dependency conflicts
- [ ] Test Chart.js renders: Create simple component with Doughnut chart
- [ ] Test React Router works: Create basic routing
- [ ] Document any version adjustments needed
- [ ] Clean up test project: `cd ../.. && rm -rf .tmp/react19-test`

**Success Criteria:**
- ✅ All dependencies install without peer dependency errors
- ✅ Chart.js renders with react-chartjs-2
- ✅ React Router navigation works

---

### 2. Initialize Vite React Project

Create the production frontend project with all required dependencies.

**Steps:**
- [ ] Create frontend directory: `mkdir frontend && cd frontend`
- [ ] Initialize with Vite: `npm create vite@latest . -- --template react-ts`
- [ ] Update `package.json` with exact versions:
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
- [ ] Run `npm install`
- [ ] Verify all packages install without conflicts

---

### 3. Configure Build Tools

**A. TypeScript Configuration**

Update `frontend/tsconfig.json` for React 19 with strict mode:
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

**B. Tailwind CSS 4 Configuration**

Update `frontend/src/index.css` with CSS-first configuration:
```css
@import "tailwindcss";
```

**Note:** Tailwind 4 uses CSS-first configuration - no config files needed.

**C. Vite Configuration**

Update `frontend/vite.config.ts`:
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

**Verify:**
- [ ] Run `npm run dev` - should start without errors
- [ ] Run `npm run build` - should complete successfully
- [ ] TypeScript compilation should show 0 errors

---

### 4. Create ALL Type Definitions

Create `frontend/src/types/api.ts` with complete TypeScript interfaces for all API responses:

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

export interface VoteParams {
  page?: number;
  sort?: 'ASC' | 'DESC';
  type?: string;
  subject?: string;
}
```

**Success Criteria:**
- ✅ All API response types defined
- ✅ Types are exported
- ✅ Types match actual API responses (verified against API endpoints)

---

### 5. Create Complete API Service Layer

**A. Environment Configuration**

Create `frontend/src/config/env.ts`:
```typescript
// In development: use Vite proxy (relative URLs work via proxy)
// In production: use relative URLs (Flask serves from same origin)
export const API_BASE_URL = '';  // Empty string for relative URLs
```

**B. API Service Functions**

Create `frontend/src/services/api.ts` with all 7 typed functions:

```typescript
import { API_BASE_URL } from '../config/env';
import type {
  Politician,
  Donor,
  Donation,
  DonationSummary,
  VoteResponse,
  VoteParams
} from '../types/api';

async function fetchJSON<T>(url: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${url}`);
  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }
  return response.json();
}

export const api = {
  searchPoliticians: async (query: string): Promise<Politician[]> => {
    return fetchJSON<Politician[]>(`/api/politicians/search?q=${encodeURIComponent(query)}`);
  },

  searchDonors: async (query: string): Promise<Donor[]> => {
    return fetchJSON<Donor[]>(`/api/donors/search?q=${encodeURIComponent(query)}`);
  },

  getDonorDonations: async (donorId: number): Promise<Donation[]> => {
    return fetchJSON<Donation[]>(`/api/donor/${donorId}/donations`);
  },

  getPoliticianVotes: async (
    politicianId: string,
    params: VoteParams = {}
  ): Promise<VoteResponse> => {
    const searchParams = new URLSearchParams();
    if (params.page) searchParams.set('page', params.page.toString());
    if (params.sort) searchParams.set('sort', params.sort);
    if (params.type) searchParams.set('type', params.type);
    if (params.subject) searchParams.set('subject', params.subject);

    const queryString = searchParams.toString();
    const url = `/api/politician/${politicianId}/votes${queryString ? `?${queryString}` : ''}`;
    return fetchJSON<VoteResponse>(url);
  },

  getDonationSummary: async (politicianId: string): Promise<DonationSummary[]> => {
    return fetchJSON<DonationSummary[]>(`/api/politician/${politicianId}/donations/summary`);
  },

  getFilteredDonationSummary: async (
    politicianId: string,
    topic: string
  ): Promise<DonationSummary[]> => {
    return fetchJSON<DonationSummary[]>(
      `/api/politician/${politicianId}/donations/summary/filtered?topic=${encodeURIComponent(topic)}`
    );
  },

  getBillSubjects: async (): Promise<string[]> => {
    return fetchJSON<string[]>('/api/bills/subjects');
  },
};
```

**Success Criteria:**
- ✅ All 7 API functions implemented
- ✅ All functions have proper TypeScript return types
- ✅ Error handling in fetchJSON helper
- ✅ Query parameters properly encoded

---

### 6. Setup Basic Routing Structure

**A. Create Placeholder Pages**

Create empty placeholder components:

`frontend/src/pages/PoliticianSearch.tsx`:
```typescript
export default function PoliticianSearch() {
  return <div>Politician Search - Coming Soon</div>;
}
```

`frontend/src/pages/DonorSearch.tsx`:
```typescript
export default function DonorSearch() {
  return <div>Donor Search - Coming Soon</div>;
}
```

`frontend/src/pages/Feedback.tsx`:
```typescript
export default function Feedback() {
  return <div>Feedback - Coming Soon</div>;
}
```

**B. Setup React Router**

Update `frontend/src/App.tsx`:
```typescript
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import PoliticianSearch from './pages/PoliticianSearch';
import DonorSearch from './pages/DonorSearch';
import Feedback from './pages/Feedback';
import './index.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<PoliticianSearch />} />
        <Route path="/donor_search" element={<DonorSearch />} />
        <Route path="/feedback" element={<Feedback />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

**Verify:**
- [ ] Run `npm run dev`
- [ ] Navigate to `http://localhost:5173/` - should see "Politician Search - Coming Soon"
- [ ] Navigate to `http://localhost:5173/donor_search` - should see "Donor Search - Coming Soon"
- [ ] Navigate to `http://localhost:5173/feedback` - should see "Feedback - Coming Soon"
- [ ] Browser back/forward buttons should work

---

### 7. Create Development Documentation

**A. Frontend README**

Create `frontend/README.md`:
```markdown
# Paper Trail Frontend

React 19.2 + TypeScript 5.9.2 + Tailwind CSS 4 + Vite

## Development Setup

1. Ensure Node.js 24+ is installed
2. Install dependencies: `npm install`
3. Start development server: `npm run dev`

## Development Workflow

For local development, run TWO servers simultaneously:

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

## Project Structure

```
frontend/
├── src/
│   ├── types/
│   │   └── api.ts              # All TypeScript type definitions
│   ├── services/
│   │   └── api.ts              # API service layer (all 7 endpoints)
│   ├── config/
│   │   └── env.ts              # Environment configuration
│   ├── pages/
│   │   ├── PoliticianSearch.tsx
│   │   ├── DonorSearch.tsx
│   │   └── Feedback.tsx
│   ├── components/             # Reusable components
│   ├── hooks/                  # Custom React hooks
│   ├── App.tsx                 # Main app with routing
│   └── index.css               # Tailwind CSS imports
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

## Code Patterns

### Using API Services
```typescript
import { api } from '../services/api';
import type { Politician } from '../types/api';

// In your component
const [politicians, setPoliticians] = useState<Politician[]>([]);

const searchPoliticians = async (query: string) => {
  try {
    const results = await api.searchPoliticians(query);
    setPoliticians(results);
  } catch (error) {
    console.error('Search failed:', error);
  }
};
```

### TypeScript Strict Mode
- All components must have proper types
- No `any` types allowed
- Props interfaces required for all components

### Tailwind CSS
- Use Tailwind classes exclusively
- No inline styles or CSS modules
- Tailwind 4 uses CSS-first configuration

## Building for Production

```bash
npm run build
```

Build output goes to `dist/` which Flask will serve in production.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
```

**B. Update Root README**

Update `README.md` with frontend section:
```markdown
## Frontend Development

The frontend is a React 19.2 TypeScript application built with Vite.

### Setup
```bash
cd frontend
npm install
npm run dev  # Development server on http://localhost:5173
```

### Development Workflow
1. Start Flask backend: `flask run` (port 5000)
2. Start Vite dev server: `cd frontend && npm run dev` (port 5173)
3. Open http://localhost:5173 in browser

See `frontend/README.md` for detailed documentation.
```

**C. Update .gitignore**

Add frontend artifacts to `.gitignore`:
```
# Frontend
frontend/node_modules/
frontend/dist/
frontend/.vite/
frontend/.DS_Store
```

---

## ✅ VERIFICATION CHECKPOINT 1 (BLOCKING)

**This checkpoint MUST pass before releasing work to parallel agents.**

Run through ALL verification steps:

### Build Verification
- [ ] `npm run dev` starts without errors
- [ ] `npm run build` completes successfully
- [ ] TypeScript compilation: 0 errors
- [ ] No console errors in browser

### Type Definitions
- [ ] `frontend/src/types/api.ts` exists
- [ ] Contains all 10+ interfaces: Politician, Donor, Donation, DonationSummary, Vote, VoteResponse, VotePagination, VoteParams
- [ ] All types are exported

### API Service Layer
- [ ] `frontend/src/services/api.ts` exists
- [ ] Contains all 7 API functions:
  - searchPoliticians
  - searchDonors
  - getDonorDonations
  - getPoliticianVotes
  - getDonationSummary
  - getFilteredDonationSummary
  - getBillSubjects
- [ ] All functions have proper TypeScript return types
- [ ] Error handling implemented

### Routing
- [ ] Can navigate to `/` (Politician Search placeholder)
- [ ] Can navigate to `/donor_search` (Donor Search placeholder)
- [ ] Can navigate to `/feedback` (Feedback placeholder)
- [ ] Browser back/forward buttons work

### Tailwind CSS
- [ ] Tailwind compiles without errors
- [ ] No CSS-related warnings in console

### Documentation
- [ ] `frontend/README.md` exists with setup instructions
- [ ] Root `README.md` updated with frontend section
- [ ] `.gitignore` updated with frontend artifacts
- [ ] Project structure documented

### Browser Testing (REQUIRED)
**Use MCP Chrome DevTools to verify the application works in a real browser:**

1. **Start Backend and Frontend:**
   ```bash
   # Terminal 1: Start Flask backend
   source .venv/bin/activate
   python -m app.main  # Should run on port 5001

   # Terminal 2: Start Vite dev server
   cd frontend && pnpm run dev  # Should run on port 5173 or 5174
   ```

2. **Load Database (if needed):**
   ```bash
   cd bin && tar -xjf sql_data.tar.bz2
   cd sql && python ../../bin/load_sql.py
   ```

3. **Open Browser and Test:**
   - [ ] Navigate to http://localhost:5173 (or 5174)
   - [ ] Home page (/) loads without errors
   - [ ] Navigate to /donor_search - loads placeholder
   - [ ] Navigate to /feedback - loads placeholder
   - [ ] No console errors or warnings
   - [ ] Take screenshots of working pages

**Why Browser Testing is Required:**
- TypeScript compilation errors don't catch runtime issues
- React component errors only appear in the browser
- Proxy configuration issues only show during actual API calls
- Visual layout problems can't be detected by build tools

---

## Deliverables Package for Parallel Agents

Once CHECKPOINT 1 passes, provide the following to parallel agents:

1. **Working Vite Project**
   - All dependencies installed
   - Dev server runs without errors
   - TypeScript compiles successfully

2. **Complete Type System**
   - `frontend/src/types/api.ts` with all interfaces
   - Types documented and ready to use

3. **Complete API Layer**
   - `frontend/src/services/api.ts` with all 7 functions
   - Error handling implemented
   - Ready to import and use

4. **Routing Infrastructure**
   - Basic routing in place
   - Placeholder pages created
   - Agents only need to implement page content

5. **Documentation**
   - Clear setup instructions
   - Code patterns documented
   - Project structure explained

---

## Notes

- **Quality over speed** - Take time to get this right
- **No shortcuts** - All parallel work depends on this foundation
- **Test thoroughly** - Run all verification steps
- **Document clearly** - Other agents will use this as reference
- **Ask for help** - If stuck, stop and ask TYT Dev

---

## Timeline

**Estimated Duration:** 2-3 hours

**Do not proceed to parallel work until CHECKPOINT 1 fully passes.**
