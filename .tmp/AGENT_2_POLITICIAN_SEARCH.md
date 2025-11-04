# Agent 2: Politician Search Specialist

**Agent Type:** `frontend-ts-expert` or `typescript-pro`
**Duration:** 4-6 hours (REDUCED from 8-12 - shadcn/ui components available)
**Dependencies:** CHECKPOINT 1 passed (Agent 1 complete) ✅
**Can Start:** ✅ READY NOW - All dependencies installed

## ⚡ CRITICAL UPDATE: shadcn/ui Components Installed

**Phase 1 delivered MORE than planned!**

Instead of creating components from scratch, you now have **33 production-ready shadcn/ui components** available:

```tsx
// Import components directly - DO NOT create from scratch
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Pagination, PaginationContent, PaginationItem, PaginationLink } from '@/components/ui/pagination'
```

**This means:**
- ✅ No need to create Button, Input, Card, Table components
- ✅ Built-in accessibility (Radix UI primitives)
- ✅ Built-in animations and interactions
- ✅ Consistent styling (already configured)
- ⚡ **50% faster implementation**

**Focus your time on:**
- Business logic (search, filtering, pagination)
- API integration
- Data transformation and state management
- Component composition (using shadcn components)

## Overview

Build the complete Politician Search feature - the most complex page in the application. This includes search functionality, politician details display, donation charts with filtering, and comprehensive vote records with pagination and filtering.

**Original Template:** `app/templates/index.html` (836 lines) - ALL functionality must be preserved.

---

## Prerequisites

Before starting, verify you have:
- ✅ Working Vite dev server (`npm run dev`)
- ✅ `frontend/src/types/api.ts` with all type definitions
- ✅ `frontend/src/services/api.ts` with all API functions
- ✅ `frontend/src/App.tsx` with routing structure
- ✅ Flask backend running on port 5000

---

## Tasks

### 1. Create Custom Hooks

#### A. Politician Search Hook

Create `frontend/src/hooks/usePoliticianSearch.ts`:

```typescript
import { useState } from 'react';
import { api } from '../services/api';
import type { Politician } from '../types/api';

interface UsePoliticianSearchResult {
  query: string;
  setQuery: (query: string) => void;
  politicians: Politician[];
  selectedPolitician: Politician | null;
  isLoading: boolean;
  error: string | null;
  search: () => Promise<void>;
  selectPolitician: (politician: Politician) => void;
  clearSelection: () => void;
}

export function usePoliticianSearch(): UsePoliticianSearchResult {
  const [query, setQuery] = useState('');
  const [politicians, setPoliticians] = useState<Politician[]>([]);
  const [selectedPolitician, setSelectedPolitician] = useState<Politician | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const search = async () => {
    if (query.length < 2) {
      setPoliticians([]);
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const results = await api.searchPoliticians(query);
      setPoliticians(results);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Search failed');
      setPoliticians([]);
    } finally {
      setIsLoading(false);
    }
  };

  const selectPolitician = (politician: Politician) => {
    setSelectedPolitician(politician);
  };

  const clearSelection = () => {
    setSelectedPolitician(null);
  };

  return {
    query,
    setQuery,
    politicians,
    selectedPolitician,
    isLoading,
    error,
    search,
    selectPolitician,
    clearSelection,
  };
}
```

#### B. Votes Hook

Create `frontend/src/hooks/useVotes.ts`:

