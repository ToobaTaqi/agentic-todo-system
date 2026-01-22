// frontend/components/Notifications/NotificationService.ts
export class NotificationService {
  private static instance: NotificationService;

  private constructor() {}

  public static getInstance(): NotificationService {
    if (!NotificationService.instance) {
      NotificationService.instance = new NotificationService();
    }
    return NotificationService.instance;
  }

  /**
   * Request notification permission from the user
   */
  async requestPermission(): Promise<NotificationPermission> {
    if (!('Notification' in window)) {
      throw new Error('Browser does not support notifications');
    }

    if (Notification.permission === 'granted') {
      return 'granted';
    }

    const permission = await Notification.requestPermission();
    return permission;
  }

  /**
   * Check if notifications are supported and permission is granted
   */
  canNotify(): boolean {
    return (
      'Notification' in window &&
      Notification.permission === 'granted'
    );
  }

  /**
   * Show a notification for a task due soon
   */
  showTaskNotification(title: string, body: string, tag?: string): void {
    if (!this.canNotify()) {
      console.warn('Notifications not available or permission not granted');
      return;
    }

    const notification = new Notification(title, {
      body,
      tag,
      icon: '/favicon.ico', // Use your app's favicon
      requireInteraction: false, // Auto-dismiss after a few seconds
    });

    // Close notification after 5 seconds if not clicked
    setTimeout(() => {
      notification.close();
    }, 5000);

    // Handle notification click
    notification.onclick = () => {
      window.focus();
      notification.close();
    };
  }

  /**
   * Schedule a notification for a specific time
   */
  scheduleNotification(
    title: string,
    body: string,
    scheduledTime: Date,
    tag?: string
  ): number {
    const timeDiff = scheduledTime.getTime() - Date.now();

    if (timeDiff <= 0) {
      // If the time has already passed, show immediately
      this.showTaskNotification(title, body, tag);
      return -1; // No timer needed
    }

    const timerId = window.setTimeout(() => {
      this.showTaskNotification(title, body, tag);
    }, timeDiff);

    return timerId;
  }

  /**
   * Cancel a scheduled notification
   */
  cancelScheduledNotification(timerId: number): void {
    if (timerId !== -1) {
      clearTimeout(timerId);
    }
  }

  /**
   * Show a notification for an upcoming task deadline
   */
  showUpcomingDeadline(taskTitle: string, dueDateTime: Date): void {
    const timeUntilDue = dueDateTime.getTime() - Date.now();
    const hoursUntilDue = Math.floor(timeUntilDue / (1000 * 60 * 60));

    let title = `Task Due Soon: ${taskTitle}`;
    let body = `This task is due ${dueDateTime.toLocaleString()}`;

    if (hoursUntilDue <= 1) {
      title = `URGENT: Task Due Soon!`;
      body = `"${taskTitle}" is due in less than an hour at ${dueDateTime.toLocaleTimeString()}`;
    }

    this.showTaskNotification(title, body);
  }

  /**
   * Check for upcoming deadlines and schedule notifications
   */
  checkAndScheduleNotifications(tasks: Array<{
    id: string;
    title: string;
    due_date?: string | null;
  }>): Map<string, number> {
    const scheduledTimers = new Map<string, number>();

    tasks.forEach(task => {
      if (task.due_date) {
        const dueDate = new Date(task.due_date);
        const now = new Date();

        // Only schedule notifications for future due dates
        if (dueDate > now) {
          // Calculate time until notification should fire (1 hour before due)
          const notificationTime = new Date(dueDate.getTime() - (60 * 60 * 1000)); // 1 hour before

          // Only schedule if the notification time is in the future
          if (notificationTime > now) {
            const timerId = this.scheduleNotification(
              `Task Due Soon: ${task.title}`,
              `This task is due at ${dueDate.toLocaleTimeString()} today`,
              notificationTime,
              `task-${task.id}-deadline`
            );

            scheduledTimers.set(task.id, timerId);
          } else if (dueDate > now && dueDate.getTime() - now.getTime() < 60 * 60 * 1000) {
            // If due date is less than 1 hour away but more than now, show immediately
            this.showUpcomingDeadline(task.title, dueDate);
          }
        }
      }
    });

    return scheduledTimers;
  }
}