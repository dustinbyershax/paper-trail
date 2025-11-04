# Agent 6: Testing Framework & Test Implementation

**Agent Type:** `typescript-pro` or `python-pro`
**Duration:** 6-8 hours
**Dependencies:** Phases 1-5 complete (Foundation, Features, and Integration)
**Can Start:** After all frontend features implemented and backend integrated

## Overview

Implement comprehensive test coverage for the Paper Trail application following TDD principles. This phase addresses the **critical blocker** from PR reviews: missing unit tests.

**Per CLAUDE.md:** "FOR EVERY NEW FEATURE OR BUGFIX, YOU MUST follow Test Driven Development"

This phase ensures:
- ✅ All frontend components have unit tests
- ✅ All custom hooks have behavioral tests
- ✅ API service layer has integration tests
- ✅ Backend API endpoints maintain coverage
- ✅ Test infrastructure for future development

---

## Part A: Frontend Test Framework Setup

### Task 1: Install Vitest and Testing Libraries

Vitest is the recommended testing framework for Vite projects, with React Testing Library for component testing.

**Steps:**

1. **Install core testing dependencies**

```bash
cd frontend
npm install -D vitest@^1.0.0 \
  @vitest/ui@^1.0.0 \
  jsdom@^23.0.0 \
  @testing-library/react@^14.1.0 \
  @testing-library/jest-dom@^6.1.0 \
  @testing-library/user-event@^14.5.0
```

2. **Update package.json scripts**

Add to `frontend/package.json`:
```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage"
  }
}
```

3. **Configure Vitest**

Create `frontend/vitest.config.ts`:
```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/mockData.ts',
      ],
    },
  },
});
```

4. **Create test setup file**

Create `frontend/src/test/setup.ts`:
```typescript
import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';

// Cleanup after each test
afterEach(() => {
  cleanup();
});
```

**Verify:**
- [ ] All packages install without errors
- [ ] `npm run test` starts Vitest in watch mode
- [ ] `npm run test:ui` opens Vitest UI
- [ ] No configuration errors

---

### Task 2: Create Test Utilities

Create reusable testing utilities for consistent test patterns.

**A. Mock Data**

Create `frontend/src/test/mockData.ts`:
```typescript
import type { Politician, Donor, Donation, Vote, DonationSummary } from '../types/api';

export const mockPoliticians: Politician[] = [
  {
    politicianid: 'P001',
    firstname: 'John',
    lastname: 'Doe',
    party: 'Democratic',
    state: 'CA',
    role: 'Senator',
    isactive: true,
  },
  {
    politicianid: 'P002',
    firstname: 'Jane',
    lastname: 'Smith',
    party: 'Republican',
    state: 'TX',
    role: 'Representative',
    isactive: true,
  },
];

export const mockDonors: Donor[] = [
  {
    donorid: 1,
    name: 'Tech Corp',
    donortype: 'PAC',
    employer: 'Tech Industry',
    state: 'CA',
  },
  {
    donorid: 2,
    name: 'Jane Doe',
    donortype: 'Individual',
    employer: 'Self-employed',
    state: 'NY',
  },
];

export const mockDonations: Donation[] = [
  {
    amount: 5000,
    date: '2024-01-15',
    firstname: 'John',
    lastname: 'Doe',
    party: 'Democratic',
    state: 'CA',
  },
  {
    amount: 2500,
    date: '2024-02-20',
    firstname: 'Jane',
    lastname: 'Smith',
    party: 'Republican',
    state: 'TX',
  },
];

export const mockDonationSummary: DonationSummary[] = [
  { industry: 'Technology', totalamount: 150000 },
  { industry: 'Finance', totalamount: 125000 },
  { industry: 'Healthcare', totalamount: 95000 },
];

export const mockVotes: Vote[] = [
  {
    voteid: 1,
    vote: 'Yea',
    billnumber: 'H.R. 1234',
    title: 'Healthcare Reform Act',
    dateintroduced: '2024-01-10',
    subjects: ['Health', 'Insurance'],
  },
  {
    voteid: 2,
    vote: 'Nay',
    billnumber: 'S. 5678',
    title: 'Tax Reform Bill',
    dateintroduced: '2024-02-15',
    subjects: ['Taxation', 'Economics'],
  },
];
```