```typescript
import { useState, useEffect } from 'react';
import { api } from '../services/api';
import type { VoteResponse, VoteParams } from '../types/api';

interface UseVotesResult {
  voteData: VoteResponse | null;
  isLoading: boolean;
  error: string | null;
  currentPage: number;
  sortOrder: 'ASC' | 'DESC';
  billType: string;
  subject: string;
  setCurrentPage: (page: number) => void;
  setSortOrder: (order: 'ASC' | 'DESC') => void;
  setBillType: (type: string) => void;
  setSubject: (subject: string) => void;
  loadVotes: (politicianId: string) => Promise<void>;
}

export function useVotes(): UseVotesResult {
  const [voteData, setVoteData] = useState<VoteResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [sortOrder, setSortOrder] = useState<'ASC' | 'DESC'>('DESC');
  const [billType, setBillType] = useState('');
  const [subject, setSubject] = useState('');
  const [politicianId, setPoliticianId] = useState<string | null>(null);

  const loadVotes = async (id: string) => {
    setPoliticianId(id);
    setIsLoading(true);
    setError(null);

    try {
      const params: VoteParams = {
        page: currentPage,
        sort: sortOrder,
      };

      if (billType) params.type = billType;
      if (subject) params.subject = subject;

      const data = await api.getPoliticianVotes(id, params);
      setVoteData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load votes');
      setVoteData(null);
    } finally {
      setIsLoading(false);
    }
  };

  // Reload when filters change
  useEffect(() => {
    if (politicianId) {
      loadVotes(politicianId);
    }
  }, [currentPage, sortOrder, billType, subject]);

  return {
    voteData,
    isLoading,
    error,
    currentPage,
    sortOrder,
    billType,
    subject,
    setCurrentPage,
    setSortOrder,
    setBillType,
    setSubject,
    loadVotes,
  };
}
```

**Verify:**
- [ ] Both hooks compile without TypeScript errors
- [ ] All state management logic is typed
- [ ] Hooks follow React hooks best practices

---

### 2. Create Politician Components

#### A. Politician Card

Create `frontend/src/components/PoliticianCard.tsx`:

Component displays a politician in search results. Clicking the card should trigger selection.

**Props:**
```typescript
interface PoliticianCardProps {
  politician: Politician;
  onSelect: (politician: Politician) => void;
}
```

**Requirements:**
- Display: Name, Party, State, Role (if available)
- Show active/inactive status
- Clickable to select politician
- Use Tailwind CSS for styling (match original design)
- Hover effects

#### B. Politician Details

Create `frontend/src/components/PoliticianDetails.tsx`:

Main detail view component that orchestrates the politician's information display.

**Props:**
```typescript
interface PoliticianDetailsProps {
  politician: Politician;
  onClose: () => void;
}
```

**Requirements:**
- Display politician header (name, party, state, role)
- Include DonationChart component (import from shared - Agent 4 creates this)
- Include VoteRecord component
- Close button to return to search
- Use Tailwind CSS

**Note:** This component imports `DonationChart` from `../components/DonationChart`. Agent 4 creates that component. If not yet available, create a placeholder:
```typescript
// Temporary placeholder if Agent 4 hasn't finished
const DonationChart = ({ politicianId }: { politicianId: string }) => (
  <div>Donation Chart - Coming from Agent 4</div>
);
```

#### C. Vote Record

Create `frontend/src/components/VoteRecord.tsx`:

Displays paginated vote history with filtering capabilities.

**Props:**
```typescript
interface VoteRecordProps {
  politicianId: string;
}
```

**Requirements:**
- Use `useVotes` hook for state management
- Display vote table with columns: Vote, Bill Number, Title, Date Introduced, Subjects
- Pagination controls (prev/next, page numbers)
- Include VoteFilters component
- Show loading state
- Show error state
- Handle empty results
- Use Tailwind CSS

**Vote Display Colors (match original):**
- Yea: Green background
- Nay: Red background
- Present: Yellow background
- Not Voting: Gray background

#### D. Vote Filters

Create `frontend/src/components/VoteFilters.tsx`:

Filtering UI for vote records.

**Props:**
```typescript
interface VoteFiltersProps {
  billType: string;
  setBillType: (type: string) => void;
  subject: string;
  setSubject: (subject: string) => void;
  sortOrder: 'ASC' | 'DESC';
  setSortOrder: (order: 'ASC' | 'DESC') => void;
  availableSubjects: string[];
}
```

**Requirements:**
- Bill Type filter: Checkboxes for HR, S (can select multiple)
- Subject filter: Dropdown or searchable select
- Sort order toggle: ASC/DESC button
- Clear filters button
- Use Tailwind CSS

**Note:** Load available subjects using `api.getBillSubjects()` on component mount.

---

### 3. Create Main Page

Create `frontend/src/pages/PoliticianSearch.tsx`:

Main page component that brings everything together.

**Requirements:**

1. **Search Interface**
   - Search input field
   - Search button
   - Minimum 2 characters to search
   - Show loading state during search
   - Show error messages
   - Display search results using PoliticianCard

2. **Results Display**
   - List of PoliticianCard components
   - Click card to view details
   - Handle empty results with message

