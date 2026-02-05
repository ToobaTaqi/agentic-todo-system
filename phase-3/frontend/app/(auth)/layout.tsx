import { Inter } from 'next/font/google';
// import '../../globals.css';

const inter = Inter({ subsets: ['latin'] });

// Layout for authentication pages that don't require authentication
export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <main>
          {children}
        </main>
      </body>
    </html>
  );
}