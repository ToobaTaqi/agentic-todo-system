import React from 'react';

interface TagChipProps {
  tag: string;
  onRemove?: (tag: string) => void;
}

export const TagChip: React.FC<TagChipProps> = ({ tag, onRemove }) => {
  return (
    <div className="inline-flex items-center bg-indigo-100 text-indigo-800 rounded-full px-3 py-1 text-sm font-medium">
      {tag}
      {onRemove && (
        <button
          type="button"
          onClick={() => onRemove(tag)}
          className="ml-2 text-indigo-600 hover:text-indigo-800 focus:outline-none"
        >
          ×
        </button>
      )}
    </div>
  );
};