// next.config.js

import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  env: {
    AUTH_SERVER_URL: process.env.NEXT_PUBLIC_AUTH_SERVER_URL,
  },
};

export default nextConfig;