/**
 * Contribution history component
 * Displays a list of donations made by a donor with formatted amounts and dates
 */
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import type { Donation } from '../types/api';

interface ContributionHistoryProps {
  donations: Donation[];
  isLoading: boolean;
  error: string | null;
}

function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

function formatDate(dateString: string): string {
  try {
    const date = new Date(dateString);
    if (!isNaN(date.getTime())) {
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        timeZone: 'UTC',
      });
    }
  } catch (e) {
    console.warn('Could not parse date:', dateString);
  }
  return 'N/A';
}

export function ContributionHistory({ donations, isLoading, error }: ContributionHistoryProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-center">
          Contribution History (&gt; $2000)
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
          <div className="text-center py-8 text-gray-600">
            <p>No contribution history found &gt; $2000 for politicians in our database.</p>
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