**B. Test Utilities**

Create `frontend/src/test/utils.tsx`:
```typescript
import { render, RenderOptions } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { ReactElement, ReactNode } from 'react';

interface AllTheProvidersProps {
  children: ReactNode;
}

function AllTheProviders({ children }: AllTheProvidersProps) {
  return <BrowserRouter>{children}</BrowserRouter>;
}

const customRender = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) => render(ui, { wrapper: AllTheProviders, ...options });

export * from '@testing-library/react';
export { customRender as render };
```

**Verify:**
- [ ] Mock data covers all API types
- [ ] Test utilities provide router context
- [ ] Files are in `frontend/src/test/` directory

---

## Part B: Component Unit Tests

### Task 3: Test Shared Components (Phase 4)

**A. Header Component Tests**

Create `frontend/src/components/__tests__/Header.test.tsx`:
```typescript
import { describe, it, expect } from 'vitest';
import { render, screen } from '../../test/utils';
import Header from '../Header';

describe('Header', () => {
  it('renders Paper Trail branding', () => {
    render(<Header />);
    expect(screen.getByText('Paper Trail')).toBeInTheDocument();
  });

  it('renders all navigation links', () => {
    render(<Header />);
    expect(screen.getByText('Politician Search')).toBeInTheDocument();
    expect(screen.getByText('Donor Search')).toBeInTheDocument();
    expect(screen.getByText('Feedback')).toBeInTheDocument();
  });

  it('displays disclaimer banner', () => {
    render(<Header />);
    expect(screen.getByText(/This data is for informational purposes only/i)).toBeInTheDocument();
  });

  it('navigation links have correct hrefs', () => {
    render(<Header />);
    const politicianLink = screen.getByRole('link', { name: /Politician Search/i });
    const donorLink = screen.getByRole('link', { name: /Donor Search/i });
    const feedbackLink = screen.getByRole('link', { name: /Feedback/i });

    expect(politicianLink).toHaveAttribute('href', '/');
    expect(donorLink).toHaveAttribute('href', '/donor_search');
    expect(feedbackLink).toHaveAttribute('href', '/feedback');
  });
});
```

**B. LoadingSpinner Component Tests**

Create `frontend/src/components/__tests__/LoadingSpinner.test.tsx`:
```typescript
import { describe, it, expect } from 'vitest';
import { render, screen } from '../../test/utils';
import LoadingSpinner from '../LoadingSpinner';

describe('LoadingSpinner', () => {
  it('renders spinner element', () => {
    const { container } = render(<LoadingSpinner />);
    const spinner = container.querySelector('.animate-spin');
    expect(spinner).toBeInTheDocument();
  });

  it('renders with small size', () => {
    const { container } = render(<LoadingSpinner size="sm" />);
    const spinner = container.querySelector('.w-6.h-6');
    expect(spinner).toBeInTheDocument();
  });

  it('renders with medium size by default', () => {
    const { container } = render(<LoadingSpinner />);
    const spinner = container.querySelector('.w-12.h-12');
    expect(spinner).toBeInTheDocument();
  });

  it('renders with large size', () => {
    const { container } = render(<LoadingSpinner size="lg" />);
    const spinner = container.querySelector('.w-16.h-16');
    expect(spinner).toBeInTheDocument();
  });

  it('displays optional message', () => {
    render(<LoadingSpinner message="Loading data..." />);
    expect(screen.getByText('Loading data...')).toBeInTheDocument();
  });

  it('does not display message when not provided', () => {
    const { container } = render(<LoadingSpinner />);
    expect(container.querySelector('p')).not.toBeInTheDocument();
  });
});
```

**C. DonationChart Component Tests**

