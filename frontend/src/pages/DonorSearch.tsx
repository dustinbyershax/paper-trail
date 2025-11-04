/**
 * Donor Search page
 * Allows users to search for donors and view their donation history
 */
import { useDonorSearch } from '../hooks/useDonorSearch';
import { DonorCard } from '../components/DonorCard';
import { DonorDetails } from '../components/DonorDetails';
import { ContributionHistory } from '../components/ContributionHistory';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';

export default function DonorSearch() {
  const {
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
  } = useDonorSearch();

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    await search();
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value);
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      search();
    }
  };

  // If a donor is selected, show the details view
  if (selectedDonor) {
    return (
      <div className="container mx-auto px-4 py-8">
        <DonorDetails
          donor={selectedDonor}
          onClose={clearSelection}
        />
        <ContributionHistory
          donations={donations}
          isLoading={isLoadingDonations}
          error={donationsError}
        />
      </div>
    );
  }

  // Otherwise, show the search interface
  return (
    <div className="container mx-auto px-4 py-8">
      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="text-2xl">Search for a Donor (PAC or Individual)</CardTitle>
          <p className="text-sm text-gray-600">
            Find donors and explore their contribution history to politicians
          </p>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSearch} className="flex gap-2">
            <Input
              type="text"
              placeholder="Enter donor name (minimum 3 characters, e.g., Boeing, AT&T)"
              value={query}
              onChange={handleInputChange}
              onKeyPress={handleKeyPress}
              className="flex-1"
            />
            <Button
              type="submit"
              disabled={isSearching || query.length < 3}
            >
              {isSearching ? 'Searching...' : 'Search'}
            </Button>
          </form>

          {query.length > 0 && query.length < 3 && (
            <p className="text-sm text-amber-600 mt-2">
              Please enter at least 3 characters to search
            </p>
          )}

          {searchError && (
            <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
              <p className="text-red-800 text-sm">{searchError}</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Search Results */}
      {isSearching ? (
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-8 text-gray-600">
              Searching for donors...
            </div>
          </CardContent>
        </Card>
      ) : donors.length > 0 ? (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold">
            Found {donors.length} donor{donors.length !== 1 ? 's' : ''}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {donors.map((donor) => (
              <DonorCard
                key={donor.donorid}
                donor={donor}
                onSelect={selectDonor}
              />
            ))}
          </div>
        </div>
      ) : query.length >= 3 && !isSearching && !searchError ? (
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-8 text-gray-600">
              No donors found matching "{query}"
            </div>
          </CardContent>
        </Card>
      ) : null}
    </div>
  );
}
