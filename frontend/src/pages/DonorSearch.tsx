/**
 * Donor Search page
 * Allows users to search for donors and view their donation history
 */
import { useEffect, useState } from 'react';
import { useDonorSearch } from '../hooks/useDonorSearch';
import { DonorCard } from '../components/DonorCard';
import { DonorDetails } from '../components/DonorDetails';
import { ContributionHistory } from '../components/ContributionHistory';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { useRouteState } from '../utils/routing';
import { api } from '../services/api';
import type { Donor } from '../types/api';

export default function DonorSearch() {
  const {
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
  } = useDonorSearch();

  const {
    entityId,
    searchQuery,
    navigateToEntity,
    navigateToSearch,
    navigateBack,
  } = useRouteState();

  // Local input state - this is the source of truth for the input field
  const [inputValue, setInputValue] = useState(query);

  // Hydrate state from URL on mount and URL changes
  useEffect(() => {
    const loadFromUrl = async () => {
      if (entityId) {
        // URL contains donor ID
        const donorId = Number(entityId);

        // Check if already selected
        if (selectedDonor?.donorid === donorId) {
          return;
        }

        // Try to find in search results first
        const donor = donors.find((d) => d.donorid === donorId);
        if (donor) {
          selectDonor(donor);
          return;
        }

        // Not in search results - fetch directly from API (cold start)
        try {
          const fetchedDonor = await api.getDonor(donorId);
          selectDonor(fetchedDonor);
        } catch (err) {
          console.error('Failed to load donor from URL:', err);
        }
      } else if (searchQuery && searchQuery !== query) {
        // Set search query from URL
        setInputValue(searchQuery);
        setQuery(searchQuery);
        // Trigger search if query is valid
        if (searchQuery.length >= 3) {
          search(searchQuery);
        }
      }
    };

    loadFromUrl();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [entityId, searchQuery, donors, selectedDonor, selectDonor]);

  // Sync URL when donor is selected
  useEffect(() => {
    if (selectedDonor && !entityId) {
      navigateToEntity(selectedDonor.donorid, 'donor');
    }
  }, [selectedDonor, entityId, navigateToEntity]);

  // Listen for donor selection from command palette
  useEffect(() => {
    const handleCommandSelection = (event: Event) => {
      const customEvent = event as CustomEvent<Donor>;
      selectDonor(customEvent.detail);
    };

    window.addEventListener('selectDonorFromCommand', handleCommandSelection);
    return () => window.removeEventListener('selectDonorFromCommand', handleCommandSelection);
  }, [selectDonor]);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    // Update hook state and trigger search
    setQuery(inputValue);
    if (inputValue.length >= 3) {
      await search(inputValue);
      navigateToSearch('donor', inputValue);
    } else if (inputValue.length === 0) {
      navigateToSearch('donor');
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    // Only update local state - search happens on button click or Enter
    setInputValue(e.target.value);
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      // Trigger the same logic as clicking Search button
      handleSearch(e as any);
    }
  };

  const handleClearSelection = () => {
    clearSelection();
    navigateBack();
  };

  // If a donor is selected, show the details view
  if (selectedDonor) {
    return (
      <div className="container mx-auto px-4 py-8">
        <DonorDetails
          donor={selectedDonor}
          onClose={handleClearSelection}
        />
        <ContributionHistory
          donations={donations}
          isLoading={isLoadingDonations}
          error={donationsError}
        />
      </div>
    );
  }

  // Otherwise, show the search interface
  return (
    <div className="container mx-auto px-4 py-8">
      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="text-2xl">Search for a Donor (PAC or Individual)</CardTitle>
          <p className="text-sm text-muted-foreground">
            Find donors and explore their contribution history to politicians
          </p>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSearch} className="flex gap-2">
            <Input
              type="text"
              placeholder="Enter donor name (minimum 3 characters, e.g., Boeing, AT&T)"
              value={inputValue}
              onChange={handleInputChange}
              onKeyPress={handleKeyPress}
              className="flex-1"
            />
            <Button
              type="submit"
              disabled={isSearching || inputValue.length < 3}
            >
              {isSearching ? 'Searching...' : 'Search'}
            </Button>
          </form>

          {inputValue.length > 0 && inputValue.length < 3 && (
            <p className="text-sm text-amber-600 mt-2">
              Please enter at least 3 characters to search
            </p>
          )}

          {searchError && (
            <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
              <p className="text-red-800 text-sm">{searchError}</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Search Results */}
      {isSearching ? (
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-8 text-muted-foreground">
              Searching for donors...
            </div>
          </CardContent>
        </Card>
      ) : donors.length > 0 ? (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold">
            Found {donors.length} donor{donors.length !== 1 ? 's' : ''}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {donors.map((donor) => (
              <DonorCard
                key={donor.donorid}
                donor={donor}
                onSelect={selectDonor}
              />
            ))}
          </div>
        </div>
      ) : query.length >= 3 && !isSearching && !searchError ? (
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-8 text-muted-foreground">
              No donors found matching "{query}"
            </div>
          </CardContent>
        </Card>
      ) : null}
    </div>
  );
}