3. **Detail View**
   - Show PoliticianDetails component when politician selected
   - Hide search results when viewing details
   - Back/close button to return to search

4. **State Management**
   - Use `usePoliticianSearch` hook
   - Track current view (search vs details)
   - Preserve search results when viewing details

5. **Error Handling**
   - Display API errors to user
   - Handle network failures gracefully
   - Show appropriate messages

**Layout Structure:**
```
┌─────────────────────────────────────┐
│ Header (from Agent 4)               │
├─────────────────────────────────────┤
│ Search Bar                          │
│ [Input] [Search Button]             │
├─────────────────────────────────────┤
│                                     │
│ EITHER:                             │
│   Search Results                    │
│   - PoliticianCard                  │
│   - PoliticianCard                  │
│   - ...                             │
│                                     │
│ OR:                                 │
│   Politician Details                │
│   - Header                          │
│   - Donation Chart                  │
│   - Vote Record                     │
│                                     │
└─────────────────────────────────────┘
```

**Preserve ALL Original Functionality:**
- Search with min 2 chars
- Display results list
- Select politician to view details
- View donation chart (with topic filtering)
- View vote record (with pagination)
- Filter votes (by bill type, subject)
- Sort votes (ASC/DESC)
- Click subject tags to filter by that subject
- Return to search from details

**Styling:**
- Use Tailwind CSS exclusively
- Match the visual design of original template
- Responsive layout
- Consistent spacing and typography

---

## ✅ VERIFICATION CHECKPOINT 2

Run through ALL verification steps before marking complete:

### Functionality Tests
- [ ] Search politicians with query (min 2 chars) returns results
- [ ] Short query (< 2 chars) shows appropriate message
- [ ] Click politician card shows details view
- [ ] Politician details display correctly (name, party, state, role)
- [ ] Donation chart displays (or placeholder if Agent 4 not done)
- [ ] Vote record displays with pagination
- [ ] Pagination controls work (prev/next)
- [ ] Page numbers display correctly
- [ ] Vote filters work:
  - [ ] Bill type filter (HR, S, multiple)
  - [ ] Subject filter
  - [ ] Sort order toggle
- [ ] Click subject tag filters votes by that subject
- [ ] Clear filters button works
- [ ] Back/close button returns to search
- [ ] Search results preserved when returning from details
- [ ] Loading states display during API calls
- [ ] Error messages display on API failures

### Code Quality
- [ ] No TypeScript errors (`npm run build` succeeds)
- [ ] No `any` types used
- [ ] All props have TypeScript interfaces
- [ ] Components follow React best practices
- [ ] Custom hooks follow hooks rules

### Styling
- [ ] All styles use Tailwind CSS (no inline styles)
- [ ] Vote colors correct (Yea=green, Nay=red, Present=yellow, Not Voting=gray)
- [ ] Responsive layout works (mobile, tablet, desktop)
- [ ] Consistent with original design

### Browser Tests
- [ ] No console errors
- [ ] No console warnings
- [ ] Browser back/forward buttons work correctly
- [ ] Page performance is acceptable

### End-to-End Browser Testing (REQUIRED)
**Use MCP Chrome DevTools to verify the complete politician search flow:**

1. **Ensure Backend and Frontend are Running:**
   ```bash
   # Terminal 1: Backend on port 5001
   source .venv/bin/activate
   python -m app.main

   # Terminal 2: Frontend on port 5173/5174
   cd frontend && pnpm run dev
   ```

2. **Ensure Database is Loaded:**
   ```bash
   # If not already loaded:
   cd bin && tar -xjf sql_data.tar.bz2
   cd sql && python ../../bin/load_sql.py
   # Should see: 2600 politicians, 989K votes, 1.75M donations
   ```

3. **Test Politician Search Flow:**
   - [ ] Navigate to http://localhost:5173/
   - [ ] Try searching with 1 character (should show validation message)
   - [ ] Search with 2+ characters (e.g., "Warren", "Miller", "Smith")
   - [ ] Verify search results display with:
     - Party colors (Republican=red, Democratic=blue)
     - Active/Inactive badges
     - State and role information
   - [ ] Click on a politician card to view details

