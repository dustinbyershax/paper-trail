# Agent 4: Shared Components & Visualization Specialist

**Agent Type:** `frontend-ts-expert` with Chart.js experience
**Duration:** 2-3 hours (REDUCED from 4-6 - role significantly changed)
**Dependencies:** CHECKPOINT 1 passed (Agent 1 complete) ✅
**Can Start:** ✅ READY NOW (can run PARALLEL with Agents 2 & 3)

## 🚨 MAJOR ROLE CHANGE: Focus on Composition, Not Creation

**Phase 1 delivered shadcn/ui - Your role has fundamentally changed!**

### ❌ DO NOT Create These (Already Exist in shadcn/ui):
- ~~Header component from scratch~~
- ~~Button component~~
- ~~Input component~~
- ~~Card component~~
- ~~LoadingSpinner component~~
- ~~Any basic UI primitives~~

### ✅ DO Create These (Your New Focus):

1. **Header** - COMPOSE using shadcn components (NavigationMenu, etc.)
2. **DonationChart** - Chart.js integration (unique, not provided by shadcn)
3. **Page Layouts** - Layout wrappers and containers
4. **Theme Toggle** - Use existing theme-provider.tsx
5. **Business Logic Hooks** - useDebounce, useLocalStorage, etc.

## Overview

Create COMPOSITION components and business logic that leverage the installed shadcn/ui component library. Your work focuses on unique functionality that shadcn doesn't provide.

**Critical:** The DonationChart component MUST properly register Chart.js components for React 19 compatibility.

---

## Prerequisites

Before starting, verify you have:
- ✅ Working Vite dev server (`npm run dev`)
- ✅ `frontend/src/types/api.ts` with all type definitions
- ✅ `frontend/src/services/api.ts` with all API functions
- ✅ Chart.js and react-chartjs-2 installed
- ✅ Flask backend running on port 5000

---

## Tasks

### 1. Create Header Component

Create `frontend/src/components/Header.tsx`:

Site-wide navigation header used on all pages.

**Requirements:**

1. **Logo and Title**
   - App name/title: "Paper Trail"
   - Optional logo/icon
   - Prominent positioning

2. **Navigation Links**
   - Link to "/" (Politician Search)
   - Link to "/donor_search" (Donor Search)
   - Link to "/feedback" (Feedback)
   - Active link highlighting
   - Use React Router's `Link` or `NavLink`

3. **Disclaimer Banner**
   - Display disclaimer text from original template
   - Subtle styling (different background color)
   - Full width below main header

4. **Responsive Design**
   - Mobile: Hamburger menu or stacked links
   - Desktop: Horizontal navigation
   - Tailwind CSS for all styling

**Example Implementation:**
```typescript
import { NavLink } from 'react-router-dom';

export default function Header() {
  return (
    <header className="bg-blue-600 text-white">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold">Paper Trail</h1>
          <nav className="flex gap-4">
            <NavLink
              to="/"
              className={({ isActive }) =>
                isActive ? 'font-bold underline' : 'hover:underline'
              }
            >
              Politician Search
            </NavLink>
            <NavLink
              to="/donor_search"
              className={({ isActive }) =>
                isActive ? 'font-bold underline' : 'hover:underline'
              }
            >
              Donor Search
            </NavLink>
            <NavLink
              to="/feedback"
              className={({ isActive }) =>
                isActive ? 'font-bold underline' : 'hover:underline'
              }
            >
              Feedback
            </NavLink>
          </nav>
        </div>
      </div>
      <div className="bg-blue-500 px-4 py-2">
        <p className="text-sm text-center">
          Disclaimer: This data is for informational purposes only.
          Data accuracy is not guaranteed. Please verify all information
          with official sources.
        </p>
      </div>
    </header>
  );
}
```

**Verify:**
- [ ] Component renders without errors
- [ ] Navigation links work
- [ ] Active link highlighted
- [ ] Disclaimer displayed
- [ ] Responsive on mobile and desktop
- [ ] TypeScript compiles without errors

---

### 2. Create Loading Spinner Component

Create `frontend/src/components/LoadingSpinner.tsx`:

Reusable loading indicator used throughout the app.

**Props:**
```typescript
interface LoadingSpinnerProps {
  message?: string;
  size?: 'sm' | 'md' | 'lg';
}
```

**Requirements:**
- Display animated spinner (CSS animation)
- Optional message below spinner
- Configurable size (small, medium, large)
- Center aligned by default
- Use Tailwind CSS