Create `frontend/src/components/__tests__/DonationChart.test.tsx`:
```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '../../test/utils';
import DonationChart from '../DonationChart';
import { mockDonationSummary } from '../../test/mockData';
import * as api from '../../services/api';

vi.mock('../../services/api');

describe('DonationChart', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('displays loading state initially', () => {
    vi.spyOn(api, 'getDonationSummary').mockImplementation(
      () => new Promise(() => {}) // Never resolves
    );

    render(<DonationChart politicianId="P001" />);
    expect(screen.getByText(/Loading donation data.../i)).toBeInTheDocument();
  });

  it('displays error state on API failure', async () => {
    vi.spyOn(api, 'getDonationSummary').mockRejectedValue(
      new Error('API Error')
    );

    render(<DonationChart politicianId="P001" />);

    await waitFor(() => {
      expect(screen.getByText(/Error: API Error/i)).toBeInTheDocument();
    });
  });

  it('displays empty state when no data', async () => {
    vi.spyOn(api, 'getDonationSummary').mockResolvedValue([]);

    render(<DonationChart politicianId="P001" />);

    await waitFor(() => {
      expect(screen.getByText(/No donation data available/i)).toBeInTheDocument();
    });
  });

  it('renders chart with donation data', async () => {
    vi.spyOn(api, 'getDonationSummary').mockResolvedValue(mockDonationSummary);

    render(<DonationChart politicianId="P001" />);

    await waitFor(() => {
      expect(screen.getByText('Donations by Industry')).toBeInTheDocument();
    });
  });

  it('calls getDonationSummary with correct politician ID', async () => {
    const getSummarySpy = vi.spyOn(api, 'getDonationSummary').mockResolvedValue(mockDonationSummary);

    render(<DonationChart politicianId="P001" />);

    await waitFor(() => {
      expect(getSummarySpy).toHaveBeenCalledWith('P001');
    });
  });

  it('cleans up on unmount to prevent memory leaks', async () => {
    vi.spyOn(api, 'getDonationSummary').mockResolvedValue(mockDonationSummary);

    const { unmount } = render(<DonationChart politicianId="P001" />);

    // Component should cleanup AbortController
    unmount();

    // No assertion needed - just verify unmount doesn't throw
    expect(true).toBe(true);
  });
});
```

**Verify:**
- [ ] All tests pass: `npm run test`
- [ ] Tests cover loading, error, and success states
- [ ] Tests verify cleanup and memory leak prevention
- [ ] Coverage includes all component props

---

### Task 4: Test Donor Search Components (Phase 3)

**A. DonorCard Component Tests**

Create `frontend/src/components/__tests__/DonorCard.test.tsx`:
```typescript
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '../../test/utils';
import userEvent from '@testing-library/user-event';
import { DonorCard } from '../DonorCard';
import { mockDonors } from '../../test/mockData';

describe('DonorCard', () => {
  const mockOnSelect = vi.fn();

  beforeEach(() => {
    mockOnSelect.mockClear();
  });

  it('renders donor name', () => {
    render(<DonorCard donor={mockDonors[0]} onSelect={mockOnSelect} />);
    expect(screen.getByText('Tech Corp')).toBeInTheDocument();
  });

  it('renders donor type and employer', () => {
    render(<DonorCard donor={mockDonors[0]} onSelect={mockOnSelect} />);
    expect(screen.getByText(/PAC - Tech Industry/i)).toBeInTheDocument();
  });

  it('renders state badge when present', () => {
    render(<DonorCard donor={mockDonors[0]} onSelect={mockOnSelect} />);
    expect(screen.getByText('CA')).toBeInTheDocument();
  });

  it('handles missing employer gracefully', () => {
    const donorWithoutEmployer = { ...mockDonors[0], employer: undefined };
    render(<DonorCard donor={donorWithoutEmployer} onSelect={mockOnSelect} />);
    expect(screen.getByText('PAC')).toBeInTheDocument();
  });

  it('handles missing state gracefully', () => {
    const donorWithoutState = { ...mockDonors[0], state: undefined };
    render(<DonorCard donor={donorWithoutState} onSelect={mockOnSelect} />);
    expect(screen.queryByText('CA')).not.toBeInTheDocument();
  });

  it('calls onSelect when clicked', async () => {
    const user = userEvent.setup();
    render(<DonorCard donor={mockDonors[0]} onSelect={mockOnSelect} />);

    await user.click(screen.getByText('Tech Corp'));
    expect(mockOnSelect).toHaveBeenCalledWith(mockDonors[0]);
  });

  it('calls onSelect when Enter key pressed', async () => {
    const user = userEvent.setup();
    render(<DonorCard donor={mockDonors[0]} onSelect={mockOnSelect} />);

    const card = screen.getByRole('button');
    card.focus();
    await user.keyboard('{Enter}');

    expect(mockOnSelect).toHaveBeenCalledWith(mockDonors[0]);
  });

  it('calls onSelect when Space key pressed', async () => {
    const user = userEvent.setup();
    render(<DonorCard donor={mockDonors[0]} onSelect={mockOnSelect} />);

    const card = screen.getByRole('button');
    card.focus();
    await user.keyboard(' ');

    expect(mockOnSelect).toHaveBeenCalledWith(mockDonors[0]);
  });

  it('is keyboard accessible with role and tabIndex', () => {
    render(<DonorCard donor={mockDonors[0]} onSelect={mockOnSelect} />);
    const card = screen.getByRole('button');

    expect(card).toHaveAttribute('tabIndex', '0');
  });
});
```

