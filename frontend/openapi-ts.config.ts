import { defineConfig } from '@hey-api/openapi-ts';

export default defineConfig({
  client: 'legacy/axios',
  input: './openapi.json',
  output: './src/client',
  // exportSchemas: true,
  plugins: [
    {
      name: '@hey-api/sdk',
      // NOTE: this doesn't allow tree-shaking
      asClass: true,
      operationId: true,
      methodNameBuilder: (operation) => {
        // @ts-ignore
        let name: string = operation.name;
        return name.split('ApiV1')[0];
      },
    },
  ],
});
