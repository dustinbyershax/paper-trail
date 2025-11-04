/**
 * Donor card component for displaying a donor in search results
 * Shows name, type, employer (if available), and state (if available) with clickable interaction
 */
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import type { Donor } from '../types/api';

interface DonorCardProps {
  donor: Donor;
  onSelect: (donor: Donor) => void;
}

export function DonorCard({ donor, onSelect }: DonorCardProps) {
  return (
    <Card
      className="cursor-pointer transition-all hover:shadow-md hover:border-gray-400"
      onClick={() => onSelect(donor)}
    >
      <CardContent className="pt-6">
        <div className="flex flex-col gap-2">
          <h3 className="text-lg font-semibold text-red-600">
            {donor.name}
          </h3>

          <div className="flex flex-col gap-1">
            <p className="text-sm text-gray-600">
              {donor.donortype}
              {donor.employer && ` - ${donor.employer}`}
            </p>
            {donor.state && (
              <Badge variant="outline" className="w-fit">
                {donor.state}
              </Badge>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