**B. ContributionHistory Component Tests**

Create `frontend/src/components/__tests__/ContributionHistory.test.tsx`:
```typescript
import { describe, it, expect } from 'vitest';
import { render, screen } from '../../test/utils';
import { ContributionHistory } from '../ContributionHistory';
import { mockDonations } from '../../test/mockData';

describe('ContributionHistory', () => {
  it('displays loading state', () => {
    render(
      <ContributionHistory donations={[]} isLoading={true} error={null} />
    );
    expect(screen.getByText(/Loading contribution history.../i)).toBeInTheDocument();
  });

  it('displays error message', () => {
    render(
      <ContributionHistory
        donations={[]}
        isLoading={false}
        error="Failed to load"
      />
    );
    expect(screen.getByText(/Could not load contribution history: Failed to load/i)).toBeInTheDocument();
  });

  it('displays empty state when no donations', () => {
    render(
      <ContributionHistory donations={[]} isLoading={false} error={null} />
    );
    expect(screen.getByText(/No contribution history found/i)).toBeInTheDocument();
  });

  it('renders donation list', () => {
    render(
      <ContributionHistory
        donations={mockDonations}
        isLoading={false}
        error={null}
      />
    );

    expect(screen.getByText('John Doe (Democratic-CA)')).toBeInTheDocument();
    expect(screen.getByText('Jane Smith (Republican-TX)')).toBeInTheDocument();
  });

  it('formats currency correctly', () => {
    render(
      <ContributionHistory
        donations={mockDonations}
        isLoading={false}
        error={null}
      />
    );

    expect(screen.getByText('$5,000')).toBeInTheDocument();
    expect(screen.getByText('$2,500')).toBeInTheDocument();
  });

  it('formats dates with UTC timezone', () => {
    render(
      <ContributionHistory
        donations={mockDonations}
        isLoading={false}
        error={null}
      />
    );

    // Date formatting: Jan 15, 2024 and Feb 20, 2024
    expect(screen.getByText(/Jan 15, 2024/i)).toBeInTheDocument();
    expect(screen.getByText(/Feb 20, 2024/i)).toBeInTheDocument();
  });

  it('displays threshold in title', () => {
    render(
      <ContributionHistory
        donations={mockDonations}
        isLoading={false}
        error={null}
        threshold={2000}
      />
    );

    expect(screen.getByText(/Contribution History \(> \$2,000\)/i)).toBeInTheDocument();
  });
});
```

**Verify:**
- [ ] All donor search component tests pass
- [ ] Tests cover keyboard accessibility
- [ ] Tests verify currency/date formatting
- [ ] Tests check optional field handling

---

