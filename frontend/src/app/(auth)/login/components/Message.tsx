"use client";

interface MessageProps {
  type: "success" | "error";
  children: React.ReactNode;
}

export default function Message({ type, children }: MessageProps) {
  return (
    <div
      className={`mb-4 p-3 rounded ${
        type === "success"
          ? "bg-green-100 text-green-800 border border-green-300"
          : "bg-red-100 text-red-800 border border-red-300"
      }`}
    >
      {children}
    </div>
  );
}
