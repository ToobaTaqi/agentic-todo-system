'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';

// Disable static generation for this page since it requires client-side hooks
export const dynamic = 'force-dynamic';

export default function VerifyEmailPage() {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get('token');

  // Ref to hold the redirect timeout ID
  const redirectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  // Automatically verify the token when the page loads
  useEffect(() => {
    const verifyTokenOnLoad = async () => {
      if (!token) {
        setError('No verification token provided');
        return;
      }

      // Skip if already processed (to prevent multiple calls)
      if (loading || message || error) return;

      setLoading(true);
      setError('');

      try {
        // Call the backend verification endpoint - ensure no auth headers are included
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/verify-email`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'omit', // Explicitly omit any stored credentials/cookies
          body: JSON.stringify({ token }), // Send token in the request body
        });

        const data = await response.json();

        if (response.ok) {
          setMessage(data.message || 'Email verified successfully!');

          // Clear any existing timeout to prevent multiple redirects
          if (redirectTimeoutRef.current) {
            clearTimeout(redirectTimeoutRef.current);
          }

          // Redirect to login after a short delay so user can log in with verified status
          redirectTimeoutRef.current = setTimeout(() => {
            router.push('/auth/login'); // Redirect to login after verification
          }, 3000);
        } else {
          setError(data.detail || 'Failed to verify email');
        }
      } catch (err) {
        console.error('Verification error:', err);
        setError('An error occurred during verification');
      } finally {
        setLoading(false);
      }
    };

    // Only run if we have a token and haven't started verification yet
    if (token && !loading && !message && !error) {
      verifyTokenOnLoad();
    }

    // Cleanup function to clear timeout if component unmounts
    return () => {
      if (redirectTimeoutRef.current) {
        clearTimeout(redirectTimeoutRef.current);
      }
    };
  }, [token, loading, message, error, router]);

  const handleVerifyClick = async () => {
    if (!token) {
      setError('No verification token provided');
      return;
    }

    // Prevent multiple clicks while verifying
    if (loading) return;

    setLoading(true);
    setError('');

    try {
      // Call the backend verification endpoint - ensure no auth headers are included
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/verify-email`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'omit', // Explicitly omit any stored credentials/cookies
        body: JSON.stringify({ token }), // Send token in the request body
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(data.message || 'Email verified successfully!');

        // Clear any existing timeout to prevent multiple redirects
        if (redirectTimeoutRef.current) {
          clearTimeout(redirectTimeoutRef.current);
        }

        // Redirect to login after a short delay so user can log in with verified status
        redirectTimeoutRef.current = setTimeout(() => {
          router.push('/auth/login'); // Redirect to login after verification
        }, 3000);
      } else {
        setError(data.detail || 'Failed to verify email');
      }
    } catch (err) {
      console.error('Verification error:', err);
      setError('An error occurred during verification');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Verify Your Email
        </h2>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <div className="text-center">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-blue-100">
              <svg className="h-6 w-6 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h3 className="mt-2 text-lg font-medium text-gray-900">Email Verification Required</h3>
            <p className="mt-2 text-sm text-gray-500">
              {loading ? 'Verifying your email...' : 'Please click the button below to verify your email address.'}
            </p>
          </div>

          {error && (
            <div className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md text-sm">
              {error}
            </div>
          )}

          {message && (
            <div className="mt-4 bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-md text-sm">
              {message}
            </div>
          )}

          <div className="mt-6">
            <button
              onClick={handleVerifyClick}
              disabled={loading}
              className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${
                loading
                  ? 'bg-indigo-400 cursor-not-allowed'
                  : 'bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
              }`}
            >
              {loading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Verifying...
                </>
              ) : (
                'Click Here to Verify'
              )}
            </button>
          </div>

          <div className="mt-4 text-center text-sm text-gray-500">
            <button
              onClick={() => router.push('/auth/login')}
              className="font-medium text-indigo-600 hover:text-indigo-500"
              disabled={loading} // Disable during verification
            >
              Back to Login
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}