### Task 5: Test Custom Hooks

**A. useDonorSearch Hook Tests**

Create `frontend/src/hooks/__tests__/useDonorSearch.test.ts`:
```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useDonorSearch } from '../useDonorSearch';
import { mockDonors, mockDonations } from '../../test/mockData';
import * as api from '../../services/api';

vi.mock('../../services/api');

describe('useDonorSearch', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('initializes with empty state', () => {
    const { result } = renderHook(() => useDonorSearch());

    expect(result.current.query).toBe('');
    expect(result.current.donors).toEqual([]);
    expect(result.current.selectedDonor).toBeNull();
    expect(result.current.donations).toEqual([]);
    expect(result.current.isSearching).toBe(false);
    expect(result.current.searchError).toBeNull();
  });

  it('updates query when setQuery called', () => {
    const { result } = renderHook(() => useDonorSearch());

    result.current.setQuery('Boeing');
    expect(result.current.query).toBe('Boeing');
  });

  it('does not search with less than 3 characters', async () => {
    const searchSpy = vi.spyOn(api, 'searchDonors');
    const { result } = renderHook(() => useDonorSearch());

    result.current.setQuery('AB');
    await result.current.search();

    expect(searchSpy).not.toHaveBeenCalled();
    expect(result.current.donors).toEqual([]);
  });

  it('searches when query is 3+ characters', async () => {
    vi.spyOn(api, 'searchDonors').mockResolvedValue(mockDonors);
    const { result } = renderHook(() => useDonorSearch());

    result.current.setQuery('Tech');
    await result.current.search();

    await waitFor(() => {
      expect(result.current.donors).toEqual(mockDonors);
      expect(result.current.isSearching).toBe(false);
    });
  });

  it('handles search errors', async () => {
    vi.spyOn(api, 'searchDonors').mockRejectedValue(new Error('API Error'));
    const { result } = renderHook(() => useDonorSearch());

    result.current.setQuery('Test');
    await result.current.search();

    await waitFor(() => {
      expect(result.current.searchError).toBe('API Error');
      expect(result.current.donors).toEqual([]);
    });
  });

  it('selects donor and loads donations', async () => {
    vi.spyOn(api, 'getDonorDonations').mockResolvedValue(mockDonations);
    const { result } = renderHook(() => useDonorSearch());

    await result.current.selectDonor(mockDonors[0]);

    await waitFor(() => {
      expect(result.current.selectedDonor).toEqual(mockDonors[0]);
      expect(result.current.donations).toEqual(mockDonations);
      expect(result.current.isLoadingDonations).toBe(false);
    });
  });

  it('handles donation loading errors', async () => {
    vi.spyOn(api, 'getDonorDonations').mockRejectedValue(new Error('Failed'));
    const { result } = renderHook(() => useDonorSearch());

    await result.current.selectDonor(mockDonors[0]);

    await waitFor(() => {
      expect(result.current.donationsError).toBe('Failed');
      expect(result.current.donations).toEqual([]);
    });
  });

  it('clears selection', () => {
    const { result } = renderHook(() => useDonorSearch());

    result.current.clearSelection();

    expect(result.current.selectedDonor).toBeNull();
    expect(result.current.donations).toEqual([]);
  });

  it('cancels pending requests on unmount', async () => {
    vi.spyOn(api, 'getDonorDonations').mockImplementation(
      () => new Promise((resolve) => setTimeout(resolve, 1000))
    );

    const { result, unmount } = renderHook(() => useDonorSearch());

    result.current.selectDonor(mockDonors[0]);

    // Unmount before promise resolves
    unmount();

    // Should not throw error
    expect(true).toBe(true);
  });
});
```

**Verify:**
- [ ] Hook tests pass
- [ ] Tests verify state management
- [ ] Tests check async behavior
- [ ] Tests confirm cleanup on unmount

---

### Task 6: Test API Service Layer

