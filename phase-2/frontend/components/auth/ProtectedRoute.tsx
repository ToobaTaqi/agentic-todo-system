"use client";

import { useAuth } from "../../lib/contexts/AuthContext";
// import { useAuth } from '@/lib/contexts/AuthContext';
import { useEffect } from "react";
import { useRouter } from "next/navigation";

interface ProtectedRouteProps {
  children: React.ReactNode;
  redirectTo?: any;
  requireVerified?: boolean;
}

export default function ProtectedRoute(
  {
  children,
  redirectTo = "/auth/login",
  requireVerified = true, // Whether to require email verification
}: ProtectedRouteProps & { requireVerified?: boolean }) {
  const { isAuthenticated, user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push(redirectTo);
    } else if (!loading && isAuthenticated && requireVerified && user && !user.is_verified) {
      // If user is authenticated but not verified, redirect to check-inbox page
      router.push("/check-inbox");
    }
  }, [isAuthenticated, user, loading, router, redirectTo, requireVerified]);

  // Show loading state while checking authentication
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-text-primary">Loading...</p>
        </div>
      </div>
    );
  }

  // If authenticated and verified (or verification not required), render the protected content
  if (isAuthenticated && (!requireVerified || (user && user.is_verified))) {
    return <>{children}</>;
  }

  // If not authenticated and not loading, show nothing or redirect has already happened
  return null;
}
