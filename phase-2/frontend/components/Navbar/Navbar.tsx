"use client";

// import { useAuth } from '../../../lib/contexts/AuthContext';
import { useAuth } from "@/lib/contexts/AuthContext";
import Link from "next/link";
import { useState } from "react";

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error("Logout error:", error);
    }
  };

  return (
    <nav className="bg-surface shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/dashboard" className="flex-shrink-0 flex items-center">
              <span className="text-xl font-bold text-text-primary">
                TodoApp
              </span>
            </Link>
          </div>

          <div className="hidden md:flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <Link
                  href="/dashboard"
                  className="text-text-secondary hover:text-text-primary px-3 py-2 rounded-md text-sm font-medium"
                >
                  Dashboard
                </Link>
                <div className="relative group">
                  <button className="text-text-secondary hover:text-text-primary px-3 py-2 rounded-md text-sm font-medium">
                    {user?.first_name ||
                      user?.email?.split("@")[0] ||
                      "Account"}{" "}
                    ▼
                  </button>
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                    <Link
                      href={{ pathname: "/profile" }}
                      className="block px-4 py-2 text-sm text-text-secondary hover:bg-gray-100"
                    >
                      Profile
                    </Link>
                    <Link
                      href={{ pathname: "/settings" }}
                      className="block px-4 py-2 text-sm text-text-secondary hover:bg-gray-100"
                    >
                      Settings
                    </Link>
                    <button
                      onClick={handleLogout}
                      className="block w-full text-left px-4 py-2 text-sm text-text-secondary hover:bg-gray-100"
                    >
                      Sign out
                    </button>
                  </div>
                </div>
              </>
            ) : (
              <>
                <Link
                  href="/auth/login"
                  className="text-text-secondary hover:text-text-primary px-3 py-2 rounded-md text-sm font-medium"
                >
                  Sign in
                </Link>
                <Link
                  href="/auth/register"
                  className="bg-primary hover:bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium"
                >
                  Sign up
                </Link>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-text-secondary hover:text-text-primary"
            >
              <svg
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                {isMenuOpen ? (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                ) : (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {isMenuOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            {isAuthenticated ? (
              <>
                <Link
                  href="/dashboard"
                  className="text-text-secondary hover:text-text-primary block px-3 py-2 rounded-md text-base font-medium"
                >
                  Dashboard
                </Link>
                <Link
                  href={{ pathname: "/profile" }}
                  className="text-text-secondary hover:text-text-primary block px-3 py-2 rounded-md text-base font-medium"
                >
                  Profile
                </Link>
                <Link
                  href={{ pathname: "/settings" }}
                  className="text-text-secondary hover:text-text-primary block px-3 py-2 rounded-md text-base font-medium"
                >
                  Settings
                </Link>
                <button
                  onClick={handleLogout}
                  className="w-full text-left text-text-secondary hover:text-text-primary block px-3 py-2 rounded-md text-base font-medium"
                >
                  Sign out
                </button>
              </>
            ) : (
              <>
                <Link
                  href="/auth/login"
                  className="text-text-secondary hover:text-text-primary block px-3 py-2 rounded-md text-base font-medium"
                >
                  Sign in
                </Link>
                <Link
                  href="/auth/register"
                  className="text-text-secondary hover:text-text-primary block px-3 py-2 rounded-md text-base font-medium"
                >
                  Sign up
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}
