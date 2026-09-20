"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
// import { TestComponent } from "./sandbox/testComponent"
import { useAuth } from "@/hooks/useAuth";

type BackendStatus = "loading" | "ok" | "error";

export default function Home() {
  const [status, setStatus] = useState<BackendStatus>("loading");

  const { user, isAuthenticated } = useAuth();

  useEffect(() => {
  api
      .get<{ status: string }>("/api/health/")
      .then((data) => {
        setStatus(data.status === "ok" ? "ok" : "error");
      })
      .catch(() => setStatus("error"));
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4">
      <p>{isAuthenticated ? `Hello, ${user!.email}` : "anonymous"}</p>
      {/* <TestComponent></TestComponent> */}
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
