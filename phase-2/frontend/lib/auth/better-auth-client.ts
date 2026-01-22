// lib/auth/better-auth-client.ts
import { createAuthClient } from "better-auth/client";

export const auth = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000",
  // Note: plugins are typically configured on the server side, not client side
  // JWT plugin would be configured in the server-side auth setup
});

// Export the types for TypeScript
export type { Session } from "better-auth/types";