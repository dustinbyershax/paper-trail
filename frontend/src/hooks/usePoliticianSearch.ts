/**
 * Custom hook for managing politician search state and operations
 * Handles search queries, results, selection, and loading/error states
 */
import { useState, useCallback } from 'react';
import { api } from '../services/api';
import type { Politician } from '../types/api';

interface UsePoliticianSearchResult {
  query: string;
  setQuery: (query: string) => void;
  politicians: Politician[];
  selectedPolitician: Politician | null;
  comparisonPoliticians: Politician[];
  isComparing: boolean;
  isLoading: boolean;
  error: string | null;
  search: (searchQuery?: string) => Promise<void>;
  selectPolitician: (politician: Politician) => void;
  toggleComparison: (politician: Politician) => void;
  clearSelection: () => void;
  clearComparison: () => void;
}

export function usePoliticianSearch(): UsePoliticianSearchResult {
  const [query, setQuery] = useState('');
  const [politicians, setPoliticians] = useState<Politician[]>([]);
  const [selectedPolitician, setSelectedPolitician] = useState<Politician | null>(null);
  const [comparisonPoliticians, setComparisonPoliticians] = useState<Politician[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const search = useCallback(async (searchQuery?: string) => {
    const queryToSearch = searchQuery ?? query;
    if (queryToSearch.length < 2) {
      setPoliticians([]);
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const results = await api.searchPoliticians(queryToSearch);
      setPoliticians(results);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Search failed');
      setPoliticians([]);
    } finally {
      setIsLoading(false);
    }
  }, [query]);

  const selectPolitician = useCallback((politician: Politician) => {
    setSelectedPolitician(politician);
    setComparisonPoliticians([]);
  }, []);

  const toggleComparison = useCallback((politician: Politician) => {
    setSelectedPolitician(null);
    setComparisonPoliticians((prev) => {
      const isSelected = prev.some((p) => p.politicianid === politician.politicianid);
      if (isSelected) {
        return prev.filter((p) => p.politicianid !== politician.politicianid);
      }
      if (prev.length >= 2) {
        return [prev[1], politician];
      }
      return [...prev, politician];
    });
  }, []);

  const clearSelection = useCallback(() => {
    setSelectedPolitician(null);
  }, []);

  const clearComparison = useCallback(() => {
    setComparisonPoliticians([]);
  }, []);

  const isComparing = comparisonPoliticians.length === 2;

  return {
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
  };
}
