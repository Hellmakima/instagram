import LoginForm from "./components/LoginForm";

export default function LoginPage() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
      <div className="w-full max-w-md">
        <LoginForm />
      </div>
    </main>
  );
}
