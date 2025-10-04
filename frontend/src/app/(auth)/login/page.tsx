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

interface CsrfResponse {
  csrf_token: string;
}

export default function AuthPage() {
  const [csrfToken, setCsrfToken] = useState<string | null>(null);
  const [initialMessage, setInitialMessage] = useState<
    { text: string; type: "success" | "error" } | undefined
  >({
    text: "Loading...",
    type: "success",
  });

  useEffect(() => {
    const fetchCsrf = async () => {
      try {
        const res = await typedGet<{ data: CsrfResponse; message?: string }>(
          "/auth/csrf-token"
        );
        setCsrfToken(res.data.csrf_token);
        setInitialMessage({
          text: res.message || "Ready to log in.",
          type: "success",
        });
      } catch (err: any) {
        const errorText = err.response?.data?.message || err.message;
        setInitialMessage({
          text: `Failed to initialize form: ${errorText}`,
          type: "error",
        });
      }
    };

    fetchCsrf();
  }, []);

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
            <LoginFormClient
              csrfToken={csrfToken!}
              initialMessage={initialMessage}
            />
          </TabsContent>

          <TabsContent value="signup">
            <SignUpFormClient
              csrfToken={csrfToken!}
              initialMessage={initialMessage}
            />
          </TabsContent>
        </Tabs>
      </main>

      <Footer />
    </div>
  );
}
