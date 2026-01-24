'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/contexts/AuthContext';

export default function CheckInboxPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuth();
  const [email, setEmail] = useState('');

  useEffect(() => {
    // Get email from localStorage if available
    const storedEmail = localStorage.getItem('pending_verification_email');
    if (storedEmail) {
      setEmail(storedEmail);
      // Clear the stored email after retrieving it
      localStorage.removeItem('pending_verification_email');
    }

    // If user is already authenticated and verified, redirect to dashboard
    if (isAuthenticated) {
      // We'll need to check if the user is verified here
      const storedUser = localStorage.getItem('auth_user');
      if (storedUser) {
        const user = JSON.parse(storedUser);
        if (user.is_verified) {
          router.push('/dashboard');
        }
      }
    }
  }, [isAuthenticated, router]);

  const handleGoToLogin = () => {
    router.push('/auth/login');
  };

  const handleResendEmail = () => {
    // This would be implemented to resend verification email
    alert('Verification email resent. Please check your inbox.');
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
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100">
              <svg className="h-6 w-6 text-green-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h3 className="mt-2 text-lg font-medium text-gray-900">Check your email</h3>
            <div className="mt-4 text-sm text-gray-500">
              <p>We've sent a verification link to {email || 'your email address'}.</p>
              <p className="mt-2">Please click the link to verify your account.</p>
            </div>
          </div>

          <div className="mt-6 grid grid-cols-2 gap-3">
            <button
              onClick={handleGoToLogin}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-gray-600 hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
            >
              Login
            </button>
            <button
              onClick={handleResendEmail}
              className="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Resend Email
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}