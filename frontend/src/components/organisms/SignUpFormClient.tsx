// components/organisms/SignUpFormClient.tsx
import { AuthForm } from "./AuthFormClient";

interface SignUpFormClientProps {
  csrfToken: string;
}

export function SignUpFormClient({ csrfToken }: SignUpFormClientProps) {
  return (
    <AuthForm
      csrfToken={csrfToken}
      endpoint="/v1/auth/register"
      title="User Signup"
      description="Enter your credentials to create your account."
      fields={[
        { name: "username", label: "Username", placeholder: "your_handle" },
        {
          name: "email",
          label: "Email",
          placeholder: "your_handle@example.com",
        },
        {
          name: "password",
          label: "Password",
          type: "password",
          placeholder: "••••••••",
        },
      ]}
    />
  );
}
