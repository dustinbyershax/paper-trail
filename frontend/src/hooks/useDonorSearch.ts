/**
 * Custom hook for donor search functionality
 * Manages donor search state, selected donor, and donation history
 */
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
