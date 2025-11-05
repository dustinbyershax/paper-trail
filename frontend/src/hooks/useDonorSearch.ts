/**
 * Custom hook for donor search functionality
 * Manages donor search state, selected donor, and donation history
 * Includes request cancellation to prevent memory leaks from unmounted components
 *
 * @returns Object containing search state, functions, and data
 * @property query - Current search query string
 * @property setQuery - Function to update search query
 * @property donors - Array of donor search results
 * @property selectedDonor - Currently selected donor (null if none)
 * @property donations - Array of donations for selected donor
 * @property isSearching - Loading state for donor search
 * @property isLoadingDonations - Loading state for donation fetch
 * @property searchError - Error message from donor search (null if no error)
 * @property donationsError - Error message from donation fetch (null if no error)
 * @property search - Function to trigger donor search
 * @property selectDonor - Function to select a donor and load their donations
 * @property clearSelection - Function to deselect current donor
 */
import { useState, useRef, useEffect, useCallback } from 'react';
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
  search: (searchQuery?: string) => Promise<void>;
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

  const donationAbortController = useRef<AbortController | null>(null);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      donationAbortController.current?.abort();
    };
  }, []);

  const search = useCallback(async (searchQuery?: string) => {
    const queryToSearch = searchQuery ?? query;
    if (queryToSearch.length < 3) {
      setDonors([]);
      return;
    }

    setIsSearching(true);
    setSearchError(null);

    try {
      const results = await api.searchDonors(queryToSearch);
      setDonors(results);
    } catch (err) {
      setSearchError(err instanceof Error ? err.message : 'Search failed');
      setDonors([]);
    } finally {
      setIsSearching(false);
    }
  }, [query]);

  const selectDonor = useCallback(async (donor: Donor) => {
    // Cancel previous request if still pending
    donationAbortController.current?.abort();

    const abortController = new AbortController();
    donationAbortController.current = abortController;

    setSelectedDonor(donor);
    setIsLoadingDonations(true);
    setDonationsError(null);

    try {
      const donationData = await api.getDonorDonations(donor.donorid, {
        signal: abortController.signal
      });

      // Only update state if request wasn't aborted
      if (!abortController.signal.aborted) {
        setDonations(donationData);
      }
    } catch (err) {
      // Ignore AbortError - it's expected when user navigates away quickly
      if (err instanceof Error && err.name === 'AbortError') {
        return;
      }

      if (!abortController.signal.aborted) {
        setDonationsError(err instanceof Error ? err.message : 'Failed to load donations');
        setDonations([]);
      }
    } finally {
      if (!abortController.signal.aborted) {
        setIsLoadingDonations(false);
      }
    }
  }, []);

  const clearSelection = useCallback(() => {
    // Cancel pending donation request
    donationAbortController.current?.abort();
    donationAbortController.current = null;

    setSelectedDonor(null);
    setDonations([]);
  }, []);

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
