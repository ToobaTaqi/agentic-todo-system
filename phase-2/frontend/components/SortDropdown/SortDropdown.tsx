'use client';

import React from 'react';

interface SortDropdownProps {
  sortBy: string;
  sortOrder: 'asc' | 'desc';
  onSortChange: (sortBy: string, sortOrder: 'asc' | 'desc') => void;
}

export const SortDropdown: React.FC<SortDropdownProps> = ({
  sortBy,
  sortOrder,
  onSortChange
}) => {
  const handleSortByChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onSortChange(e.target.value, sortOrder);
  };

  const handleSortOrderChange = () => {
    const newOrder = sortOrder === 'asc' ? 'desc' : 'asc';
    onSortChange(sortBy, newOrder);
  };

  return (
    <div className="flex items-center space-x-2">
      <label className="text-sm font-medium text-text-secondary">Sort by:</label>
      <select
        value={sortBy}
        onChange={handleSortByChange}
        className="px-3 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
      >
        <option value="due_date">Due Date</option>
        <option value="priority">Priority</option>
        <option value="title">Alphabetical</option>
        <option value="created_at">Created Date</option>
      </select>

      <button
        type="button"
        onClick={handleSortOrderChange}
        className="px-3 py-2 border border-border rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500"
      >
        {sortOrder === 'asc' ? '↑' : '↓'}
      </button>
    </div>
  );
};