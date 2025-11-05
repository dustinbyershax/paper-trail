/**
 * Politician Search page (main landing page)
 * Allows users to search for politicians and view their voting records and donation data
 * Supports comparison mode for side-by-side politician analysis
 */
import { useEffect, useState } from 'react';
import { usePoliticianSearch } from '../hooks/usePoliticianSearch';
import { PoliticianCard } from '../components/PoliticianCard';
import { PoliticianDetails } from '../components/PoliticianDetails';
import { PoliticianComparison } from '../components/PoliticianComparison';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Skeleton } from '../components/ui/skeleton';
import { Badge } from '../components/ui/badge';
import { Search, GitCompare, X } from 'lucide-react';
import { useRouteState } from '../utils/routing';
import { api } from '../services/api';
import type { Politician } from '../types/api';

export default function PoliticianSearch() {
  const {
    query,
    setQuery,
    politicians,
    selectedPolitician,
    comparisonPoliticians,
    isComparing,
    isLoading,
    error,
    search,
    selectPolitician,
    toggleComparison,
    clearSelection,
    clearComparison,
  } = usePoliticianSearch();

  const {
    entityId,
    searchQuery,
    comparisonIds,
    navigateToEntity,
    navigateToComparison,
    navigateToSearch,
    navigateBack,
  } = useRouteState();

  const [comparisonMode, setComparisonMode] = useState(false);

  // Local input state - this is the source of truth for the input field
  const [inputValue, setInputValue] = useState(query);

  // Hydrate state from URL on mount and URL changes
  useEffect(() => {
    const loadFromUrl = async () => {
      if (entityId) {
        // URL contains politician ID
        const politicianId = Number(entityId);

        // Check if already selected
        if (selectedPolitician?.politicianid === politicianId) {
          return;
        }

        // Try to find in search results first
        const politician = politicians.find((p) => p.politicianid === politicianId);
        if (politician) {
          selectPolitician(politician);
          return;
        }

        // Not in search results - fetch directly from API (cold start)
        try {
          const fetchedPolitician = await api.getPolitician(politicianId);
          selectPolitician(fetchedPolitician);
        } catch (err) {
          console.error('Failed to load politician from URL:', err);
        }
      } else if (comparisonIds.length >= 2) {
        // URL contains comparison IDs
        // Find politicians in current search results
        const foundPoliticians = comparisonIds
          .map((id) => politicians.find((p) => p.politicianid === id))
          .filter((p): p is Politician => p !== undefined);

        if (foundPoliticians.length >= 2) {
          clearSelection();
          foundPoliticians.forEach(toggleComparison);
        } else if (foundPoliticians.length === 0) {
          // Cold start - fetch politicians from API
          try {
            const fetchedPoliticians = await Promise.all(
              comparisonIds.map((id) => api.getPolitician(id))
            );
            clearSelection();
            fetchedPoliticians.forEach(toggleComparison);
          } catch (err) {
            console.error('Failed to load comparison politicians from URL:', err);
          }
        }
      } else if (searchQuery && searchQuery !== query) {
        // Set search query from URL
        setInputValue(searchQuery);
        setQuery(searchQuery);
        // Trigger search if query is valid
        if (searchQuery.length >= 2) {
          search(searchQuery);
        }
      }
    };

    loadFromUrl();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [entityId, comparisonIds, searchQuery, politicians, selectedPolitician, selectPolitician, clearSelection, toggleComparison]);

  // Sync URL when politician is selected
  useEffect(() => {
    if (selectedPolitician && !entityId) {
      navigateToEntity(selectedPolitician.politicianid, 'politician');
    }
  }, [selectedPolitician, entityId, navigateToEntity]);

  // Sync URL when comparison starts
  useEffect(() => {
    if (isComparing && comparisonIds.length === 0) {
      const ids = comparisonPoliticians.map((p) => p.politicianid);
      navigateToComparison(ids);
    }
  }, [isComparing, comparisonIds.length, comparisonPoliticians, navigateToComparison]);

  // Listen for politician selection from command palette
  useEffect(() => {
    const handleCommandSelection = (event: Event) => {
      const customEvent = event as CustomEvent<Politician>;
      selectPolitician(customEvent.detail);
    };

    window.addEventListener('selectPoliticianFromCommand', handleCommandSelection);
    return () => window.removeEventListener('selectPoliticianFromCommand', handleCommandSelection);
  }, [selectPolitician]);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    // Update hook state and trigger search
    setQuery(inputValue);
    if (inputValue.length >= 2) {
      await search(inputValue);
      navigateToSearch('politician', inputValue);
    } else if (inputValue.length === 0) {
      navigateToSearch('politician');
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

  const handleToggleComparisonMode = () => {
    setComparisonMode(!comparisonMode);
    if (!comparisonMode) {
      clearComparison();
    }
  };

  const handleExitComparison = () => {
    clearComparison();
    setComparisonMode(false);
    navigateBack();
  };

  const handleClearSelection = () => {
    clearSelection();
    navigateBack();
  };

  // If comparing two politicians, show the comparison view
  if (isComparing) {
    return (
      <div className="container mx-auto px-4 py-8">
        <PoliticianComparison
          politicians={comparisonPoliticians as [Politician, Politician]}
          onClose={handleExitComparison}
        />
      </div>
    );
  }

  // If a politician is selected, show the details view
  if (selectedPolitician) {
    return (
      <div className="container mx-auto px-4 py-8">
        <PoliticianDetails
          politician={selectedPolitician}
          onClose={handleClearSelection}
        />
      </div>
    );
  }

  // Otherwise, show the search interface
  return (
    <div className="container mx-auto px-4 py-8">
      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="text-2xl">Search Politicians</CardTitle>
          <p className="text-sm text-muted-foreground">
            Find politicians and explore their voting records and campaign donations
          </p>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSearch} className="flex gap-2">
            <Input
              type="text"
              placeholder="Enter politician name (minimum 2 characters)"
              value={inputValue}
              onChange={handleInputChange}
              onKeyPress={handleKeyPress}
              className="flex-1"
            />
            <Button
              type="submit"
              disabled={isLoading || inputValue.length < 2}
            >
              {isLoading ? 'Searching...' : 'Search'}
            </Button>
          </form>

          {inputValue.length > 0 && inputValue.length < 2 && (
            <p className="text-sm text-amber-600 mt-2">
              Please enter at least 2 characters to search
            </p>
          )}

          {error && (
            <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
              <p className="text-red-800 text-sm">{error}</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Search Results */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, idx) => (
            <Card key={idx}>
              <CardContent className="pt-6">
                <div className="flex flex-col gap-2">
                  <div className="flex items-start justify-between">
                    <Skeleton className="h-6 w-40" />
                    <Skeleton className="h-5 w-16" />
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <Skeleton className="h-6 w-24" />
                    <Skeleton className="h-6 w-12" />
                    <Skeleton className="h-6 w-20" />
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : politicians.length > 0 ? (
        <div className="space-y-4">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <h2 className="text-xl font-semibold">
              Found {politicians.length} politician{politicians.length !== 1 ? 's' : ''}
            </h2>
            <div className="flex items-center gap-2">
              {comparisonMode && comparisonPoliticians.length > 0 && (
                <Badge variant="secondary" className="px-3 py-1">
                  {comparisonPoliticians.length} selected
                </Badge>
              )}
              <Button
                variant={comparisonMode ? 'default' : 'outline'}
                size="sm"
                onClick={handleToggleComparisonMode}
              >
                {comparisonMode ? (
                  <>
                    <X className="size-4" />
                    Exit Compare Mode
                  </>
                ) : (
                  <>
                    <GitCompare className="size-4" />
                    Compare Mode
                  </>
                )}
              </Button>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {politicians.map((politician) => (
              <PoliticianCard
                key={politician.politicianid}
                politician={politician}
                onSelect={selectPolitician}
                onToggleComparison={toggleComparison}
                isSelectedForComparison={comparisonPoliticians.some(
                  (p) => p.politicianid === politician.politicianid
                )}
                comparisonMode={comparisonMode}
              />
            ))}
          </div>
          {comparisonMode && comparisonPoliticians.length === 1 && (
            <Card className="bg-blue-50 dark:bg-blue-950 border-blue-200 dark:border-blue-800">
              <CardContent className="pt-6">
                <p className="text-sm text-blue-800 dark:text-blue-200 text-center">
                  Select one more politician to compare
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      ) : query.length >= 2 && !isLoading && !error ? (
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-12 space-y-4">
              <Search className="h-16 w-16 mx-auto text-muted-foreground/50" />
              <div>
                <h3 className="font-semibold text-lg mb-2">No Results Found</h3>
                <p className="text-muted-foreground text-sm max-w-md mx-auto mb-3">
                  No politicians found matching <span className="font-semibold">"{query}"</span>
                </p>
                <p className="text-muted-foreground text-xs max-w-md mx-auto">
                  Try searching with:
                </p>
                <ul className="text-muted-foreground text-xs text-left inline-block mt-2 space-y-1">
                  <li>• Full or partial first/last name</li>
                  <li>• Different spelling variations</li>
                  <li>• Only the last name</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>
      ) : null}
    </div>
  );
}
