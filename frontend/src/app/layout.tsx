// A'udhu billahi min ash-shaytan ir-rajim Bismillahi ar-Rahmani ar-Rahim

// src/app/layout.tsx

import "@/app/globals.css";
import StoreProvider from "@/lib/store/StoreProvider";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Nmaa",
  description: "Experience social media built for connection, not addiction.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <StoreProvider>
      <html lang="en">
        <body suppressHydrationWarning>{children}</body>
      </html>
    </StoreProvider>
  );
}