**Example Implementation:**
```typescript
interface LoadingSpinnerProps {
  message?: string;
  size?: 'sm' | 'md' | 'lg';
}

export default function LoadingSpinner({
  message,
  size = 'md',
}: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'w-6 h-6',
    md: 'w-12 h-12',
    lg: 'w-16 h-16',
  };

  return (
    <div className="flex flex-col items-center justify-center p-8">
      <div
        className={`${sizeClasses[size]} border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin`}
      ></div>
      {message && (
        <p className="mt-4 text-gray-600">{message}</p>
      )}
    </div>
  );
}
```

**Verify:**
- [ ] Spinner animates smoothly
- [ ] Optional message displays
- [ ] Size variants work
- [ ] TypeScript compiles without errors

---

### 3. Create Donation Chart Component (CRITICAL)

Create `frontend/src/components/DonationChart.tsx`:

Chart component displaying donation breakdown by industry using Chart.js.

**CRITICAL REQUIREMENT:** Must properly register Chart.js components for React 19.

**Props:**
```typescript
interface DonationChartProps {
  politicianId: string;
  selectedTopic?: string; // For filtering by topic
  onTopicChange?: (topic: string) => void;
}
```

**Requirements:**

1. **Chart.js Registration (CRITICAL)**
   ```typescript
   import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

   // MUST register components before using
   ChartJS.register(ArcElement, Tooltip, Legend);
   ```

2. **Data Loading**
   - Fetch donation summary using `api.getDonationSummary(politicianId)`
   - If `selectedTopic` provided, use `api.getFilteredDonationSummary(politicianId, selectedTopic)`
   - Handle loading state
   - Handle errors

3. **Chart Display**
   - Use `react-chartjs-2` Doughnut component
   - Display donations by industry
   - Color-coded segments
   - Show percentages
   - Responsive sizing

4. **Topic Filtering (Optional but Recommended)**
   - Dropdown to select topic
   - Topics: Health, Finance, Technology, Defense, Energy, Environment, Education, Agriculture, Transportation
   - When topic selected, reload data with filter
   - Callback to parent via `onTopicChange`

5. **Legend**
   - Industry names
   - Total amounts
   - Color indicators
   - Clickable to filter (Chart.js default behavior)

**Example Implementation:**
```typescript
import { useState, useEffect } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';
import { api } from '../services/api';
import type { DonationSummary } from '../types/api';

// CRITICAL: Register Chart.js components
ChartJS.register(ArcElement, Tooltip, Legend);

interface DonationChartProps {
  politicianId: string;
  selectedTopic?: string;
  onTopicChange?: (topic: string) => void;
}

const COLORS = [
  '#FF6384',
  '#36A2EB',
  '#FFCE56',
  '#4BC0C0',
  '#9966FF',
  '#FF9F40',
  '#FF6384',
  '#C9CBCF',
  '#4BC0C0',
  '#FF6384',
];

const TOPICS = [
  'Health',
  'Finance',
  'Technology',
  'Defense',
  'Energy',
  'Environment',
  'Education',
  'Agriculture',
  'Transportation',
];

export default function DonationChart({
  politicianId,
  selectedTopic,
  onTopicChange,
}: DonationChartProps) {
  const [donations, setDonations] = useState<DonationSummary[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDonations();
  }, [politicianId, selectedTopic]);

  const loadDonations = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = selectedTopic
        ? await api.getFilteredDonationSummary(politicianId, selectedTopic)
        : await api.getDonationSummary(politicianId);
      setDonations(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load donations');
      setDonations([]);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <div>Loading chart...</div>;
  }

  if (error) {
    return <div className="text-red-600">Error: {error}</div>;
  }

  if (donations.length === 0) {
    return <div>No donation data available</div>;
  }

  const chartData = {
    labels: donations.map((d) => d.industry || 'Unknown'),
    datasets: [
      {
        data: donations.map((d) => d.totalamount),
        backgroundColor: COLORS,
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'bottom' as const,
      },
      tooltip: {
        callbacks: {
          label: (context: any) => {
            const label = context.label || '';
            const value = context.parsed || 0;
            const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0);
            const percentage = ((value / total) * 100).toFixed(1);
            return `${label}: $${value.toLocaleString()} (${percentage}%)`;
          },
        },
      },
    },
  };

  return (
    <div className="my-4">
      <h3 className="text-xl font-bold mb-4">Donations by Industry</h3>

      {onTopicChange && (
        <div className="mb-4">
          <label htmlFor="topic-filter" className="block mb-2">
            Filter by Topic:
          </label>
          <select
            id="topic-filter"
            value={selectedTopic || ''}
            onChange={(e) => onTopicChange(e.target.value)}
            className="border rounded px-3 py-2"
          >
            <option value="">All Industries</option>
            {TOPICS.map((topic) => (
              <option key={topic} value={topic}>
                {topic}
              </option>
            ))}
          </select>
        </div>
      )}

      <div className="max-w-md mx-auto">
        <Doughnut data={chartData} options={chartOptions} />
      </div>

      <div className="mt-4">
        <h4 className="font-bold mb-2">Total by Industry:</h4>
        <ul className="space-y-1">
          {donations.map((d, index) => (
            <li key={index} className="flex justify-between">
              <span>{d.industry || 'Unknown'}:</span>
              <span className="font-medium">
                ${d.totalamount.toLocaleString()}
              </span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
```

