// components/organisms/AuthFormClient.tsx
"use client";

import { useState } from "react";
import { typedPost } from "@/lib/api";
import { Input } from "@/components/atoms/input";
import { Button } from "@/components/atoms/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/atoms/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/atoms/alert";
import { Terminal, CheckCircle } from "lucide-react";

interface Field {
  name: string;
  label: string;
  type?: "text" | "email" | "password";
  placeholder?: string;
}

interface AuthFormProps {
  csrfToken: string | null;
  endpoint: string;
  title: string;
  description: string;
  fields: Field[];
  initialMessage?: { text: string; type: "success" | "error" } | null;
}

export function AuthForm({
  csrfToken,
  endpoint,
  title,
  description,
  fields,
  initialMessage,
}: AuthFormProps) {
  const [message, setMessage] = useState(initialMessage || null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    const formData = new FormData(e.currentTarget);
    const payload: { [key: string]: string } = {};
    formData.forEach((value, key) => (payload[key] = value.toString()));

    try {
      const res = await typedPost<
        { message?: string; success?: boolean },
        { [key: string]: string }
      >(endpoint, payload, { headers: { "X-CSRF-Token": csrfToken || "" } });

      setMessage({
        text: res.message || "Success!",
        type: res.success ? "success" : "error",
      });
    } catch (err: any) {
      let errorMessage = "An unknown error occurred";
      let statusCode = err.response?.status;

      if (err.response?.data?.detail) {
        const detail = err.response.data.detail;

        if (Array.isArray(detail)) {
          errorMessage = detail
            .map((d) => {
              if (d.msg && d.loc) {
                const field = Array.isArray(d.loc)
                  ? d.loc.slice(1).join(".")
                  : d.loc;
                return `${field}: ${d.msg}`;
              }
              return JSON.stringify(d);
            })
            .join("; ");
        } else if (typeof detail === "object") {
          errorMessage =
            detail.message || detail.error?.details || errorMessage;
        }
      } else if (err.response?.data?.message) {
        errorMessage = err.response.data.message;
      } else {
        errorMessage = err.message;
      }

      setMessage({
        text: `Error ${statusCode}: ${errorMessage}`,
        type: "error",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-[400px] shadow-lg">
      <CardHeader className="text-center">
        <CardTitle className="text-2xl">{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent>
        {message && (
          <Alert
            variant={message.type === "error" ? "destructive" : "default"}
            className="mb-4"
          >
            {message.type === "error" ? (
              <Terminal className="h-4 w-4" />
            ) : (
              <CheckCircle className="h-4 w-4" />
            )}
            <AlertTitle>
              {message.type === "error" ? "Error" : "Status"}
            </AlertTitle>
            <AlertDescription>{message.text}</AlertDescription>
          </Alert>
        )}

        {!csrfToken && (
          <Alert variant="destructive" className="mb-4">
            <Terminal className="h-4 w-4" />
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>
              CSRF token missing. Cannot submit form.
            </AlertDescription>
          </Alert>
        )}

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input type="hidden" name="csrfToken" value={csrfToken || ""} />
          {fields.map((field) => (
            <div className="flex flex-col space-y-1" key={field.name}>
              <label htmlFor={field.name}>{field.label}</label>
              <Input
                id={field.name}
                name={field.name}
                type={field.type || "text"}
                placeholder={field.placeholder}
                required
              />
            </div>
          ))}

          <Button
            type="submit"
            className="w-full"
            disabled={loading || !csrfToken}
          >
            {loading ? "Submitting..." : title}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
