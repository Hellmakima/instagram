// components/organisms/AuthFormClient.tsx
"use client";

import { useState } from "react";
import { authRequest } from "@/lib/api/authApi";
import { Input } from "@/components/atoms/input";
import { Button } from "@/components/atoms/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/atoms/card";
import { toast } from "sonner";
import { Terminal } from "lucide-react";

interface Field {
  name: string;
  label: string;
  type?: "text" | "email" | "password";
  placeholder?: string;
}

interface AuthFormProps {
  csrfToken: string | null;
  endpoint: string; // e.g., "/login" or "/register"
  title: string;
  description: string;
  fields: Field[];
}

export function AuthForm({
  csrfToken,
  endpoint,
  title,
  description,
  fields,
}: AuthFormProps) {
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData(e.currentTarget);
    const payload: Record<string, string> = {};
    formData.forEach((value, key) => {
      payload[key] = value.toString();
    });

    try {
      const res = await authRequest<
        { message?: string; success?: boolean },
        typeof payload
      >("POST", endpoint, payload, {
        headers: { "X-CSRF-Token": csrfToken || "" },
      });

      if (res.success) {
        toast.success(res.message || "Success!");
      } else {
        toast.error(res.message || "Something went wrong.");
      }
    } catch (err: any) {
      let errorMessage = "An unknown error occurred";

      // BackendApiError (your custom error)
      if (err?.serverResponse) {
        const serverErr = err.serverResponse;

        if (Array.isArray((serverErr.error as any)?.details)) {
          // Pydantic validation errors
          const details = (serverErr.error as any).details as Array<{
            loc?: any[];
            msg?: string;
          }>;
          errorMessage = details
            .map((d) => {
              const fieldPath = Array.isArray(d.loc)
                ? d.loc.slice(1).join(".") // skip "body"
                : d.loc;
              return fieldPath ? `${fieldPath}: ${d.msg}` : d.msg;
            })
            .join("; ");
        } else if (serverErr.message) {
          errorMessage = serverErr.message;
        }
      }
      // Axios fallback
      else if (err?.response?.data) {
        const data = err.response.data;
        if (Array.isArray(data.detail)) {
          errorMessage = data.detail
            .map((d: any) => {
              const fieldPath = Array.isArray(d.loc)
                ? d.loc.slice(1).join(".")
                : d.loc;
              return fieldPath ? `${fieldPath}: ${d.msg}` : d.msg;
            })
            .join("; ");
        } else if (data.message) {
          errorMessage = data.message;
        }
      }
      // Generic JS error
      else if (err.message) {
        errorMessage = err.message;
      }

      toast.error(errorMessage);
      console.error("AuthForm error:", err);
    } finally {
      setLoading(false);
    }
  };

  if (!csrfToken) {
    return (
      <div className="flex justify-center items-center w-full p-4">
        <Terminal className="h-6 w-6 mr-2 animate-spin" />
        <span>Loading CSRF token...</span>
      </div>
    );
  }

  return (
    <Card className="w-[400px] shadow-lg">
      <CardHeader className="text-center">
        <CardTitle className="text-2xl">{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent>
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

          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? "Submitting..." : title}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