**Verify:**
- [ ] Chart.js components registered (no console errors)
- [ ] Chart renders correctly
- [ ] Data loads from API
- [ ] Topic filter works (if implemented)
- [ ] Legend displays correctly
- [ ] Tooltips show percentages
- [ ] Colors display correctly
- [ ] Responsive on different screen sizes
- [ ] TypeScript compiles without errors
- [ ] No Chart.js warnings in console

**Testing:**
- Test with real politician ID
- Test with different topics
- Test with politician who has no donations
- Test with politician who has many donations
- Verify percentages add up to 100%

---

### 4. Create Feedback Page

Create `frontend/src/pages/Feedback.tsx`:

Basic placeholder page for feedback (original template doesn't exist).

**Requirements:**
- Import and use Header component
- Simple message or form placeholder
- Match design patterns from other pages
- Use Tailwind CSS

**Example Implementation:**
```typescript
import Header from '../components/Header';

export default function Feedback() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-4">Feedback</h1>
        <p className="text-gray-600 mb-4">
          We value your feedback! This page is under development.
        </p>
        <p className="text-gray-600">
          For now, please contact us directly with any questions or suggestions.
        </p>
      </main>
    </div>
  );
}
```

**Verify:**
- [ ] Page renders without errors
- [ ] Header displays correctly
- [ ] Content is readable and styled
- [ ] Matches design of other pages
- [ ] TypeScript compiles without errors

---

### 5. Update App.tsx

Update `frontend/src/App.tsx` to include Header on all pages:

**Option A:** Wrap routes with Header
```typescript
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import PoliticianSearch from './pages/PoliticianSearch';
import DonorSearch from './pages/DonorSearch';
import Feedback from './pages/Feedback';
import './index.css';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<PoliticianSearch />} />
            <Route path="/donor_search" element={<DonorSearch />} />
            <Route path="/feedback" element={<Feedback />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
```

**Option B:** Let each page import Header (more flexible)
- Each page handles its own layout
- Header imported individually
- More control for special layouts

Choose Option A for consistency.

**Verify:**
- [ ] Header shows on all pages
- [ ] Navigation works between pages
- [ ] Layout is consistent
- [ ] No console errors

---

## ✅ VERIFICATION CHECKPOINT 4

Run through ALL verification steps before marking complete:

### Component Tests
- [ ] **Header:**
  - [ ] Renders on all pages
  - [ ] Navigation links work
  - [ ] Active link highlighted correctly
  - [ ] Disclaimer displays
  - [ ] Responsive on mobile and desktop

- [ ] **LoadingSpinner:**
  - [ ] Spinner animates smoothly
  - [ ] Optional message displays
  - [ ] Size variants work (sm, md, lg)
  - [ ] Centers correctly

- [ ] **DonationChart:**
  - [ ] Chart.js components registered (CRITICAL - no console errors)
  - [ ] Chart renders with real data
  - [ ] Data loads from API correctly
  - [ ] Topic filter works (if implemented)
  - [ ] Legend displays with correct colors
  - [ ] Tooltips show amounts and percentages
  - [ ] Responsive sizing works
  - [ ] Handles empty data gracefully
  - [ ] Error state displays correctly
  - [ ] Loading state displays correctly

- [ ] **Feedback Page:**
  - [ ] Page renders
  - [ ] Header displays
  - [ ] Content styled consistently
  - [ ] Navigation works

### Code Quality
- [ ] No TypeScript errors (`npm run build` succeeds)
- [ ] No `any` types used
- [ ] All props have TypeScript interfaces
- [ ] Components follow React best practices
- [ ] Chart.js properly registered

### Browser Tests
- [ ] No console errors
- [ ] No console warnings (especially Chart.js warnings)
- [ ] Navigation between pages works smoothly
- [ ] Chart animation is smooth
- [ ] Page performance is acceptable

### Integration Ready
- [ ] Components exported correctly
- [ ] Can be imported by other components
- [ ] TypeScript types exported where needed
- [ ] Documentation clear for other agents

### Browser Testing (REQUIRED)
**Use MCP Chrome DevTools to verify all shared components work correctly:**

1. **Ensure Backend and Frontend are Running:**
   ```bash
   # Backend should be on port 5001
   # Frontend should be on port 5173 or 5174
   ```

2. **Test Header Component:**
   - [ ] Navigate to http://localhost:5173/
   - [ ] Verify header appears at top of page
   - [ ] Click "Politician Search" link - should navigate to /
   - [ ] Click "Donor Search" link - should navigate to /donor_search
   - [ ] Click "Feedback" link - should navigate to /feedback
   - [ ] Verify active link is highlighted correctly on each page
   - [ ] Check disclaimer text is visible and properly styled
   - [ ] Test on different screen sizes (responsive)

3. **Test DonationChart Component:**
   - [ ] Navigate to politician search and select a politician with donations
   - [ ] Verify donation chart loads and displays correctly
   - [ ] Check Chart.js console for errors (should be none)
   - [ ] Verify chart legend shows industries
   - [ ] Hover over chart sections - tooltips should show
   - [ ] If topic filtering implemented, test all topics
   - [ ] Test with politician who has no donations (should show message)
   - [ ] Verify chart is responsive on different screen sizes

4. **Test LoadingSpinner Component:**
   - [ ] Should appear during API calls (search, loading donations, etc.)
   - [ ] Verify animation is smooth and centered
   - [ ] Check optional message displays if provided
   - [ ] Test different size variants if implemented

5. **Test Feedback Page:**
   - [ ] Navigate to http://localhost:5173/feedback
   - [ ] Verify page renders with header
   - [ ] Content displays correctly
   - [ ] Navigation works from header
   - [ ] Take screenshot

**Critical Chart.js Checks:**
- [ ] NO console errors about Chart.js registration
- [ ] Chart renders on first load (not blank)
- [ ] Chart updates when data changes
- [ ] No memory leaks (chart destroys on unmount)

**Why Browser Testing is Critical for Shared Components:**
- Chart.js registration errors only show in browser console
- Navigation highlighting depends on React Router state
- Responsive design must be visually verified
- Animation smoothness can't be tested by compiler
- Other agents depend on these components working perfectly

---

## Integration with Other Agents

### What You Provide

**To Agent 2 (Politician Search):**
- `Header` component
- `LoadingSpinner` component
- `DonationChart` component (CRITICAL for politician details)

**To Agent 3 (Donor Search):**
- `Header` component
- `LoadingSpinner` component

**Export Pattern:**
All components should be exported as default exports from their files, making them easy to import:
```typescript
// Other agents import like this:
import Header from '../components/Header';
import LoadingSpinner from '../components/LoadingSpinner';
import DonationChart from '../components/DonationChart';
```

### Coordination

- Your components will be imported by Agents 2 and 3
- If you finish first, notify other agents components are ready
- If you finish after them, they may have placeholders - that's OK
- Other agents will replace placeholders with real components

---

## Files to Create

```
frontend/src/
├── components/
│   ├── Header.tsx
│   ├── LoadingSpinner.tsx
│   └── DonationChart.tsx
└── pages/
    └── Feedback.tsx
```

**Files to Modify:**
- `frontend/src/App.tsx` (add Header to layout)

---

## Reference: Original Templates

Review original templates to understand:
- Header layout and navigation
- Disclaimer text
- Chart display and formatting
- Color schemes

**Key elements to preserve:**
- Site title and branding
- Navigation structure
- Disclaimer message
- Chart color palette
- Data formatting in chart tooltips

---

## Tips

1. **Chart.js Registration is CRITICAL** - Don't skip this or chart won't render
2. **Test with real data** - Use actual politician IDs from API
3. **Responsive design matters** - Test on mobile and desktop
4. **Colors should be distinguishable** - Use accessible color palette
5. **Percentages must add to 100%** - Verify calculation logic
6. **Handle edge cases** - Empty data, loading, errors
7. **TypeScript is your friend** - Let types guide you

---

## Chart.js + React 19 Compatibility Notes

**Critical Points:**
1. MUST register components before use
2. Import from 'chart.js' not 'chart.js/auto'
3. Use react-chartjs-2 version compatible with React 19
4. Test thoroughly - Chart.js issues often appear at runtime

**If you encounter issues:**
- Check console for Chart.js errors
- Verify all required components registered
- Check react-chartjs-2 version compatibility
- Test with simple data first, then complex

---

## Timeline

**Estimated Duration:** 4-6 hours

Focus on getting Chart.js working correctly - this is the most critical component.

---

## Notes

- DonationChart is the most complex and important component
- Header will be visible on every page - make it good
- LoadingSpinner should be smooth and professional
- Chart.js registration MUST be done correctly for React 19
- Test all components with real data
- Document any Chart.js issues for future reference
