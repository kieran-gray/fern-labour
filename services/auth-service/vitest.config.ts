import { defineWorkersConfig } from "@cloudflare/vitest-pool-workers/config";

export default defineWorkersConfig(async () => {
  return {
    test: {
      poolOptions: {
        workers: {
          wrangler: { configPath: "./wrangler.jsonc" },
          miniflare: {
            bindings: {
              ENVIRONMENT: "test",
              ALLOWED_ORIGINS: "http://localhost:5173,http://localhost:5174,http://localhost:5175",
              AUTH_ISSUER_URL: "https://fernlabour.uk.auth0.com/",
              AUTH_JWKS_PATH: ".well-known/jwks.json",
            },
            kvNamespaces: {
              AUTH_JWKS_CACHE: "test-jwks-cache"
            },
          },
        },
      },
    },
  };
});