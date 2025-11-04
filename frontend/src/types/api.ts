/**
 * TypeScript type definitions for Paper Trail API responses
 * These types match the exact structure returned by Flask endpoints
 */

export interface Politician {
  politicianid: string;
  firstname: string;
  lastname: string;
  party: string;
  state: string;
  role: string | null;
  isactive: boolean;
}

export interface Donor {
  donorid: number;
  name: string;
  donortype: string;
  employer: string | null;
  state: string | null;
}

export interface Donation {
  amount: number;
  date: string;
  firstname: string;
  lastname: string;
  party: string;
  state: string;
}

export interface DonationSummary {
  industry: string;
  totalamount: number;
}

export interface Vote {
  VoteID: number;
  Vote: 'Yea' | 'Nay' | 'Present' | 'Not Voting';
  BillNumber: string;
  Title: string;
  DateIntroduced: string;
  subjects: string[];
}

export interface VotePagination {
  currentPage: number;
  totalPages: number;
  totalVotes: number;
}

export interface VoteResponse {
  pagination: VotePagination;
  votes: Vote[];
}

export interface VoteParams {
  page?: number;
  sort?: 'ASC' | 'DESC';
  type?: string | string[];
  subject?: string | string[];
}
