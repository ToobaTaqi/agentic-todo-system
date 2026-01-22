// frontend/lib/hooks/useNotification.ts
import { useEffect, useState, useRef } from 'react';
import { NotificationService } from '@/components/Notifications/NotificationService';

export interface TaskWithDueDate {
  id: string;
  title: string;
  due_date?: string | null;
}

export const useNotification = () => {
  const [permission, setPermission] = useState<NotificationPermission>('default');
  const [isSupported, setIsSupported] = useState<boolean>(false);
  const scheduledNotifications = useRef<Map<string, number>>(new Map()).current;

  useEffect(() => {
    // Check if notifications are supported
    const supported = 'Notification' in window;
    setIsSupported(supported);

    if (supported) {
      setPermission(Notification.permission);
    }
  }, []);

  const requestPermission = async (): Promise<NotificationPermission> => {
    if (!isSupported) {
      throw new Error('Browser does not support notifications');
    }

    if (Notification.permission === 'granted') {
      setPermission('granted');
      return 'granted';
    }

    const newPermission = await Notification.requestPermission();
    setPermission(newPermission);
    return newPermission;
  };

  const showNotification = (title: string, body: string, tag?: string): void => {
    if (permission !== 'granted') {
      console.warn('Notifications not granted');
      return;
    }

    const notificationService = NotificationService.getInstance();
    notificationService.showTaskNotification(title, body, tag);
  };

  const scheduleNotificationsForTasks = (tasks: TaskWithDueDate[]): Map<string, number> => {
    if (permission !== 'granted') {
      console.warn('Cannot schedule notifications: permission not granted');
      return new Map();
    }

    const notificationService = NotificationService.getInstance();
    const timers = notificationService.checkAndScheduleNotifications(tasks);

    // Store scheduled timers
    timers.forEach((timerId, taskId) => {
      scheduledNotifications.set(taskId, timerId);
    });

    return timers;
  };

  const cancelScheduledNotification = (taskId: string): void => {
    const timerId = scheduledNotifications.get(taskId);
    if (timerId) {
      const notificationService = NotificationService.getInstance();
      notificationService.cancelScheduledNotification(timerId);
      scheduledNotifications.delete(taskId);
    }
  };

  return {
    isSupported,
    permission,
    requestPermission,
    showNotification,
    scheduleNotificationsForTasks,
    cancelScheduledNotification,
    hasPermission: permission === 'granted',
  };
};