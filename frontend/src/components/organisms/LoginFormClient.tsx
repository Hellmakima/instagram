// components/organisms/LoginFormClient.tsx
import { AuthForm } from "./AuthFormClient";

interface LoginFormClientProps {
  csrfToken: string;
}

export function LoginFormClient({ csrfToken }: LoginFormClientProps) {
  return (
    <AuthForm
      csrfToken={csrfToken}
      endpoint="/auth/login"
      title="User Login"
      description="Enter your credentials to access your account."
      fields={[
        {
          name: "username_or_email",
          label: "Username or Email",
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
