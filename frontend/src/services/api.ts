/**
 * API service layer for Paper Trail application
 * Provides typed functions for all Flask backend endpoints
 */

import { API_BASE_URL } from '../config/env';
import type {
  Politician,
  Donor,
  Donation,
  DonationSummary,
  VoteResponse,
  VoteParams
} from '../types/api';

async function fetchJSON<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${url}`, options);
  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }
  return response.json();
}

export const api = {
  /**
   * Search for politicians by name
   * @param query - Search query (minimum 2 characters)
   * @returns Array of matching politicians
   */
  searchPoliticians: async (query: string): Promise<Politician[]> => {
    return fetchJSON<Politician[]>(`/api/politicians/search?name=${encodeURIComponent(query)}`);
  },

  /**
   * Get a single politician by ID
   * @param politicianId - The politician's ID
   * @returns Politician data
   */
  getPolitician: async (politicianId: number): Promise<Politician> => {
    return fetchJSON<Politician>(`/api/politician/${politicianId}`);
  },

  /**
   * Search for donors by name
   * @param query - Search query (minimum 3 characters)
   * @returns Array of matching donors
   */
  searchDonors: async (query: string): Promise<Donor[]> => {
    return fetchJSON<Donor[]>(`/api/donors/search?name=${encodeURIComponent(query)}`);
  },

  /**
   * Get a single donor by ID
   * @param donorId - The donor's ID
   * @returns Donor data
   */
  getDonor: async (donorId: number): Promise<Donor> => {
    return fetchJSON<Donor>(`/api/donor/${donorId}`);
  },

  /**
   * Get all donations made by a specific donor
   * @param donorId - The donor's ID
   * @param options - Optional fetch options including signal for cancellation
   * @returns Array of donations with recipient politician information
   */
  getDonorDonations: async (donorId: number, options?: RequestInit): Promise<Donation[]> => {
    return fetchJSON<Donation[]>(`/api/donor/${donorId}/donations`, options);
  },

  /**
   * Get paginated voting history for a politician with optional filters
   * @param politicianId - The politician's ID
   * @param params - Optional pagination and filter parameters
   * @returns Paginated vote response with metadata
   */
  getPoliticianVotes: async (
    politicianId: number,
    params: VoteParams = {}
  ): Promise<VoteResponse> => {
    const searchParams = new URLSearchParams();
    if (params.page) searchParams.set('page', params.page.toString());
    if (params.sort) searchParams.set('sort', params.sort);

    // Handle array parameters for type and subject filters
    if (params.type) {
      const types = Array.isArray(params.type) ? params.type : [params.type];
      types.forEach(t => searchParams.append('type', t));
    }
    if (params.subject) {
      const subjects = Array.isArray(params.subject) ? params.subject : [params.subject];
      subjects.forEach(s => searchParams.append('subject', s));
    }

    const queryString = searchParams.toString();
    const url = `/api/politician/${politicianId}/votes${queryString ? `?${queryString}` : ''}`;
    return fetchJSON<VoteResponse>(url);
  },

  /**
   * Get donation summary grouped by industry for a politician
   * @param politicianId - The politician's ID
   * @returns Array of industry donation summaries sorted by total amount
   */
  getDonationSummary: async (politicianId: number): Promise<DonationSummary[]> => {
    return fetchJSON<DonationSummary[]>(`/api/politician/${politicianId}/donations/summary`);
  },

  /**
   * Get donation summary filtered by bill topic/subject
   * @param politicianId - The politician's ID
   * @param topic - The bill topic to filter by (e.g., "Health", "Finance")
   * @returns Array of industry donation summaries for topic-related industries
   */
  getFilteredDonationSummary: async (
    politicianId: number,
    topic: string
  ): Promise<DonationSummary[]> => {
    return fetchJSON<DonationSummary[]>(
      `/api/politician/${politicianId}/donations/summary/filtered?topic=${encodeURIComponent(topic)}`
    );
  },

  /**
   * Get all unique bill subjects from the database
   * @returns Array of bill subject strings sorted alphabetically
   */
  getBillSubjects: async (): Promise<string[]> => {
    return fetchJSON<string[]>('/api/bills/subjects');
  },
};
