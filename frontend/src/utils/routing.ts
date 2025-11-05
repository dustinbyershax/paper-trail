/**
 * Type-safe routing utilities for Paper Trail application.
 * Provides URL building and parsing functions for politician and donor routes.
 */

import { useNavigate, useParams, useSearchParams } from 'react-router-dom';

/**
 * Entity types supported by the routing system
 */
export type EntityType = 'politician' | 'donor';

/**
 * Parse comparison IDs from query parameter.
 * Returns array of politician IDs as strings (matches Politician.politicianid type).
 */
export function parseComparisonIds(idsParam: string | null): string[] {
  if (!idsParam || idsParam.trim() === '') return [];
  return idsParam
    .split(',')
    .map((id) => id.trim())
    .filter((id) => id.length > 0);
}

/**
 * Build comparison URL from politician IDs.
 * Politicians use string IDs (e.g., "412", "P000123").
 */
export function buildComparisonUrl(politicianIds: string[]): string {
  const ids = politicianIds.join(',');
  return `/politician/compare?ids=${ids}`;
}

/**
 * Build politician detail URL.
 * Politicians use string IDs.
 */
export function buildPoliticianUrl(politicianId: string): string {
  return `/politician/${politicianId}`;
}

/**
 * Build donor detail URL.
 * Donors use numeric IDs.
 */
export function buildDonorUrl(donorId: number): string {
  return `/donor/${donorId}`;
}

/**
 * Build search URL with optional query parameter.
 * Empty or whitespace-only queries return the base path.
 */
export function buildSearchUrl(
  entityType: EntityType,
  searchQuery?: string
): string {
  const basePath = entityType === 'politician' ? '/politician' : '/donor';
  if (!searchQuery || searchQuery.trim() === '') return basePath;
  return `${basePath}?search=${encodeURIComponent(searchQuery)}`;
}

/**
 * Route state returned by useRouteState hook
 */
export interface RouteState {
  entityId?: string;
  searchQuery?: string;
  comparisonIds: string[];
  navigateToEntity: (id: string | number, entityType: EntityType) => void;
  navigateToComparison: (ids: string[]) => void;
  navigateToSearch: (entityType: EntityType, query?: string) => void;
  navigateBack: () => void;
}

/**
 * Custom hook for URL-based state management.
 * Provides typed access to route parameters and navigation helpers.
 */
export function useRouteState(): RouteState {
  const navigate = useNavigate();
  const params = useParams();
  const [searchParams] = useSearchParams();

  return {
    // Route parameters
    entityId: params.id,

    // Query parameters
    searchQuery: searchParams.get('search') || undefined,
    comparisonIds: parseComparisonIds(searchParams.get('ids')),

    // Navigation helpers with minimal history (replace: true)
    navigateToEntity: (id: string | number, entityType: EntityType) => {
      const url =
        entityType === 'politician'
          ? buildPoliticianUrl(String(id))
          : buildDonorUrl(Number(id));
      navigate(url, { replace: true });
    },

    navigateToComparison: (ids: string[]) => {
      navigate(buildComparisonUrl(ids), { replace: true });
    },

    navigateToSearch: (entityType: EntityType, query?: string) => {
      navigate(buildSearchUrl(entityType, query));
    },

    navigateBack: () => {
      navigate(-1);
    },
  };
}
