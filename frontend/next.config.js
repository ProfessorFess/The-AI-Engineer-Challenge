/** @type {import('next').NextConfig} */
const nextConfig = {
  // App directory is enabled by default in Next.js 13+
  async rewrites() {
    // Only proxy to localhost during local development
    // On Vercel, the main vercel.json handles API routing
    if (process.env.NODE_ENV === 'development') {
      return [
        {
          source: '/api/:path*',
          destination: 'http://localhost:8000/api/:path*', // Proxy to Backend
        },
      ]
    }
    return []
  },
}

module.exports = nextConfig
