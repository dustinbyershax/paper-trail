/**
 * Contribution history component
 * Displays a list of donations made by a donor with formatted amounts and dates
 *
 * @param donations - Array of donation records to display
 * @param isLoading - Loading state for async donation fetch
 * @param error - Error message if donation fetch failed
 * @param threshold - Minimum donation amount threshold (defaults to 2000)
 */
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { formatCurrency, formatDate } from '../utils/formatters';
import type { Donation } from '../types/api';

interface ContributionHistoryProps {
  donations: Donation[];
  isLoading: boolean;
  error: string | null;
  threshold?: number;
}

export function ContributionHistory({
  donations,
  isLoading,
  error,
  threshold = 2000
}: ContributionHistoryProps) {
  const thresholdDisplay = threshold ? `(> $${threshold.toLocaleString()})` : '';

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-center">
          Contribution History {thresholdDisplay}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="text-center py-8">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-red-600 border-r-transparent"></div>
            <p className="mt-2 text-gray-600">Loading contribution history...</p>
          </div>
        ) : error ? (
          <div className="text-center py-8 text-red-600">
            <p className="font-semibold">Could not load contribution history: {error}</p>
          </div>
        ) : donations.length === 0 ? (
          <div className="text-center py-8 text-gray-600 space-y-2">
            <p className="font-medium">
              No large contributions found {thresholdDisplay} to politicians in our database.
            </p>
            <p className="text-sm">
              This donor may have:
            </p>
            <ul className="text-sm text-left inline-block">
              <li>• Made smaller contributions (under ${threshold.toLocaleString()})</li>
              <li>• Not contributed to politicians we track</li>
              <li>• Contributed only to state/local politicians</li>
            </ul>
          </div>
        ) : (
          <div className="max-h-[60vh] overflow-y-auto space-y-3 pr-2">
            {donations.map((donation, index) => (
              <div
                key={index}
                className="border-t border-gray-200 pt-3 pb-1 first:border-t-0 first:pt-0"
              >
                <div className="flex justify-between items-center mb-1">
                  <p className="font-semibold text-gray-900">
                    {donation.firstname} {donation.lastname} ({donation.party}-{donation.state})
                  </p>
                  <p className="font-bold text-green-600">
                    {formatCurrency(donation.amount)}
                  </p>
                </div>
                <p className="text-sm text-gray-500">
                  Date: {formatDate(donation.date)}
                </p>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
