'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
// import { useAuth } from '../lib/contexts/AuthContext';
import { useAuth } from '../lib/contexts/AuthContext';

export default function HomePage() {
  const router = useRouter();
  const { isAuthenticated, user, loading } = useAuth();

  useEffect(() => {
    if (!loading) {
      if (isAuthenticated) {
        // If user is authenticated but not verified, redirect to check-inbox
        if (user && !user.is_verified) {
          router.push('/check-inbox');
        } else {
          // If user is authenticated and verified, redirect to dashboard
          router.push('/dashboard');
        }
      } else {
        // If user is not authenticated, redirect to login
        router.push('/auth/login');
      }
    }
  }, [isAuthenticated, user, loading, router]);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-text-primary mb-4">AI-Ready Todo App</h1>
        <p className="text-text-secondary">Redirecting...</p>
      </div>
    </div>
  );
}