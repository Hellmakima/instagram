"use client";

import { Input } from "@/components/atoms/input";
import { useState } from "react";

export default function LoginForm() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  return (
    <form className="flex flex-col gap-4">
      <div className="flex flex-col">
        <label htmlFor="username" className="font-semibold mb-1">
          Username or Email
        </label>
        <Input
          id="username"
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
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
        />
      </div>
    </form>
  );
}
