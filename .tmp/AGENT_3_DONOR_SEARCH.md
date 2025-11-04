# Agent 3: Donor Search Specialist

**Agent Type:** `frontend-ts-expert` or `react-specialist`
**Duration:** 2-3 hours (REDUCED from 4-6 - shadcn/ui components available)
**Dependencies:** CHECKPOINT 1 passed (Agent 1 complete) ✅
**Can Start:** ✅ READY NOW - All dependencies installed (can run PARALLEL with Agent 2)

## ⚡ CRITICAL UPDATE: shadcn/ui Components Installed

**Phase 1 delivered MORE than planned!**

You have **33 production-ready shadcn/ui components** available. DO NOT create UI components from scratch:

```tsx
// Import components directly
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
```

**This means:**
- ✅ No need to create DonorCard, ContributionHistory table from scratch
- ✅ Use shadcn Card for donor cards
- ✅ Use shadcn Table for contribution history
- ⚡ **50% faster implementation** - focus on business logic

## Overview

Build the complete Donor Search feature. This is a simpler feature than Politician Search - search for donors, view details, and display contribution history.

**Original Template:** `app/templates/donor_search.html` (252 lines) - ALL functionality must be preserved.

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

### 1. Create Custom Hook

Create `frontend/src/hooks/useDonorSearch.ts`:

```typescript
import { useState } from 'react';
import { api } from '../services/api';
import type { Donor, Donation } from '../types/api';

interface UseDonorSearchResult {
  query: string;
  setQuery: (query: string) => void;
  donors: Donor[];
  selectedDonor: Donor | null;
  donations: Donation[];
  isSearching: boolean;
  isLoadingDonations: boolean;
  searchError: string | null;
  donationsError: string | null;
  search: () => Promise<void>;
  selectDonor: (donor: Donor) => void;
  clearSelection: () => void;
}

export function useDonorSearch(): UseDonorSearchResult {
  const [query, setQuery] = useState('');
  const [donors, setDonors] = useState<Donor[]>([]);
  const [selectedDonor, setSelectedDonor] = useState<Donor | null>(null);
  const [donations, setDonations] = useState<Donation[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [isLoadingDonations, setIsLoadingDonations] = useState(false);
  const [searchError, setSearchError] = useState<string | null>(null);
  const [donationsError, setDonationsError] = useState<string | null>(null);

  const search = async () => {
    if (query.length < 3) {
      setDonors([]);
      return;
    }

    setIsSearching(true);
    setSearchError(null);

    try {
      const results = await api.searchDonors(query);
      setDonors(results);
    } catch (err) {
      setSearchError(err instanceof Error ? err.message : 'Search failed');
      setDonors([]);
    } finally {
      setIsSearching(false);
    }
  };

  const selectDonor = async (donor: Donor) => {
    setSelectedDonor(donor);
    setIsLoadingDonations(true);
    setDonationsError(null);

    try {
      const donationData = await api.getDonorDonations(donor.donorid);
      setDonations(donationData);
    } catch (err) {
      setDonationsError(err instanceof Error ? err.message : 'Failed to load donations');
      setDonations([]);
    } finally {
      setIsLoadingDonations(false);
    }
  };

  const clearSelection = () => {
    setSelectedDonor(null);
    setDonations([]);
  };

  return {
    query,
    setQuery,
    donors,
    selectedDonor,
    donations,
    isSearching,
    isLoadingDonations,
    searchError,
    donationsError,
    search,
    selectDonor,
    clearSelection,
  };
}
```

**Key Features:**
- Separate loading states for search and donations
- Separate error states for search and donations
- Minimum 3 character search requirement
- Automatic donation loading when donor selected

**Verify:**
- [ ] Hook compiles without TypeScript errors
- [ ] All state is properly typed
- [ ] Follows React hooks best practices

---

### 2. Create Donor Components

#### A. Donor Card

Create `frontend/src/components/DonorCard.tsx`:

Component displays a donor in search results.

**Props:**
```typescript
interface DonorCardProps {
  donor: Donor;
  onSelect: (donor: Donor) => void;
}
```

**Requirements:**
- Display: Donor Name, Type, Employer (if available), State (if available)
- Clickable to select donor
- Use Tailwind CSS for styling (match original design)
- Hover effects
- Handle optional fields gracefully (employer, state may be null)

