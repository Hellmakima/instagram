"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useRouter } from "next/navigation";

const loginSchema = z.object({
  username: z.string().min(3, "Username must be at least 3 characters"),
  password: z.string().min(4, "Password must be at least 4 characters"),
});

const registerSchema = z.object({
  username: z.string().min(3, "Username must be at least 3 characters"),
  password: z.string().min(4, "Password must be at least 4 characters"),
});

type LoginFormData = z.infer<typeof loginSchema>;
type RegisterFormData = z.infer<typeof registerSchema>;

export default function AuthPage() {
  const [activeTab, setActiveTab] = useState<"login" | "register">("login");
  const router = useRouter();

  const {
    register: loginRegister,
    handleSubmit: handleLoginSubmit,
    formState: { errors: loginErrors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const {
    register: registerRegister,
    handleSubmit: handleRegisterSubmit,
    formState: { errors: registerErrors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  const handleLogin = async (data: LoginFormData) => {
    try {
      const params = new URLSearchParams();
      params.append("username", data.username);
      params.append("password", data.password);

      const res = await fetch("http://localhost:5000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: params,
      });

      if (!res.ok) throw new Error(await res.text());
      
      const result = await res.json();
      localStorage.setItem("access_token", result.access_token);
      localStorage.setItem("refresh_token", result.refresh_token);
      router.push("/me");
    } catch (err) {
      alert("Login failed: " + (err instanceof Error ? err.message : "Unknown error"));
    }
  };

  const handleRegister = async (data: RegisterFormData) => {
    try {
      const res = await fetch("http://localhost:5000/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!res.ok) throw new Error(await res.text());
      
      const result = await res.json();
      localStorage.setItem("access_token", result.access_token);
      localStorage.setItem("refresh_token", result.refresh_token);
      router.push("/me");
    } catch (err) {
      alert("Registration failed: " + (err instanceof Error ? err.message : "Unknown error"));
    }
  };

  return (
    <div className="max-w-md mx-auto p-5">
      <div className="flex mb-5">
        <button
          className={`flex-1 py-2 ${activeTab === "login" ? "bg-blue-500 text-white" : "bg-gray-200"}`}
          onClick={() => setActiveTab("login")}
        >
          Login
        </button>
        <button
          className={`flex-1 py-2 ${activeTab === "register" ? "bg-blue-500 text-white" : "bg-gray-200"}`}
          onClick={() => setActiveTab("register")}
        >
          Register
        </button>
      </div>

      {activeTab === "login" ? (
        <form onSubmit={handleLoginSubmit(handleLogin)} className="flex flex-col gap-3">
          <h2 className="text-xl font-bold">Login</h2>
          <input
            {...loginRegister("username")}
            placeholder="Username"
            className="p-2 border rounded"
          />
          {loginErrors.username && (
            <p className="text-red-500 text-sm">{loginErrors.username.message}</p>
          )}
          <input
            type="password"
            {...loginRegister("password")}
            placeholder="Password"
            className="p-2 border rounded"
          />
          {loginErrors.password && (
            <p className="text-red-500 text-sm">{loginErrors.password.message}</p>
          )}
          <button type="submit" className="p-2 bg-blue-500 text-white rounded hover:bg-blue-600">
            Login
          </button>
        </form>
      ) : (
        <form onSubmit={handleRegisterSubmit(handleRegister)} className="flex flex-col gap-3">
          <h2 className="text-xl font-bold">Register</h2>
          <input
            {...registerRegister("username")}
            placeholder="Username"
            className="p-2 border rounded"
          />
          {registerErrors.username && (
            <p className="text-red-500 text-sm">{registerErrors.username.message}</p>
          )}
          <input
            type="password"
            {...registerRegister("password")}
            placeholder="Password"
            className="p-2 border rounded"
          />
          {registerErrors.password && (
            <p className="text-red-500 text-sm">{registerErrors.password.message}</p>
          )}
          <button type="submit" className="p-2 bg-blue-500 text-white rounded hover:bg-blue-600">
            Register
          </button>
        </form>
      )}
    </div>
  );
}