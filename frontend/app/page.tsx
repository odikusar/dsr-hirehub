"use client";

import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:18000";
type BackendStatus = "loading" | "ok" | "error";

export default function Home() {
  const [status, setStatus] = useState<BackendStatus>("loading");

  useEffect(() => {
    fetch(`${API_URL}/api/health/`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => setStatus(data.status === "ok" ? "ok" : "error"))
      .catch(() => setStatus("error"));
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4">
      <h1 className="text-3xl font-bold">JobMatch Lab</h1>
      <p>
        backend:{" "}
        <span
          className={
            status === "ok"
              ? "text-green-600"
              : status === "error"
                ? "text-red-600"
                : "text-gray-400"
          }
        >
          {status}
        </span>
      </p>
    </main>
  );
}