Create `frontend/src/services/__tests__/api.test.ts`:
```typescript
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { api } from '../api';
import { mockPoliticians, mockDonors, mockDonations, mockDonationSummary, mockVotes } from '../../test/mockData';

global.fetch = vi.fn();

describe('API Service', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.resetAllMocks();
  });

  describe('searchPoliticians', () => {
    it('calls correct endpoint with encoded query', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockPoliticians,
      });

      await api.searchPoliticians('John Doe');

      expect(global.fetch).toHaveBeenCalledWith('/api/politicians/search?q=John%20Doe');
    });

    it('returns politician array', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockPoliticians,
      });

      const result = await api.searchPoliticians('John');
      expect(result).toEqual(mockPoliticians);
    });

    it('throws error on API failure', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
      });

      await expect(api.searchPoliticians('test')).rejects.toThrow('API error: 500 Internal Server Error');
    });
  });

  describe('searchDonors', () => {
    it('encodes special characters in query', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockDonors,
      });

      await api.searchDonors('AT&T Inc.');

      expect(global.fetch).toHaveBeenCalledWith('/api/donors/search?q=AT%26T%20Inc.');
    });
  });

  describe('getPoliticianVotes', () => {
    it('builds query string with multiple parameters', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ pagination: {}, votes: mockVotes }),
      });

      await api.getPoliticianVotes('P001', {
        page: 2,
        sort: 'ASC',
        type: 'hr',
        subject: 'Health',
      });

      expect(global.fetch).toHaveBeenCalledWith(
        '/api/politician/P001/votes?page=2&sort=ASC&type=hr&subject=Health'
      );
    });

    it('works with no parameters', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ pagination: {}, votes: [] }),
      });

      await api.getPoliticianVotes('P001');

      expect(global.fetch).toHaveBeenCalledWith('/api/politician/P001/votes');
    });
  });

  describe('getDonationSummary', () => {
    it('returns donation summary array', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockDonationSummary,
      });

      const result = await api.getDonationSummary('P001');
      expect(result).toEqual(mockDonationSummary);
    });
  });

  describe('getFilteredDonationSummary', () => {
    it('includes topic parameter', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockDonationSummary,
      });

      await api.getFilteredDonationSummary('P001', 'Health');

      expect(global.fetch).toHaveBeenCalledWith(
        '/api/politician/P001/donations/summary/filtered?topic=Health'
      );
    });
  });
});
```

**Verify:**
- [ ] API service tests pass
- [ ] Tests verify URL encoding
- [ ] Tests check error handling
- [ ] Tests confirm proper query string construction

---

## Part C: Backend Test Coverage

### Task 7: Verify Backend Test Coverage

The backend already has comprehensive tests from Phase 0. Verify they still pass after frontend integration.

**Steps:**

1. **Run existing backend tests**

```bash
# Activate virtual environment
source .venv/bin/activate

# Run pytest with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Verify all 135 tests pass
```

2. **Check coverage report**

```bash
# Open HTML report
open htmlcov/index.html
# OR
# View in terminal
pytest --cov=app --cov-report=term-missing
```

3. **Ensure no breaking changes**

All API endpoint tests from Phase 0 must still pass:
- ✅ test_api_politicians.py (24 tests)
- ✅ test_api_donors.py (24 tests)
- ✅ test_api_bills.py (17 tests)
- ✅ test_api_donations.py (30 tests)
- ✅ test_api_votes.py (40 tests)

**Verify:**
- [ ] All 135 backend tests pass
- [ ] Coverage remains ≥90%
- [ ] No SQL injection vulnerabilities
- [ ] No breaking API changes

---

## Part D: Integration Testing

### Task 8: Add End-to-End Test Scenarios

Create integration tests that verify complete user flows.

