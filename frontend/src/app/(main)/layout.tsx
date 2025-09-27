// A'udhu billahi min ash-shaytan ir-rajim Bismillahi ar-Rahmani ar-Rahim

import "@/app/globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Welcome to Nmaa",
  description: "Where the magic happens",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body suppressHydrationWarning>{children}</body>
    </html>
  );
}
