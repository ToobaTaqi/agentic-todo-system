export interface Task {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  priority: 'high' | 'medium' | 'low';
  tags: string[];
  label?: 'work' | 'home' | null; // Label field for categorization
  due_date?: string | null; // ISO string format
  is_completed: boolean;
  is_recurring: boolean;
  recurrence_pattern?: 'daily' | 'weekly' | 'monthly' | null;
  created_at: string; // ISO string
  updated_at: string; // ISO string
}