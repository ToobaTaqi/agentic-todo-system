import { Task } from '../types/types';

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Utility function to get auth token
const getAuthToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('auth_token');
  }
  return null;
};

// Utility function to create headers with auth token
const getHeaders = (includeAuth: boolean = true) => {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };

  if (includeAuth) {
    const token = getAuthToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    } else {
      // If no token is available but auth is required, we might want to handle this differently
      console.warn('No authentication token found for protected endpoint');
    }
  }

  return headers;
};

// Auth API functions
export const authApi = {
  // Register a new user
  register: async (userData: { email: string; password: string; first_name?: string; last_name?: string }): Promise<{ access_token: string; token_type: string; user: any }> => {
    try {
      // const response = await fetch(`${API_BASE_URL}/api/v1/register`, {
      const response = await fetch(`${API_BASE_URL}/api/v1/register`, {
        method: 'POST',
        headers: getHeaders(false), // Don't include auth token for registration
        body: JSON.stringify(userData),
      });
       console.log(response,"response")

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Registration failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Error registering user:', error);
      throw error;
    }
  },

  // Login user
  login: async (credentials: { email: string; password: string }): Promise<{ access_token: string; token_type: string; user: any }> => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/login`, {
        method: 'POST',
        headers: getHeaders(false), // Don't include auth token for login
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Login failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Error logging in:', error);
      throw error;
    }
  },

  // Get current session
  getSession: async (token: string): Promise<any> => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/session`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Session validation failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting session:', error);
      throw error;
    }
  },
};

// Task API functions
export const api = {
  // Get all tasks for the authenticated user
  getTasks: async (): Promise<Task[]> => {
    try {
      // Get the authenticated user's ID from the stored user data
      let userId = '';
      if (typeof window !== 'undefined') {
        const storedUser = localStorage.getItem('auth_user');
        if (storedUser) {
          const user = JSON.parse(storedUser);
          userId = user.id;
        }
      }

      const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks`, {
        method: 'GET',
        headers: getHeaders(),
      });

      if (!response.ok) {
        if (response.status === 401) {
          // Unauthorized - token might be expired
          localStorage.removeItem('auth_token');
          localStorage.removeItem('auth_user');
          window.location.href = '/auth/login';
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching tasks:', error);
      throw error;
    }
  },

  // Create a new task
  createTask: async (taskData: Omit<Task, 'id' | 'user_id' | 'created_at' | 'updated_at'>): Promise<Task> => {
    try {
      // Get the authenticated user's ID from the stored user data
      let userId = '';
      if (typeof window !== 'undefined') {
        const storedUser = localStorage.getItem('auth_user');
        if (storedUser) {
          const user = JSON.parse(storedUser);
          userId = user.id;
        }
      }

      const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks`, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        if (response.status === 401) {
          // Unauthorized - token might be expired
          localStorage.removeItem('auth_token');
          localStorage.removeItem('auth_user');
          window.location.href = '/auth/login';
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error creating task:', error);
      throw error;
    }
  },

  // Get a specific task
  getTask: async (taskId: string): Promise<Task> => {
    try {
      // Get the authenticated user's ID from the stored user data
      let userId = '';
      if (typeof window !== 'undefined') {
        const storedUser = localStorage.getItem('auth_user');
        if (storedUser) {
          const user = JSON.parse(storedUser);
          userId = user.id;
        }
      }

      const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks/${taskId}`, {
        method: 'GET',
        headers: getHeaders(),
      });

      if (!response.ok) {
        if (response.status === 401) {
          // Unauthorized - token might be expired
          localStorage.removeItem('auth_token');
          localStorage.removeItem('auth_user');
          window.location.href = '/auth/login';
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching task:', error);
      throw error;
    }
  },

  // Update a task
  updateTask: async (taskId: string, taskData: Partial<Task>): Promise<Task> => {
    try {
      // Get the authenticated user's ID from the stored user data
      let userId = '';
      if (typeof window !== 'undefined') {
        const storedUser = localStorage.getItem('auth_user');
        if (storedUser) {
          const user = JSON.parse(storedUser);
          userId = user.id;
        }
      }

      const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks/${taskId}`, {
        method: 'PUT',
        headers: getHeaders(),
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        if (response.status === 401) {
          // Unauthorized - token might be expired
          localStorage.removeItem('auth_token');
          localStorage.removeItem('auth_user');
          window.location.href = '/auth/login';
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error updating task:', error);
      throw error;
    }
  },

  // Delete a task
  deleteTask: async (taskId: string): Promise<void> => {
    try {
      // Get the authenticated user's ID from the stored user data
      let userId = '';
      if (typeof window !== 'undefined') {
        const storedUser = localStorage.getItem('auth_user');
        if (storedUser) {
          const user = JSON.parse(storedUser);
          userId = user.id;
        }
      }

      const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks/${taskId}`, {
        method: 'DELETE',
        headers: getHeaders(),
      });

      if (!response.ok) {
        if (response.status === 401) {
          // Unauthorized - token might be expired
          localStorage.removeItem('auth_token');
          localStorage.removeItem('auth_user');
          window.location.href = '/auth/login';
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error deleting task:', error);
      throw error;
    }
  },

  // Toggle task completion
  toggleTaskCompletion: async (taskId: string): Promise<Task> => {
    try {
      // Get the authenticated user's ID from the stored user data
      let userId = '';
      if (typeof window !== 'undefined') {
        const storedUser = localStorage.getItem('auth_user');
        if (storedUser) {
          const user = JSON.parse(storedUser);
          userId = user.id;
        }
      }

      const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks/${taskId}/complete`, {
        method: 'PATCH',
        headers: getHeaders(),
      });

      if (!response.ok) {
        if (response.status === 401) {
          // Unauthorized - token might be expired
          localStorage.removeItem('auth_token');
          localStorage.removeItem('auth_user');
          window.location.href = '/auth/login';
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error toggling task completion:', error);
      throw error;
    }
  },

  // Chat with AI
  chatWithAI: async (userId: string, requestData: { conversation_id?: string; message: string }): Promise<any> => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/${userId}/chat`, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        if (response.status === 401) {
          // Unauthorized - token might be expired
          localStorage.removeItem('auth_token');
          localStorage.removeItem('auth_user');
          window.location.href = '/auth/login';
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error chatting with AI:', error);
      throw error;
    }
  },
};