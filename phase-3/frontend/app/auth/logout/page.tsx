'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../../../lib/contexts/AuthContext';

export default function LogoutPage() {
  const router = useRouter();
  const { logout } = useAuth();

  useEffect(() => {
    // Perform logout and redirect
    logout();
    router.push('/auth/login');
    router.refresh(); // Refresh to update UI
  }, [logout, router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="text-center">
        <p className="text-text-primary">Logging out...</p>
      </div>
    </div>
  );
}