/**
 * Politician Search page (main landing page)
 * Allows users to search for politicians and view their voting records and donation data
 */
import { usePoliticianSearch } from '../hooks/usePoliticianSearch';
import { PoliticianCard } from '../components/PoliticianCard';
import { PoliticianDetails } from '../components/PoliticianDetails';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';

export default function PoliticianSearch() {
  const {
    query,
    setQuery,
    politicians,
    selectedPolitician,
    isLoading,
    error,
    search,
    selectPolitician,
    clearSelection,
  } = usePoliticianSearch();

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

  // If a politician is selected, show the details view
  if (selectedPolitician) {
    return (
      <div className="container mx-auto px-4 py-8">
        <PoliticianDetails
          politician={selectedPolitician}
          onClose={clearSelection}
        />
      </div>
    );
  }

  // Otherwise, show the search interface
  return (
    <div className="container mx-auto px-4 py-8">
      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="text-2xl">Search Politicians</CardTitle>
          <p className="text-sm text-gray-600">
            Find politicians and explore their voting records and campaign donations
          </p>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSearch} className="flex gap-2">
            <Input
              type="text"
              placeholder="Enter politician name (minimum 2 characters)"
              value={query}
              onChange={handleInputChange}
              onKeyPress={handleKeyPress}
              className="flex-1"
            />
            <Button
              type="submit"
              disabled={isLoading || query.length < 2}
            >
              {isLoading ? 'Searching...' : 'Search'}
            </Button>
          </form>

          {query.length > 0 && query.length < 2 && (
            <p className="text-sm text-amber-600 mt-2">
              Please enter at least 2 characters to search
            </p>
          )}

          {error && (
            <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
              <p className="text-red-800 text-sm">{error}</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Search Results */}
      {isLoading ? (
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-8 text-gray-600">
              Searching for politicians...
            </div>
          </CardContent>
        </Card>
      ) : politicians.length > 0 ? (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold">
            Found {politicians.length} politician{politicians.length !== 1 ? 's' : ''}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {politicians.map((politician) => (
              <PoliticianCard
                key={politician.politicianid}
                politician={politician}
                onSelect={selectPolitician}
              />
            ))}
          </div>
        </div>
      ) : query.length >= 2 && !isLoading && !error ? (
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-8 text-gray-600">
              No politicians found matching "{query}"
            </div>
          </CardContent>
        </Card>
      ) : null}
    </div>
  );
}
