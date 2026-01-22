// frontend/components/Notifications/NotificationProvider.tsx
'use client';

import React, { createContext, useContext, useEffect, ReactNode } from 'react';
import { useNotification } from '@/lib/hooks/useNotification';

interface NotificationContextType {
  isSupported: boolean;
  permission: NotificationPermission;
  requestPermission: () => Promise<NotificationPermission>;
  showNotification: (title: string, body: string, tag?: string) => void;
  scheduleNotificationsForTasks: (tasks: Array<{ id: string; title: string; due_date?: string | null }>) => Map<string, number>;
  hasPermission: boolean;
}

const NotificationContext = createContext<NotificationContextType | undefined>(undefined);

export const useNotificationContext = () => {
  const context = useContext(NotificationContext);
  if (context === undefined) {
    throw new Error('useNotificationContext must be used within a NotificationProvider');
  }
  return context;
};

interface NotificationProviderProps {
  children: ReactNode;
}

export const NotificationProvider: React.FC<NotificationProviderProps> = ({ children }) => {
  const {
    isSupported,
    permission,
    requestPermission,
    showNotification,
    scheduleNotificationsForTasks,
    hasPermission
  } = useNotification();

  useEffect(() => {
    // Initialize notification permission when the provider mounts
    if (isSupported && permission === 'default') {
      // Optionally prompt for permission automatically or let the user decide
      // For now, we'll let the user decide when to request permission
    }
  }, [isSupported, permission]);

  return (
    <NotificationContext.Provider
      value={{
        isSupported,
        permission,
        requestPermission,
        showNotification,
        scheduleNotificationsForTasks,
        hasPermission,
      }}
    >
      {children}
    </NotificationContext.Provider>
  );
};