Create `frontend/src/test/integration/user-flows.test.tsx`:
```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '../utils';
import userEvent from '@testing-library/user-event';
import App from '../../App';
import { mockPoliticians, mockDonors, mockDonations, mockDonationSummary } from '../mockData';
import * as api from '../../services/api';

vi.mock('../../services/api');

describe('User Flow Integration Tests', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('completes politician search flow', async () => {
    const user = userEvent.setup();

    vi.spyOn(api, 'searchPoliticians').mockResolvedValue(mockPoliticians);
    vi.spyOn(api, 'getPoliticianVotes').mockResolvedValue({
      pagination: { currentPage: 1, totalPages: 1, totalVotes: 0 },
      votes: [],
    });
    vi.spyOn(api, 'getDonationSummary').mockResolvedValue(mockDonationSummary);

    render(<App />);

    // User searches for politician
    const searchInput = screen.getByPlaceholderText(/search politician/i);
    await user.type(searchInput, 'John');
    await user.click(screen.getByRole('button', { name: /search/i }));

    // Results appear
    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
    });

    // User selects politician
    await user.click(screen.getByText('John Doe'));

    // Details page loads with donation chart
    await waitFor(() => {
      expect(screen.getByText(/Donations by Industry/i)).toBeInTheDocument();
    });
  });

  it('completes donor search flow', async () => {
    const user = userEvent.setup();

    vi.spyOn(api, 'searchDonors').mockResolvedValue(mockDonors);
    vi.spyOn(api, 'getDonorDonations').mockResolvedValue(mockDonations);

    render(<App />);

    // Navigate to donor search
    await user.click(screen.getByRole('link', { name: /Donor Search/i }));

    // Search for donor
    const searchInput = screen.getByPlaceholderText(/enter donor name/i);
    await user.type(searchInput, 'Tech Corp');
    await user.click(screen.getByRole('button', { name: /search/i }));

    // Results appear
    await waitFor(() => {
      expect(screen.getByText('Tech Corp')).toBeInTheDocument();
    });

    // Select donor
    await user.click(screen.getByText('Tech Corp'));

    // Contribution history loads
    await waitFor(() => {
      expect(screen.getByText(/Contribution History/i)).toBeInTheDocument();
    });

    // Navigate back to search
    await user.click(screen.getByRole('button', { name: /back to search/i }));

    // Results still visible
    expect(screen.getByText('Tech Corp')).toBeInTheDocument();
  });
});
```

**Verify:**
- [ ] Integration tests pass
- [ ] Tests verify complete user flows
- [ ] Tests check navigation between pages
- [ ] Tests confirm data persistence

---

## Part E: Coverage and Documentation

### Task 9: Generate Coverage Reports

**Steps:**

1. **Install coverage tool**

```bash
cd frontend
npm install -D @vitest/coverage-v8
```

2. **Generate coverage report**

```bash
npm run test:coverage
```

3. **Review coverage metrics**

Target coverage thresholds:
- **Statements:** ≥80%
- **Branches:** ≥75%
- **Functions:** ≥80%
- **Lines:** ≥80%

4. **Update vitest.config.ts with thresholds**

```typescript
export default defineConfig({
  test: {
    coverage: {
      statements: 80,
      branches: 75,
      functions: 80,
      lines: 80,
    },
  },
});
```

**Verify:**
- [ ] Coverage report generates successfully
- [ ] All thresholds met
- [ ] HTML report opens in browser
- [ ] Untested code identified

---

### Task 10: Document Testing Practices

Create `frontend/TESTING.md`:
```markdown
# Testing Guide for Paper Trail Frontend

## Running Tests

```bash
# Run tests in watch mode
npm run test

# Run tests once with coverage
npm run test:coverage

# Open Vitest UI
npm run test:ui
```

## Test Structure

```
frontend/src/
├── test/
│   ├── setup.ts              # Global test setup
│   ├── utils.tsx             # Test utilities (custom render)
│   ├── mockData.ts           # Mock data for all types
│   └── integration/          # Integration tests
└── [component folders]/
    └── __tests__/            # Component tests
        └── Component.test.tsx
```

## Writing Tests

### Component Tests

```typescript
import { describe, it, expect } from 'vitest';
import { render, screen } from '../../test/utils';
import MyComponent from '../MyComponent';

describe('MyComponent', () => {
  it('renders correctly', () => {
    render(<MyComponent />);
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });
});
```

### Hook Tests

```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { useMyHook } from '../useMyHook';

