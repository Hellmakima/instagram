// components/organisms/AuthFormClient.tsx
// AuthFormClient.tsx
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
import { toast } from "sonner";
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
    const payload: { [key: string]: string } = {};
    formData.forEach((value, key) => (payload[key] = value.toString()));

    try {
      const res = await typedPost<
        { message?: string; success?: boolean },
        { [key: string]: string }
      >(endpoint, payload, { headers: { "X-CSRF-Token": csrfToken || "" } });

      if (res.success) {
        toast.success(res.message || "Success!");
      } else {
        toast.error(res.message || "Something went wrong.");
      }
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
      toast.error(errorMessage);
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
