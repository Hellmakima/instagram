// app/(auth)/login/page.tsx
"use client";

import { useEffect, useState } from "react";
import { typedGet } from "@/lib/api";
import { LoginFormClient } from "@/components/organisms/LoginFormClient";
import { SignUpFormClient } from "@/components/organisms/SignUpFormClient";
import { Header } from "@/components/organisms/Header";
import { Footer } from "@/components/organisms/Footer";
import {
  Tabs,
  TabsList,
  TabsTrigger,
  TabsContent,
} from "@/components/atoms/tabs"; // shadcn Tabs
import { toast } from "sonner";

interface CsrfResponse {
  csrf_token: string;
}

export default function AuthPage() {
  const [csrfToken, setCsrfToken] = useState<string | null>(null);

  useEffect(() => {
    const fetchCsrf = async () => {
      try {
        const res = await typedGet<{ data: CsrfResponse; message?: string }>(
          "/auth/csrf-token"
        );
        setCsrfToken(res.data.csrf_token);
        toast.success(res.message || "Ready to log in.");
      } catch (err: any) {
        console.error("Failed to fetch CSRF token:", err);
        toast.error(`Failed to initialize form: ${err.message}`);
      }
    };

    fetchCsrf();
  }, []);

  if (!csrfToken) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen bg-background">
      <Header />

      <main className="flex-1 flex flex-col items-center justify-center p-4">
        <Tabs defaultValue="login" className="w-[400px]">
          <TabsList>
            <TabsTrigger value="login">Login</TabsTrigger>
            <TabsTrigger value="signup">Signup</TabsTrigger>
          </TabsList>

          <TabsContent value="login">
            <LoginFormClient csrfToken={csrfToken} />
          </TabsContent>

          <TabsContent value="signup">
            <SignUpFormClient csrfToken={csrfToken} />
          </TabsContent>
        </Tabs>
      </main>

      <Footer />
    </div>
  );
}
