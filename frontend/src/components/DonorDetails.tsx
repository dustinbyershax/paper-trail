/**
 * Donor details header component
 * Displays donor information with a close button to return to search
 *
 * @param donor - The donor object containing name, type, employer, and state
 * @param onClose - Callback fired when the back button is clicked to return to search
 */
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';
import type { Donor } from '../types/api';

interface DonorDetailsProps {
  donor: Donor;
  onClose: () => void;
}

export function DonorDetails({ donor, onClose }: DonorDetailsProps) {
  return (
    <Card className="mb-6">
      <CardContent className="pt-6">
        <Button
          variant="link"
          onClick={onClose}
          className="mb-4 p-0 text-red-600 hover:text-red-700"
        >
          ← Back to search results
        </Button>

        <div className="text-center border-b border-gray-200 pb-4">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            {donor.name}
          </h2>
          <p className="text-lg text-gray-600">
            {donor.donortype}
          </p>
          {donor.employer && (
            <p className="text-sm text-gray-500 mt-1">
              Employer: {donor.employer}
            </p>
          )}
          {donor.state && (
            <p className="text-sm text-gray-500">
              State: {donor.state}
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
