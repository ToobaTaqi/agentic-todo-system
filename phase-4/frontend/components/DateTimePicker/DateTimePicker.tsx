'use client';

import React, { useState, useEffect } from 'react';

interface DateTimePickerProps {
  value: Date | null;
  onChange: (date: Date | null) => void;
}

export const DateTimePicker: React.FC<DateTimePickerProps> = ({ value, onChange }) => {
  // Convert UTC value to local for display in datetime-local input
  const convertUtcToLocalString = (date: Date | null): string => {
    if (!date) return '';

    // Convert UTC date to local time string suitable for datetime-local input
    const localDate = new Date(date.getTime() - date.getTimezoneOffset() * 60000);
    return localDate.toISOString().slice(0, 16);
  };

  // Convert local datetime string back to UTC Date
  const convertLocalStringToUtc = (localDateTimeStr: string): Date | null => {
    if (!localDateTimeStr) return null;

    // Parse the local datetime string and convert back to UTC
    const localDate = new Date(localDateTimeStr);
    const utcDate = new Date(localDate.getTime() + localDate.getTimezoneOffset() * 60000);
    return utcDate;
  };

  const [dateTimeLocal, setDateTimeLocal] = useState<string>(() => convertUtcToLocalString(value));

  useEffect(() => {
    // Update local datetime when value prop changes
    setDateTimeLocal(convertUtcToLocalString(value));
  }, [value]);

  const handleDateTimeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const localDateTimeStr = e.target.value;
    setDateTimeLocal(localDateTimeStr);

    if (localDateTimeStr) {
      const utcDate = convertLocalStringToUtc(localDateTimeStr);
      onChange(utcDate);
    } else {
      onChange(null);
    }
  };

  const handleClear = () => {
    setDateTimeLocal('');
    onChange(null);
  };

  return (
    <div className="relative">
      <div className="flex items-center space-x-2">
        <div className="relative">
          <input
            type="datetime-local"
            value={dateTimeLocal}
            onChange={handleDateTimeChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
      </div>

      {dateTimeLocal && (
        <button
          type="button"
          onClick={handleClear}
          className="mt-2 text-sm text-red-600 hover:text-red-800"
        >
          Clear
        </button>
      )}
    </div>
  );
};