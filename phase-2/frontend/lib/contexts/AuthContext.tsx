'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
// Using the original API approach instead of Better Auth until properly configured
import { api, authApi, API_BASE_URL } from '../api/api';
import { Task } from '../types/types';

interface User {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, firstName?: string, lastName?: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
  updateProfile: (firstName?: string, lastName?: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check for existing token on mount
  useEffect(() => {
    const storedToken = localStorage.getItem('auth_token');
    const storedUser = localStorage.getItem('auth_user');

    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
      setIsAuthenticated(true);
    }

    setLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    try {
      setLoading(true);

      const data = await authApi.login({ email, password });
      const { access_token, user: userData } = data;

      // Store token and user data
      setToken(access_token);
      setUser(userData);
      setIsAuthenticated(true);

      localStorage.setItem('auth_token', access_token);
      localStorage.setItem('auth_user', JSON.stringify(userData));
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const register = async (email: string, password: string, firstName?: string, lastName?: string) => {
    try {
      setLoading(true);

      const data = await authApi.register({
        email,
        password,
        first_name: firstName,
        last_name: lastName
      });
      const { access_token, user: userData } = data;

      // Store token and user data
      setToken(access_token);
      setUser(userData);
      setIsAuthenticated(true);

      localStorage.setItem('auth_token', access_token);
      localStorage.setItem('auth_user', JSON.stringify(userData));

    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };
  // console.log(register,"clg in /lib/contexts/AuthContext.tsx")

  const logout = () => {
    setToken(null);
    setUser(null);
    setIsAuthenticated(false);

    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
  };

  const refreshToken = async () => {
    if (!token) {
      throw new Error('No token available for refresh');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Token refresh failed');
      }

      const data = await response.json();
      const newToken = data.access_token;

      setToken(newToken);
      localStorage.setItem('auth_token', newToken);
    } catch (error) {
      console.error('Token refresh error:', error);
      throw error;
    }
  };

  const updateProfile = async (firstName?: string, lastName?: string) => {
    if (!token) {
      throw new Error('Not authenticated');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/profile`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ first_name: firstName, last_name: lastName }),
      });

      if (!response.ok) {
        throw new Error('Profile update failed');
      }

      const updatedUser = await response.json();
      setUser(updatedUser);
      localStorage.setItem('auth_user', JSON.stringify(updatedUser));
    } catch (error) {
      console.error('Profile update error:', error);
      throw error;
    }
  };

  const value = {
    user,
    token,
    isAuthenticated,
    loading,
    login,
    register,
    logout,
    refreshToken,
    updateProfile,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};