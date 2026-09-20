import { api } from "@/lib/api";
import type { User } from "@/lib/types";

export type LoginPayload = { email: string; password: string };

export const authApi = {
  me: () => api.get<User>("/api/auth/me/"),
  login: (payload: LoginPayload) => api.post<User>("/api/auth/login/", payload),
  logout: () => api.post<void>("/api/auth/logout/"),
};
