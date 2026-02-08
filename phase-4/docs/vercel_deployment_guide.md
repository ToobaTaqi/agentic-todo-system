# Vercel Deployment Configuration for Next.js App

## Issue
Error: No Output Directory named "public" found after the Build completed. Configure the Output Directory in your Project Settings.

## Root Cause
Vercel is looking for a traditional static site output in a "public" directory, but Next.js 16 with App Router generates output in a different structure.

## Solution

### 1. Vercel Configuration
The vercel.json file should specify the framework:

```json
{
  "framework": "nextjs"
}
```

### 2. Next.js Configuration
Make sure your next.config.js (if it exists) is properly configured:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  // For static export (if needed)
  // output: 'export',  // Uncomment only if you need static export
  
  // For API routes to work properly with external backend
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NEXT_PUBLIC_API_BASE_URL ? `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/:path*` : 'http://localhost:8000/api/:path*',
      },
    ]
  },
}

module.exports = nextConfig
```

### 3. Environment Variables
Ensure your environment variables are set in Vercel dashboard:
- NEXT_PUBLIC_API_BASE_URL (pointing to your deployed backend)

### 4. Build Process
Next.js 16 with App Router should build correctly with:
```bash
npm run build
```

### 5. Vercel Project Settings
In your Vercel project settings:
- Framework Preset: Next.js (should be auto-detected)
- Build Command: `npm run build` (should be auto-detected)
- Output Directory: Leave empty for Next.js (Vercel handles this automatically)
- Install Command: `npm install` (should be auto-detected)

### 6. Important Notes
- Don't manually specify outputDirectory as "public" for Next.js apps
- Next.js apps output to .next/ directory during build
- Vercel automatically handles serving the Next.js app
- If you need static export, add `output: 'export'` to next.config.js and remove API routes

## Troubleshooting

### If still getting errors:
1. Check that your Next.js version is compatible with Vercel
2. Verify all dependencies are properly listed in package.json
3. Make sure there are no build errors locally with `npm run build`
4. Check that your API routes are properly configured for proxying if needed

### For Static Export (only if required):
If you specifically need static export, add to next.config.js:
```javascript
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true, // Required for static export
  },
}
```

Then the output would be in the "out" directory instead of .next/