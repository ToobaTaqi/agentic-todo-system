// lib/auth/better-auth-client.ts
import { createAuth } from "better-auth";

export const auth = createAuth({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000",
  plugins: [
    // Enable JWT plugin as required by the constitution
    {
      $id: "jwt-plugin",
      client: {},
      server: {
        $context: (ctx) => ({
          secret: process.env.BETTER_AUTH_SECRET!,
        }),
      },
    },
  ],
  secret: process.env.BETTER_AUTH_SECRET,
  trustHost: true,
});

// Export the types for TypeScript
export type AuthSession = Awaited<ReturnType<typeof auth.api.getSession>>;