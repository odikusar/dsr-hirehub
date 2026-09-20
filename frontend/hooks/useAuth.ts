"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { authApi } from "@/lib/auth-api";

// Custom hook = a plain function that composes other hooks (Angular: AuthService).
// Every component calling useAuth() SUBSCRIBES to the ["me"] cache entry:
// when it changes (login/logout/refetch), all subscribers re-render automatically.
export function useAuth() {
  const { data: user, isLoading } = useQuery({
    // queryKey — the cache address. All useQuery(["me"]) across the app share
    // ONE cache entry and ONE request (deduplication).
    queryKey: ["me"],
    // queryFn — how to fetch when the cache is empty or stale.
    queryFn: authApi.me,
    // 401 from /me is a normal "not logged in", not a flaky error — don't retry.
    retry: false,
    // Fresh for 5 min: remounts within that window read cache, no request.
    staleTime: 5 * 60_000,
  });

  return {
    user: user ?? null, // undefined (no data) -> null for a cleaner contract
    isLoading,
    isAuthenticated: !!user,
  };
}

// Mutations = write operations (POST/...). They don't touch the cache by
// themselves — onSuccess says what to do with the result.
export function useLogin() {
  // useQueryClient — direct handle to the app-wide cache (from Providers).
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: authApi.login,
    // Login response body IS the user — write it into ["me"] directly
    // (setQueryData) instead of refetching /me. Subscribers re-render instantly.
    onSuccess: (user) => queryClient.setQueryData(["me"], user),
  });
}

export function useLogout() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: authApi.logout,
    // Cookies are already cleared by the server; drop the cached user too.
    onSuccess: () => queryClient.setQueryData(["me"], null),
  });
}

// Usage in a component:
//   const { user, isAuthenticated, isLoading } = useAuth();
//   const login = useLogin();
//   login.mutate({ email, password });  // login.isPending / login.error for UI
