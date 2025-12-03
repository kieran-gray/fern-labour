import { defineWorkersConfig, readD1Migrations } from "@cloudflare/vitest-pool-workers/config";

export default defineWorkersConfig(async () => {
  const migrations = await readD1Migrations("./migrations");

  return {
    test: {
      poolOptions: {
        workers: {
          wrangler: { configPath: "./wrangler.jsonc" },
          miniflare: {
            bindings: {
              ENVIRONMENT: "test",
              CLOUDFLARE_SITEVERIFY_URL: "https://test.fernlabour.com/turnstile/v0/siteverify",
              CLOUDFLARE_SECRET_KEY: "test-secret-key",
              ALLOWED_ORIGINS: "http://localhost:5173,http://localhost:5174,http://localhost:5175",
              TEST_MIGRATIONS: migrations,
            },
            d1Databases: {
              DB: "test-db"
            },
            workers: [
              {
                name: "fern-labour-auth-service-worker",
                modules: [
                  {
                    path: "index.js",
                    type: "ESModule",
                    contents: `
                      export default {
                        async fetch(request) {
                          const body = await request.json();
                          const token = body.token;

                          if (token.includes("SUCCESS")) {
                            return Response.json({ user_id: "test-user-123", valid: true });
                          }

                          return Response.json({ error: "Unauthorised" }, { status: 401 });
                        }
                      }
                    `,
                  },
                ],
                compatibilityDate: "2025-10-01",
              },
            ],
          },
        },
      },
    },
  };
});