import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-purple-200 via-pink-200 to-yellow-100 text-gray-800 font-sans px-6">
      <h1 className="text-6xl md:text-7xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-purple-600 mb-6">
        InstaClone
      </h1>
      <p className="text-lg md:text-xl mb-4 text-center">
        Check out the source code on{" "}
        <a
          href="https://github.com/hellmakima/instagram"
          className="text-blue-500 hover:text-blue-700 font-semibold transition-colors"
        >
          GitHub
        </a>
        .
      </p>
      <p className="text-lg md:text-xl mb-4">Other links:</p>
      <div className="flex flex-col md:flex-row gap-4">
        <Link
          href="/login"
          className="px-6 py-3 bg-white/80 backdrop-blur-md rounded-full shadow-lg text-lg font-medium hover:bg-white/100 transition"
        >
          Login
        </Link>
        <Link
          href="/register"
          className="px-6 py-3 bg-white/80 backdrop-blur-md rounded-full shadow-lg text-lg font-medium hover:bg-white/100 transition"
        >
          Register
        </Link>
      </div>
    </main>
  );
}
