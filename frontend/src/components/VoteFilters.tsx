/**
 * Vote filtering UI component
 * Provides bill type, subject, and sort order filtering controls
 */
import { useEffect, useState } from 'react';
import { Button } from './ui/button';
import { Checkbox } from './ui/checkbox';
import { Label } from './ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { api } from '../services/api';

interface VoteFiltersProps {
  billType: string;
  setBillType: (type: string) => void;
  subject: string;
  setSubject: (subject: string) => void;
  sortOrder: 'ASC' | 'DESC';
  setSortOrder: (order: 'ASC' | 'DESC') => void;
}

export function VoteFilters({
  billType,
  setBillType,
  subject,
  setSubject,
  sortOrder,
  setSortOrder,
}: VoteFiltersProps) {
  const [availableSubjects, setAvailableSubjects] = useState<string[]>([]);
  const [isLoadingSubjects, setIsLoadingSubjects] = useState(false);

  useEffect(() => {
    const loadSubjects = async () => {
      setIsLoadingSubjects(true);
      try {
        const subjects = await api.getBillSubjects();
        setAvailableSubjects(subjects);
      } catch (err) {
        console.error('Failed to load bill subjects:', err);
      } finally {
        setIsLoadingSubjects(false);
      }
    };

    loadSubjects();
  }, []);

  const billTypes = [
    { id: 'hr', label: 'House (HR)' },
    { id: 's', label: 'Senate (S)' },
  ];

  const handleBillTypeChange = (type: string, checked: boolean) => {
    const currentTypes = billType.split(',').filter(Boolean);

    if (checked) {
      // Add the type
      const newTypes = [...currentTypes, type];
      setBillType(newTypes.join(','));
    } else {
      // Remove the type
      const newTypes = currentTypes.filter(t => t !== type);
      setBillType(newTypes.join(','));
    }
  };

  const isBillTypeChecked = (type: string): boolean => {
    return billType.split(',').includes(type);
  };

  const clearFilters = () => {
    setBillType('');
    setSubject('');
    setSortOrder('DESC');
  };

  return (
    <div className="space-y-4 p-4 bg-gray-50 rounded-lg border">
      <h3 className="font-semibold text-sm text-gray-700">Filter Votes</h3>

      {/* Bill Type Filter */}
      <div className="space-y-2">
        <Label className="text-sm font-medium">Bill Type</Label>
        <div className="flex gap-4">
          {billTypes.map((type) => (
            <div key={type.id} className="flex items-center gap-2">
              <Checkbox
                id={`bill-type-${type.id}`}
                checked={isBillTypeChecked(type.id)}
                onCheckedChange={(checked) =>
                  handleBillTypeChange(type.id, checked === true)
                }
              />
              <Label
                htmlFor={`bill-type-${type.id}`}
                className="text-sm cursor-pointer"
              >
                {type.label}
              </Label>
            </div>
          ))}
        </div>
      </div>

      {/* Subject Filter */}
      <div className="space-y-2">
        <Label className="text-sm font-medium">Subject</Label>
        <Select
          value={subject || 'all'}
          onValueChange={(value) => setSubject(value === 'all' ? '' : value)}
          disabled={isLoadingSubjects}
        >
          <SelectTrigger className="w-full">
            <SelectValue placeholder="All subjects" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All subjects</SelectItem>
            {availableSubjects.map((subj) => (
              <SelectItem key={subj} value={subj}>
                {subj}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Sort Order */}
      <div className="space-y-2">
        <Label className="text-sm font-medium">Sort Order</Label>
        <div className="flex gap-2">
          <Button
            variant={sortOrder === 'DESC' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setSortOrder('DESC')}
          >
            Newest First
          </Button>
          <Button
            variant={sortOrder === 'ASC' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setSortOrder('ASC')}
          >
            Oldest First
          </Button>
        </div>
      </div>

      {/* Clear Filters Button */}
      <Button
        variant="ghost"
        size="sm"
        onClick={clearFilters}
        className="w-full"
      >
        Clear All Filters
      </Button>
    </div>
  );
}
