import type { NextConfig } from "next";

// /** @type {import('next').NextConfig} */

const nextConfig:NextConfig = {
  async rewrites() {
    return [
      {
        source: '/auth/:path*',
        destination: 'http://localhost:5000/auth/:path*', // Proxy to your backend auth API
      },
      {
        source: '/user/:path*',
        destination: 'http://localhost:5000/user/:path*', // Proxy to your backend user API
      },
    ];
  },
};

export default nextConfig;
