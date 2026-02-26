import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { AuthProvider } from '../lib/contexts/AuthContext';
// import { NotificationProvider } from '../components/Notifications/NotificationProvider';
import { NotificationProvider } from '../components/notifications/NotificationProvider';
import Navbar from '../components/Navbar/Navbar';

// Updated font configuration to avoid Turbopack issues
const inter = Inter({ 
  subsets: ['latin'],
  display: 'swap', // Use swap to avoid font loading issues
});

export const metadata: Metadata = {
  title: 'AI-Ready Todo App',
  description: 'A smart todo application with advanced features',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          <NotificationProvider>
            <Navbar />
            <main>
              {children}
            </main>
          </NotificationProvider>
        </AuthProvider>
      </body>
    </html>
  );
}