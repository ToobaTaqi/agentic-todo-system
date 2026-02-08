'use client';

import React from 'react';

interface LabelSelectorProps {
  selectedLabel: string;
  onSelect: (label: string) => void;
}

export const LabelSelector: React.FC<LabelSelectorProps> = ({ selectedLabel, onSelect }) => {
  const labels = [
    { id: '', name: 'None', color: 'bg-gray-200' },
    { id: 'work', name: 'Work', color: 'bg-blue-200' },
    { id: 'home', name: 'Home', color: 'bg-green-200' },
  ];

  return (
    <div className="flex space-x-2">
      {labels.map((label) => (
        <button
          key={label.id}
          type="button"
          onClick={() => onSelect(label.id)}
          className={`px-3 py-1.5 rounded-full text-sm font-medium border ${
            selectedLabel === label.id
              ? `${label.color} border-gray-400 text-gray-800`
              : 'bg-white border-gray-300 text-gray-600 hover:bg-gray-100'
          }`}
        >
          {label.name}
        </button>
      ))}
    </div>
  );
};