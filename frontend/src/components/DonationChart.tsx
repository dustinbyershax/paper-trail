/**
 * Donation chart component
 * Displays donation breakdown by industry using Chart.js
 * Supports optional topic filtering for industry-specific analysis
 */
import { useState, useEffect } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, type TooltipItem } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';
import { api } from '../services/api';
import type { DonationSummary } from '../types/api';
import LoadingSpinner from './LoadingSpinner';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';

// CRITICAL: Register Chart.js components before use
ChartJS.register(ArcElement, Tooltip, Legend);

interface DonationChartProps {
  politicianId: string;
  selectedTopic?: string;
  onTopicChange?: (topic: string) => void;
}

const COLORS = [
  '#FF6384', // Pink
  '#36A2EB', // Blue
  '#FFCE56', // Yellow
  '#4BC0C0', // Teal
  '#9966FF', // Purple
  '#FF9F40', // Orange
  '#E91E63', // Magenta
  '#4CAF50', // Green
  '#795548', // Brown
  '#607D8B', // Blue Grey
];

const TOPICS = [
  'Health',
  'Finance',
  'Technology',
  'Defense',
  'Energy',
  'Environment',
  'Education',
  'Agriculture',
  'Transportation',
];

export default function DonationChart({
  politicianId,
  selectedTopic,
  onTopicChange,
}: DonationChartProps) {
  const [donations, setDonations] = useState<DonationSummary[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    const loadDonations = async () => {
      if (!isMounted) return;

      setIsLoading(true);
      setError(null);

      try {
        const data = selectedTopic
          ? await api.getFilteredDonationSummary(politicianId, selectedTopic)
          : await api.getDonationSummary(politicianId);

        if (isMounted) {
          setDonations(data);
        }
      } catch (err) {
        if (isMounted) {
          setError(err instanceof Error ? err.message : 'Failed to load donations');
          setDonations([]);
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    loadDonations();

    return () => {
      isMounted = false;
    };
  }, [politicianId, selectedTopic]);

  if (isLoading) {
    return (
      <Card>
        <CardContent className="pt-6">
          <LoadingSpinner message="Loading donation data..." />
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardContent className="pt-6">
          <div className="text-red-600 text-center py-8">
            Error: {error}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (donations.length === 0) {
    return (
      <Card>
        <CardContent className="pt-6">
          <div className="text-gray-600 text-center py-8">
            No donation data available
          </div>
        </CardContent>
      </Card>
    );
  }

  const chartData = {
    labels: donations.map((d) => d.industry || 'Unknown'),
    datasets: [
      {
        data: donations.map((d) => d.totalamount),
        backgroundColor: COLORS,
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'bottom' as const,
      },
      tooltip: {
        callbacks: {
          label: (context: TooltipItem<'doughnut'>) => {
            const label = context.label || '';
            const value = context.parsed || 0;
            const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0);
            const percentage = ((value / total) * 100).toFixed(1);
            return `${label}: $${value.toLocaleString()} (${percentage}%)`;
          },
        },
      },
    },
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-xl">Donations by Industry</CardTitle>
      </CardHeader>
      <CardContent>
        {onTopicChange && (
          <div className="mb-6">
            <label htmlFor="topic-filter" className="block mb-2 text-sm font-medium">
              Filter by Topic:
            </label>
            <Select value={selectedTopic || ''} onValueChange={onTopicChange}>
              <SelectTrigger id="topic-filter" className="w-full md:w-64" aria-label="Filter donations by topic">
                <SelectValue placeholder="All Industries" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">All Industries</SelectItem>
                {TOPICS.map((topic) => (
                  <SelectItem key={topic} value={topic}>
                    {topic}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        )}

        <div className="max-w-md mx-auto mb-6" role="img" aria-label="Doughnut chart showing donation breakdown by industry">
          <Doughnut data={chartData} options={chartOptions} />
        </div>

        <div className="mt-6">
          <h4 className="font-semibold mb-3 text-sm">Total by Industry:</h4>
          <div className="space-y-2">
            {donations.map((d, index) => (
              <div key={index} className="flex justify-between items-center text-sm">
                <span className="flex items-center gap-2">
                  <span
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: COLORS[index % COLORS.length] }}
                  ></span>
                  {d.industry || 'Unknown'}
                </span>
                <span className="font-medium">
                  ${d.totalamount.toLocaleString()}
                </span>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