**Example Layout:**
```
┌───────────────────────────────┐
│ John Smith                    │
│ Type: Individual              │
│ Employer: Google LLC          │
│ State: CA                     │
└───────────────────────────────┘
```

#### B. Donor Details

Create `frontend/src/components/DonorDetails.tsx`:

Header component showing donor information.

**Props:**
```typescript
interface DonorDetailsProps {
  donor: Donor;
  onClose: () => void;
}
```

**Requirements:**
- Display donor name (large, prominent)
- Display type
- Display employer (if available)
- Display state (if available)
- Close button to return to search
- Use Tailwind CSS

#### C. Contribution History

Create `frontend/src/components/ContributionHistory.tsx`:

Displays list of donations made by the donor.

**Props:**
```typescript
interface ContributionHistoryProps {
  donations: Donation[];
  isLoading: boolean;
  error: string | null;
}
```

**Requirements:**
- Display table/list of donations with columns:
  - Amount (formatted as currency: $X,XXX.XX)
  - Date (formatted: MM/DD/YYYY)
  - Politician (First + Last Name)
  - Party
  - State
- Show loading state while fetching
- Show error message if load fails
- Handle empty donations list
- Sort by date (most recent first, if not already sorted by API)
- Use Tailwind CSS

**Amount Formatting:**
```typescript
const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
};
```

**Date Formatting:**
```typescript
const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US');
};
```

---

### 3. Create Main Page

Create `frontend/src/pages/DonorSearch.tsx`:

Main page component that brings everything together.

**Requirements:**

1. **Search Interface**
   - Search input field
   - Search button
   - Minimum 3 characters to search (show message if < 3)
   - Show loading state during search
   - Show error messages
   - Display search results using DonorCard

2. **Results Display**
   - List of DonorCard components
   - Click card to view details and contribution history
   - Handle empty results with message
   - Results should be sorted alphabetically by name

3. **Detail View**
   - Show DonorDetails component when donor selected
   - Show ContributionHistory component with donation data
   - Hide search results when viewing details
   - Back/close button to return to search

4. **State Management**
   - Use `useDonorSearch` hook
   - Track current view (search vs details)
   - Preserve search results when viewing details

5. **Error Handling**
   - Display API errors to user
   - Handle network failures gracefully
   - Show appropriate messages for different error types

**Layout Structure:**
```
┌─────────────────────────────────────┐
│ Header (from Agent 4)               │
├─────────────────────────────────────┤
│ Search Bar                          │
│ [Input] [Search Button]             │
│ Min 3 characters                    │
├─────────────────────────────────────┤
│                                     │
│ EITHER:                             │
│   Search Results                    │
│   - DonorCard                       │
│   - DonorCard                       │
│   - ...                             │
│                                     │
│ OR:                                 │
│   Donor Details                     │
│   - Donor Info Header               │
│   - Contribution History            │
│     (table of donations)            │
│                                     │
└─────────────────────────────────────┘
```

**Preserve ALL Original Functionality:**
- Search with min 3 chars
- Display results list (alphabetically sorted)
- Select donor to view details
- View contribution history
- Amount formatting ($X,XXX.XX)
- Date formatting (MM/DD/YYYY)
- Return to search from details
- Handle missing data gracefully (employer, state)

**Styling:**
- Use Tailwind CSS exclusively
- Match the visual design of original template
- Responsive layout
- Consistent spacing and typography
- Table/list formatting for contributions

---

## ✅ VERIFICATION CHECKPOINT 3

Run through ALL verification steps before marking complete:

### Functionality Tests
- [ ] Search donors with query (min 3 chars) returns results
- [ ] Query < 3 chars shows appropriate message or returns empty
- [ ] Search results sorted alphabetically by name
- [ ] Click donor card shows details view
- [ ] Donor details display correctly:
  - [ ] Name
  - [ ] Type
  - [ ] Employer (or N/A if missing)
  - [ ] State (or N/A if missing)
- [ ] Contribution history displays correctly:
  - [ ] All donation records shown
  - [ ] Amount formatted as currency
  - [ ] Date formatted correctly
  - [ ] Politician name (first + last)
  - [ ] Party
  - [ ] State
- [ ] Loading state shows during search
- [ ] Loading state shows while loading donations
- [ ] Error messages display on API failures
- [ ] Back/close button returns to search
- [ ] Search results preserved when returning from details

### Code Quality
- [ ] No TypeScript errors (`npm run build` succeeds)
- [ ] No `any` types used
- [ ] All props have TypeScript interfaces
- [ ] Components follow React best practices
- [ ] Custom hook follows hooks rules

