"use client";

import { useRouter } from "next/navigation";
import { Button } from "@/components/atoms/button";
import LoginForm from "./components/LoginForm";

export default function LoginPage() {
  const router = useRouter();

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
      <div className="w-full max-w-md space-y-4">
        <Button variant="default" onClick={() => router.back()}>
          Back
        </Button>
        <LoginForm />
      </div>
    </main>
  );
}
