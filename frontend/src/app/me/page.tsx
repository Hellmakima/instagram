"use client";

import { useEffect, useState } from "react";

export default function MePage() {
  interface UserData {
    username: string;
    email?: string;
  }

  const [userData, setUserData] = useState<UserData | null>(null);
  const [loading, setLoading] = useState(true);

  const redirectToLogin = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    window.location.href = "/login";
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    window.location.href = "/login";
  };

  const manualRefresh = async () => {
    const refresh_token = localStorage.getItem("refresh_token");
    if (!refresh_token) return alert("No refresh token found!");

    try {
      const response = await fetch("http://localhost:5000/auth/refresh", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          refresh_token: refresh_token,
          token_type: "Bearer",
        }),
      });

      if (!response.ok) throw new Error(await response.text());

      const result = await response.json();
      localStorage.setItem("access_token", result.access_token);
      localStorage.setItem("refresh_token", result.refresh_token);

      alert("Token refreshed successfully!");
      loadProfile();
    } catch (err) {
      alert("Failed to refresh token: " + (err instanceof Error ? err.message : "Unknown error"));
    }
  };

  const loadProfile = async () => {
    setLoading(true);
    let token = localStorage.getItem("access_token");
    if (!token) return redirectToLogin();

    try {
      let response = await fetch("http://localhost:5000/user/me", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.status === 401) {
        const refresh_token = localStorage.getItem("refresh_token");
        if (!refresh_token) return redirectToLogin();

        const refreshResponse = await fetch("http://localhost:5000/auth/refresh", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            refresh_token: refresh_token,
            token_type: "Bearer",
          }),
        });

        if (!refreshResponse.ok) return redirectToLogin();

        const result = await refreshResponse.json();
        localStorage.setItem("access_token", result.access_token);
        localStorage.setItem("refresh_token", result.refresh_token);

        return loadProfile();
      }

      if (!response.ok) throw new Error(await response.text());
      const user = await response.json();
      setUserData(user);
    } catch (error) {
      alert("Failed to load profile: " + (error instanceof Error ? error.message : "Unknown error"));
      redirectToLogin();
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProfile();
  }, []);

  return (
    <div className="max-w-2xl mx-auto p-5">
      <h1 className="text-2xl font-bold">My Profile</h1>
      
      <div id="profile" className="mt-5 p-5 border border-gray-200 rounded">
        {loading ? (
          <p>Loading...</p>
        ) : userData ? (
          <>
            <p>
              <strong>Username:</strong> {userData.username}
            </p>
            <p>
              <strong>Email:</strong> {userData.email || "Not provided"}
            </p>
          </>
        ) : (
          <p>Failed to load profile data</p>
        )}
      </div>

      <div className="flex gap-3 mt-5">
        <button
          onClick={logout}
          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
        >
          Logout
        </button>
        <button
          onClick={manualRefresh}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Refresh Token
        </button>
      </div>
    </div>
  );
}