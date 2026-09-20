// Fetch wrapper: base URL, JSON, cookies, auto-refresh on 401 (the "interceptor").
const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:18000";

// DRF error responses land here: err.status + err.data ({"detail": ...} or field errors).
export class ApiError extends Error {
  constructor(
    public status: number,
    public data: unknown,
  ) {
    super(`API error ${status}`);
  }
}

async function rawFetch(path: string, options: RequestInit = {}): Promise<Response> {
  return fetch(`${API_URL}${path}`, {
    ...options,
    credentials: "include", // attach cookies cross-origin — pairs with CORS_ALLOW_CREDENTIALS
    headers: { "Content-Type": "application/json", ...options.headers },
  });
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  let res = await rawFetch(path, options);

  // Interceptor: access expired -> try refresh ONCE, then retry the original request.
  // Auth endpoints are excluded (a failed login must not trigger refresh).
  if (res.status === 401 && !path.startsWith("/api/auth/")) {
    const refreshed = await rawFetch("/api/auth/refresh/", { method: "POST" });
    if (refreshed.ok) {
      res = await rawFetch(path, options); // new access cookie is already set
    }
  }

  if (!res.ok) {
    throw new ApiError(res.status, await res.json().catch(() => null));
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, body?: unknown) =>
    request<T>(path, { method: "POST", body: body === undefined ? undefined : JSON.stringify(body) }),
  patch: <T>(path: string, body: unknown) =>
    request<T>(path, { method: "PATCH", body: JSON.stringify(body) }),
  delete: <T>(path: string) => request<T>(path, { method: "DELETE" }),
};
