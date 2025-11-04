/**
 * Vote record component displaying paginated voting history with filtering
 * Shows votes in a table with pagination controls and subject filtering
 */
import { useEffect } from 'react';
import { useVotes } from '../hooks/useVotes';
import { VoteFilters } from './VoteFilters';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import type { Vote } from '../types/api';

interface VoteRecordProps {
  politicianId: string;
}

export function VoteRecord({ politicianId }: VoteRecordProps) {
  const {
    voteData,
    isLoading,
    error,
    currentPage,
    sortOrder,
    billType,
    subject,
    setCurrentPage,
    setSortOrder,
    setBillType,
    setSubject,
    loadVotes,
  } = useVotes();

  useEffect(() => {
    loadVotes(politicianId);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [politicianId]);

  const getVoteColor = (vote: Vote['Vote']): string => {
    switch (vote) {
      case 'Yea':
        return 'bg-green-100 text-green-800 border-green-300';
      case 'Nay':
        return 'bg-red-100 text-red-800 border-red-300';
      case 'Present':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'Not Voting':
        return 'bg-gray-100 text-gray-800 border-gray-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const handleSubjectClick = (clickedSubject: string) => {
    setSubject(clickedSubject);
    setCurrentPage(1);
  };

  if (error) {
    return (
      <Card>
        <CardContent className="pt-6">
          <div className="text-red-600">Error loading votes: {error}</div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Voting Record</CardTitle>
        </CardHeader>
        <CardContent>
          <VoteFilters
            billType={billType}
            setBillType={setBillType}
            subject={subject}
            setSubject={setSubject}
            sortOrder={sortOrder}
            setSortOrder={setSortOrder}
          />
        </CardContent>
      </Card>

      {isLoading ? (
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-8 text-gray-600">Loading votes...</div>
          </CardContent>
        </Card>
      ) : !voteData || voteData.votes.length === 0 ? (
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-8 text-gray-600">
              No votes found with the current filters.
            </div>
          </CardContent>
        </Card>
      ) : (
        <>
          <Card>
            <CardContent className="pt-6">
              <div className="rounded-md border">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead className="w-24">Vote</TableHead>
                      <TableHead className="w-32">Bill Number</TableHead>
                      <TableHead>Title</TableHead>
                      <TableHead className="w-32">Date Introduced</TableHead>
                      <TableHead className="w-64">Subjects</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {voteData.votes.map((vote) => (
                      <TableRow key={vote.VoteID}>
                        <TableCell>
                          <Badge className={getVoteColor(vote.Vote)}>
                            {vote.Vote}
                          </Badge>
                        </TableCell>
                        <TableCell className="font-mono text-sm">
                          {vote.BillNumber}
                        </TableCell>
                        <TableCell className="max-w-md">
                          <div className="line-clamp-2">{vote.Title}</div>
                        </TableCell>
                        <TableCell className="text-sm text-gray-600">
                          {formatDate(vote.DateIntroduced)}
                        </TableCell>
                        <TableCell>
                          <div className="flex flex-wrap gap-1">
                            {vote.subjects.slice(0, 3).map((subj, idx) => (
                              <Badge
                                key={idx}
                                variant="outline"
                                className="cursor-pointer hover:bg-gray-100"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  handleSubjectClick(subj);
                                }}
                              >
                                {subj}
                              </Badge>
                            ))}
                            {vote.subjects.length > 3 && (
                              <Badge variant="secondary" className="text-xs">
                                +{vote.subjects.length - 3}
                              </Badge>
                            )}
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>

          {/* Pagination */}
          {voteData.pagination.totalPages > 1 && (
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div className="text-sm text-gray-600">
                    Page {voteData.pagination.currentPage} of{' '}
                    {voteData.pagination.totalPages} ({voteData.pagination.totalVotes}{' '}
                    votes)
                  </div>
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setCurrentPage(currentPage - 1)}
                      disabled={currentPage === 1}
                    >
                      Previous
                    </Button>
                    {Array.from(
                      { length: Math.min(5, voteData.pagination.totalPages) },
                      (_, i) => {
                        let pageNum: number;
                        if (voteData.pagination.totalPages <= 5) {
                          pageNum = i + 1;
                        } else if (currentPage <= 3) {
                          pageNum = i + 1;
                        } else if (
                          currentPage >=
                          voteData.pagination.totalPages - 2
                        ) {
                          pageNum =
                            voteData.pagination.totalPages - 4 + i;
                        } else {
                          pageNum = currentPage - 2 + i;
                        }
                        return pageNum;
                      }
                    ).map((pageNum) => (
                      <Button
                        key={pageNum}
                        variant={pageNum === currentPage ? 'default' : 'outline'}
                        size="sm"
                        onClick={() => setCurrentPage(pageNum)}
                      >
                        {pageNum}
                      </Button>
                    ))}
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setCurrentPage(currentPage + 1)}
                      disabled={currentPage === voteData.pagination.totalPages}
                    >
                      Next
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </>
      )}
    </div>
  );
}
