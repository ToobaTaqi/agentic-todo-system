'use client';

import { useAuth } from '../../lib/contexts/AuthContext';

export default function AuthStatus() {
  const { user, isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="p-4">
      <h2>Authentication Status</h2>
      {isAuthenticated ? (
        <div>
          <p>Signed in as: {user?.email}</p>
          <p>Name: {user?.first_name} {user?.last_name}</p>
        </div>
      ) : (
        <p>Not signed in</p>
      )}
    </div>
  );
}