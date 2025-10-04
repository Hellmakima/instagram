// components/organisms/Footer.tsx
"use client";

import Link from "next/link";
import { Home, Search, PlusCircle, Heart, User } from "lucide-react";

export function Footer() {
  return (
    <footer className="w-full bg-white border-t shadow-inner">
      <div className="max-w-7xl mx-auto flex justify-around p-3 md:hidden">
        <Link href="/">
          <Home className="w-6 h-6 text-gray-600 hover:text-indigo-600" />
        </Link>
        <Link href="/search">
          <Search className="w-6 h-6 text-gray-600 hover:text-indigo-600" />
        </Link>
        <Link href="/upload">
          <PlusCircle className="w-6 h-6 text-gray-600 hover:text-indigo-600" />
        </Link>
        <Link href="/notifications">
          <Heart className="w-6 h-6 text-gray-600 hover:text-indigo-600" />
        </Link>
        <Link href="/profile">
          <User className="w-6 h-6 text-gray-600 hover:text-indigo-600" />
        </Link>
      </div>
      <div className="hidden md:flex justify-center p-2 text-xs text-gray-500">
        &copy; {new Date().getFullYear()} Nmaa - Instagram Clone
        <Link href="https://github.com/hellmakima/instagram">
          <p className="ml-2 underline">GitHub</p>
        </Link>
      </div>
    </footer>
  );
}