4. **Test Politician Details Page:**
   - [ ] Verify politician header displays correctly
   - [ ] Check donation chart section (placeholder for Agent 4 is OK)
   - [ ] Verify vote record table displays with:
     - Vote colors (Yea=green, Nay=red, Present=yellow, Not Voting=gray)
     - Bill numbers, titles, dates, subjects
     - Proper date formatting (e.g., "Dec 16, 2024")

5. **Test Vote Filtering and Pagination:**
   - [ ] Click page 2 button - should load different votes
   - [ ] Verify pagination shows correct page numbers
   - [ ] Previous/Next buttons enable/disable correctly
   - [ ] Test bill type checkboxes (HR, S)
   - [ ] Test subject dropdown - should load 100+ subjects
   - [ ] Test sort order toggle (Newest First / Oldest First)
   - [ ] Click a subject tag - should filter votes by that subject
   - [ ] Test Clear All Filters button

6. **Test Navigation:**
   - [ ] Click "Back to Search" - should return to search results
   - [ ] Verify search results are preserved
   - [ ] Test browser back button
   - [ ] Check console for errors (should be none)

**Politicians with Good Test Data:**
- "Warren" - Returns 4 politicians, but Elizabeth Warren has 0 votes
- "Miller" - Returns 13 politicians, Gary G. Miller has 1,999 votes
- "Smith" - Returns many results with varying vote counts

**Why This Testing is Critical:**
- Found and fixed Select component bug during testing (empty value error)
- Pagination logic only verifiable in browser
- Vote color coding must be visually confirmed
- API response handling errors only show at runtime
- Subject tag click-to-filter functionality requires interaction testing

---

## Integration with Other Agents

### Dependencies on Agent 4 (Shared Components)
- **Header component:** Import from `../components/Header`
- **DonationChart component:** Import from `../components/DonationChart`
- **LoadingSpinner component:** Import from `../components/LoadingSpinner` (optional)

**If Agent 4 hasn't completed these:**
Create temporary placeholders and replace when available:
```typescript
// Temporary placeholders
const Header = () => <div>Header - Coming from Agent 4</div>;
const DonationChart = ({ politicianId }: { politicianId: string }) =>
  <div>Donation Chart - Coming from Agent 4</div>;
```

### What You Provide to Integration
- Complete politician search feature
- All components in `frontend/src/components/`:
  - PoliticianCard.tsx
  - PoliticianDetails.tsx
  - VoteRecord.tsx
  - VoteFilters.tsx
- All hooks in `frontend/src/hooks/`:
  - usePoliticianSearch.ts
  - useVotes.ts
- Complete page in `frontend/src/pages/PoliticianSearch.tsx`

---

## Files to Create

```
frontend/src/
├── hooks/
│   ├── usePoliticianSearch.ts
│   └── useVotes.ts
├── components/
│   ├── PoliticianCard.tsx
│   ├── PoliticianDetails.tsx
│   ├── VoteRecord.tsx
│   └── VoteFilters.tsx
└── pages/
    └── PoliticianSearch.tsx
```

---

## Reference: Original Template

**Location:** `app/templates/index.html`

Review the original template to understand:
- Search behavior
- Display formatting
- Interaction patterns
- Vote color coding
- Subject tag interactions
- Pagination logic

**Key behaviors to preserve:**
- Search requires min 2 characters
- Results displayed as cards
- Click card for details
- Donation chart with topic filtering
- Vote record with pagination (default page 1)
- Vote filtering by bill type (HR, S)
- Vote filtering by subject
- Sort order toggle
- Subject tags are clickable to filter
- All data formatting (dates, amounts, etc.)

---

## Tips

1. **Start with hooks** - Get state management working first
2. **Build components bottom-up** - Card → Details → Page
3. **Test incrementally** - Verify each component before moving on
4. **Use the API service layer** - Don't create new fetch calls
5. **TypeScript is your friend** - Let types guide you
6. **Match original UX exactly** - Users expect the same behavior
7. **Ask for help** - If blocked on Agent 4 components, use placeholders

---

## Timeline

**Estimated Duration:** 8-12 hours

This is the most complex feature. Take your time and test thoroughly.

---

## Notes

- This is the primary user-facing feature - quality is critical
- Vote filtering is complex - test all combinations
- Pagination logic must be correct
- All original functionality must be preserved
- TypeScript strict mode - no shortcuts
