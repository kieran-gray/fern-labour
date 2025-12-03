import { createClient } from '@hey-api/openapi-ts';

const services = {
  labour_service: 'http://localhost:8000/openapi.json',
  // contact_service: 'http://localhost:8002/openapi.json',
};

Object.entries(services).forEach(([serviceName, url]) => {
  createClient({
    client: 'legacy/axios',
    input: url,
    output: {
      path: `./src/clients/${serviceName}`,
      format: 'prettier',
      lint: 'eslint',
    },
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
});
