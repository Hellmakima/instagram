// components/organisms/Header.tsx
"use client";

import Link from "next/link";
import { Home, Search, PlusCircle, Heart, User } from "lucide-react";

export function Header() {
  return (
    <header className="hidden w-full bg-white border-b shadow-sm">
      <div className="max-w-7xl mx-auto flex items-center justify-between p-4">
        <Link href="/">
          <Home className="w-6 h-6 text-gray-600 hover:text-indigo-600" />
        </Link>
      </div>
    </header>
  );
}
