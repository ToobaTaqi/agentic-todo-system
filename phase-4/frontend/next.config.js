/** @type {import('next').NextConfig} */
const nextConfig = {
  typedRoutes: true,
  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'localhost',
      },
      {
        protocol: 'https',
        hostname: 'your-production-domain.com',
      },
    ],
  },
  // Removed turbopack configuration as it's causing build issues
  // turbopack is experimental and may not work with all Next.js features
};

module.exports = nextConfig;