"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
// import { TestComponent } from "./sandbox/testComponent"

type BackendStatus = "loading" | "ok" | "error";

export default function Home() {
  const [status, setStatus] = useState<BackendStatus>("loading");

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
