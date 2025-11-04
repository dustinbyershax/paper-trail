/**
 * Custom hook for managing politician search state and operations
 * Handles search queries, results, selection, and loading/error states
 */
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
