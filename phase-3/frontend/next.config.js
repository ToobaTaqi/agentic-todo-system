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
  turbopack: {
    root: __dirname,
  },
};

module.exports = nextConfig;