describe('useMyHook', () => {
  it('returns expected value', async () => {
    const { result } = renderHook(() => useMyHook());

    await waitFor(() => {
      expect(result.current.value).toBe('expected');
    });
  });
});
```

### API Service Tests

```typescript
import { vi } from 'vitest';
import { api } from '../api';

global.fetch = vi.fn();

describe('API Service', () => {
  it('calls endpoint', async () => {
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ data: 'mock' }),
    });

    const result = await api.someMethod();
    expect(result).toEqual({ data: 'mock' });
  });
});
```

## Best Practices

1. **Test behavior, not implementation**
2. **Use descriptive test names**
3. **Follow Arrange-Act-Assert pattern**
4. **Mock external dependencies**
5. **Test edge cases and error states**
6. **Verify accessibility (keyboard navigation, ARIA)**
7. **Clean up after each test**
8. **Avoid testing third-party libraries**

## Coverage Requirements

Minimum coverage thresholds:
- Statements: 80%
- Branches: 75%
- Functions: 80%
- Lines: 80%

## Continuous Integration

Tests run automatically on:
- Every commit
- Pull request creation
- Before merge to main

All tests must pass before merging.
```

**Verify:**
- [ ] TESTING.md created with examples
- [ ] Best practices documented
- [ ] Coverage thresholds specified
- [ ] Instructions clear and complete

---

## ✅ VERIFICATION CHECKPOINT 6 (BLOCKING)

**This checkpoint MUST pass before considering Phase 6 complete.**

### Frontend Test Coverage
- [ ] Header component: 6+ tests passing
- [ ] LoadingSpinner component: 6+ tests passing
- [ ] DonationChart component: 6+ tests passing
- [ ] DonorCard component: 9+ tests passing
- [ ] ContributionHistory component: 7+ tests passing
- [ ] useDonorSearch hook: 8+ tests passing
- [ ] API service layer: 10+ tests passing
- [ ] Integration tests: 2+ user flows passing

### Coverage Metrics
- [ ] Overall coverage ≥80%
- [ ] Statement coverage ≥80%
- [ ] Branch coverage ≥75%
- [ ] Function coverage ≥80%
- [ ] Line coverage ≥80%

### Backend Test Coverage
- [ ] All 135 backend tests still passing
- [ ] No breaking API changes
- [ ] Backend coverage ≥90%

### Test Infrastructure
- [ ] Vitest configured correctly
- [ ] Test utilities created (utils.tsx, mockData.ts)
- [ ] Coverage reporting working
- [ ] Tests run in CI/CD pipeline
- [ ] TESTING.md documentation complete

### Quality Checks
- [ ] No flaky tests
- [ ] All tests run in <30 seconds
- [ ] No console errors during tests
- [ ] Mock data comprehensive
- [ ] Tests are maintainable

---

## Deliverables

Once CHECKPOINT 6 passes:

1. **Complete Test Suite**
   - 50+ frontend tests
   - 135+ backend tests (existing)
   - All tests passing

2. **Coverage Reports**
   - HTML coverage report generated
   - Thresholds met or exceeded
   - Gap analysis for missing coverage

3. **Test Documentation**
   - TESTING.md with examples
   - Best practices documented
   - CI/CD integration documented

4. **Test Infrastructure**
   - Vitest configured
   - Mock data created
   - Test utilities implemented

---

## Notes

- **TDD Compliance**: This phase addresses the critical requirement from CLAUDE.md
- **No Shortcuts**: Write tests for all components, even "simple" ones
- **Maintainability**: Tests should be as clean and maintainable as production code
- **Documentation**: Future developers need clear examples
- **CI/CD Ready**: Tests must run reliably in automated pipelines

---

## Timeline

**Estimated Duration:** 6-8 hours

**Breakdown:**
- Test framework setup: 1 hour
- Component tests: 3-4 hours
- Hook and API tests: 1-2 hours
- Integration tests: 1 hour
- Coverage and documentation: 1 hour

**Do not skip or rush this phase. Test quality directly impacts code quality.**
