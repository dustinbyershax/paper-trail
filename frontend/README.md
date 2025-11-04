# Paper Trail Frontend

React 19.2 + TypeScript 5.9.2 + Tailwind CSS 4 + Vite

## Development Setup

1. Ensure Node.js 24+ is installed
2. Install dependencies: `pnpm install`
3. Start development server: `pnpm run dev`

## Development Workflow

For local development, run TWO servers simultaneously:

1. **Backend (Flask)**: `flask run` or `python -m app.main`
   - Runs on: http://localhost:5000
   - Serves: API endpoints at `/api/*`

2. **Frontend (Vite)**: `pnpm run dev` (from frontend/ directory)
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
pnpm run build
```

Build output goes to `dist/` which Flask will serve in production.

## Available Scripts

- `pnpm run dev` - Start development server
- `pnpm run build` - Build for production
- `pnpm run preview` - Preview production build locally
- `pnpm run lint` - Run ESLint

## API Endpoints (7 total)

All endpoints are available through the typed `api` service object:

1. `api.searchPoliticians(query)` - Search politicians by name
2. `api.searchDonors(query)` - Search donors by name
3. `api.getDonorDonations(donorId)` - Get donations by donor
4. `api.getPoliticianVotes(politicianId, params)` - Get politician voting record
5. `api.getDonationSummary(politicianId)` - Get donation summary by industry
6. `api.getFilteredDonationSummary(politicianId, topic)` - Get filtered donation summary
7. `api.getBillSubjects()` - Get all bill subjects

See `src/services/api.ts` for detailed documentation of each endpoint.
