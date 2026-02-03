"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "../../../lib/contexts/AuthContext";
import Link from "next/link";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const router = useRouter();
  const { register } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await register(email, password, firstName, lastName);

      // Store the email for the check-inbox page
      localStorage.setItem('pending_verification_email', email);

      // Redirect to check-inbox page after registration
      router.push("/check-inbox");
      router.refresh(); // Refresh to update UI
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="max-w-md w-full space-y-8 p-8 bg-surface rounded-xl shadow-lg">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-text-primary">
            Create a new account
          </h2>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
              {error}
            </div>
          )}

          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label
                  htmlFor="firstName"
                  className="block text-sm font-medium text-text-secondary"
                >
                  First Name
                </label>
                <input
                  id="firstName"
                  name="firstName"
                  type="text"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                  className="mt-1 appearance-none relative block w-full px-3 py-2 border border-border rounded-md placeholder-text-secondary focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  disabled={loading}
                />
              </div>

              <div>
                <label
                  htmlFor="lastName"
                  className="block text-sm font-medium text-text-secondary"
                >
                  Last Name
                </label>
                <input
                  id="lastName"
                  name="lastName"
                  type="text"
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                  className="mt-1 appearance-none relative block w-full px-3 py-2 border border-border rounded-md placeholder-text-secondary focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  disabled={loading}
                />
              </div>
            </div>

            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-text-secondary"
              >
                Email address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="mt-1 appearance-none relative block w-full px-3 py-2 border border-border rounded-md placeholder-text-secondary focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                disabled={loading}
              />
            </div>

            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-text-secondary"
              >
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="new-password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="mt-1 appearance-none relative block w-full px-3 py-2 border border-border rounded-md placeholder-text-secondary focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                disabled={loading}
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              {loading ? "Creating account..." : "Create Account"}
            </button>
          </div>
        </form>

        <div className="text-center text-sm text-text-secondary">
          Already have an account?
          <Link
            href="/auth/login"
            className="font-medium text-indigo-600 hover:text-indigo-500"
          >
            Sign in
          </Link>
        </div>

        {/* Information for teachers */}
        <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-md">
          <h3 className="text-sm font-semibold text-yellow-800 mb-2">For Teachers:</h3>
          <p className="text-xs text-yellow-700 mb-2">
            <strong>Demo Credentials:</strong> Email: <code className="bg-yellow-100 px-1 rounded">toobtq01@gmail.com</code> | Password: <code className="bg-yellow-100 px-1 rounded">asklty01</code>
          </p>
          <p className="text-xs text-yellow-700">
            <strong>Email Verification Note:</strong> This app uses Resend for email verification.
            Due to free tier limitations, verification emails are only sent to the registered domain email.
            To experience the full app, use the demo credentials above.
          </p>
        </div>
      </div>
    </div>
  );
}