### Styling
- [ ] All styles use Tailwind CSS (no inline styles)
- [ ] Responsive layout works (mobile, tablet, desktop)
- [ ] Consistent with original design
- [ ] Table/list formatting is clean and readable

### Browser Tests
- [ ] No console errors
- [ ] No console warnings
- [ ] Browser back/forward buttons work correctly
- [ ] Page performance is acceptable

### Edge Cases
- [ ] Empty search results handled
- [ ] Donors with no employer/state handled
- [ ] Donors with no donations handled
- [ ] Very long donor names handled
- [ ] Large donation amounts formatted correctly

### Browser Testing (REQUIRED)
**Use MCP Chrome DevTools to verify the application works end-to-end:**

1. **Ensure Backend and Frontend are Running:**
   ```bash
   # Backend should be on port 5001
   # Frontend should be on port 5173 or 5174
   ```

2. **Test Donor Search in Browser:**
   - [ ] Navigate to http://localhost:5173/donor_search
   - [ ] Try searching with 1-2 characters (should not search yet)
   - [ ] Search with 3+ characters (e.g., "Google", "Smith")
   - [ ] Verify search results display correctly
   - [ ] Click on a donor card to view details
   - [ ] Verify donor details page displays:
     - Donor information (name, type, employer, state)
     - Contribution history table
     - Currency formatting ($X,XXX.XX)
     - Date formatting
   - [ ] Test back button to return to search
   - [ ] Verify search results are preserved
   - [ ] Check for console errors (should be none)
   - [ ] Take screenshots of working pages

**Example Search Queries to Test:**
- "Google" - Should find Google LLC and employees
- "Smith" - Should find many individuals
- "PAC" - Should find PACs
- Test with donors who have many donations
- Test with donors who have no donations

**Why Browser Testing is Critical:**
- Currency and date formatting only visible in browser
- API response handling bugs only show at runtime
- Layout issues invisible to TypeScript compiler
- User interaction flows must be manually verified

---

## Integration with Other Agents

### Dependencies on Agent 4 (Shared Components)
- **Header component:** Import from `../components/Header`
- **LoadingSpinner component:** Import from `../components/LoadingSpinner` (optional)

**If Agent 4 hasn't completed these:**
Create temporary placeholders and replace when available:
```typescript
// Temporary placeholders
const Header = () => <div>Header - Coming from Agent 4</div>;
```

### What You Provide to Integration
- Complete donor search feature
- All components in `frontend/src/components/`:
  - DonorCard.tsx
  - DonorDetails.tsx
  - ContributionHistory.tsx
- Hook in `frontend/src/hooks/`:
  - useDonorSearch.ts
- Complete page in `frontend/src/pages/DonorSearch.tsx`

---

## Files to Create

```
frontend/src/
├── hooks/
│   └── useDonorSearch.ts
├── components/
│   ├── DonorCard.tsx
│   ├── DonorDetails.tsx
│   └── ContributionHistory.tsx
└── pages/
    └── DonorSearch.tsx
```

---

## Reference: Original Template

**Location:** `app/templates/donor_search.html`

Review the original template to understand:
- Search behavior (min 3 chars)
- Display formatting
- Contribution history layout
- Data formatting (currency, dates)
- Interaction patterns

**Key behaviors to preserve:**
- Search requires min 3 characters
- Results displayed as cards
- Alphabetical sorting
- Click card for details and history
- Currency formatting
- Date formatting
- Handle missing employer/state

---

## Tips

1. **Start simple** - This is less complex than Politician Search
2. **Format data correctly** - Currency and dates must match original
3. **Handle optional fields** - Employer and state may be null
4. **Test with real data** - Use actual API responses
5. **Use the API service layer** - Don't create new fetch calls
6. **TypeScript is your friend** - Let types guide you
7. **Match original UX exactly** - Users expect the same behavior

---

## Timeline

**Estimated Duration:** 4-6 hours

This is a simpler feature than Politician Search. Focus on data formatting and clean presentation.

---

## Notes

- Simpler than Politician Search - no complex filtering or pagination
- Focus on clean data presentation
- Currency and date formatting must be correct
- Handle optional fields gracefully (employer, state)
- TypeScript strict mode - no shortcuts
- Test with donors that have many donations
- Test with donors that have no employer/state
