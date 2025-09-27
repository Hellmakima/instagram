"use client";

import { useState, useEffect } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import Message from "./Message";
import api from "@/lib/api";

export default function AuthForm() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [csrfToken, setCsrfToken] = useState<string | null>(null);
  const [message, setMessage] = useState<{
    text: string;
    type: "success" | "error";
  } | null>(null);

  useEffect(() => {
    const fetchCsrfToken = async () => {
      try {
        const res = await api.get("/auth/csrf-token");
        setCsrfToken(res.data.data.csrf_token);
        setMessage({
          text: res.data.message || "CSRF token ready.",
          type: "success",
        });
      } catch (err: any) {
        setMessage({
          text: `Failed to fetch CSRF token: ${err.message}`,
          type: "error",
        });
      }
    };
    fetchCsrfToken();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!csrfToken) {
      setMessage({
        text: "CSRF token not available. Refresh the page.",
        type: "error",
      });
      return;
    }

    try {
      const res = await api.post(
        "/auth/login",
        { username_or_email: username, password },
        { headers: { "X-CSRF-Token": csrfToken } }
      );

      setMessage({
        text: res.data.message || "Login successful!",
        type: "success",
      });
    } catch (err: any) {
      setMessage({
        text:
          err.response?.data?.detail?.message ||
          err.response?.data?.message ||
          err.message,
        type: "error",
      });
    }
  };

  return (
    <div className="bg-white p-8 rounded-xl shadow-lg">
      <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">
        User Login
      </h2>
      {message && <Message type={message.type}>{message.text}</Message>}
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div className="flex flex-col">
          <label htmlFor="username" className="font-semibold mb-1">
            Username or Email
          </label>
          <Input
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full"
          />
        </div>
        <div className="flex flex-col">
          <label htmlFor="password" className="font-semibold mb-1">
            Password
          </label>
          <Input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full"
          />
        </div>
        <Button type="submit" className="w-full">
          Login
        </Button>
      </form>
    </div>
  );
}
