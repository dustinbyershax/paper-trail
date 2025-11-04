/**
 * Custom hook for managing politician vote data with pagination and filtering
 * Handles vote loading, pagination state, sorting, and bill type/subject filtering
 */
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
    // eslint-disable-next-line react-hooks/exhaustive-deps
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
