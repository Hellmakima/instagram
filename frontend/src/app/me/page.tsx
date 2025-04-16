"use client";

import { useEffect, useState } from "react";

import Cookies from "js-cookie";
import LogoutButton from "@/app/components/LogoutButton";

export default function MePage() {
  interface UserData {
    username: string;
  }

  const [userData, setUserData] = useState<UserData | null>(null);

  useEffect(() => {
    const token = Cookies.get("token");
    if (!token) {
      window.location.href = "/login";
      return;
    }

    const fetchUser = async () => {
      const res = await fetch("http://localhost:5000/auth/me", {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        const data = await res.json();
        setUserData(data);
      } else {
        Cookies.remove("token");
        window.location.href = "/login";
      }
    };

    fetchUser();
  }, []);

  if (!userData) return <p className="text-center mt-10">Loading...</p>;

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-2xl font-bold mb-4">Welcome, {userData.user}!</h1>
      <LogoutButton />
    </div>
  );
}