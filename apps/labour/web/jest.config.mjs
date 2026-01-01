export default {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/test/setup.ts'],
  moduleNameMapper: {
    '^@base/(.*)$': '<rootDir>/src/$1',
    '^@shared/(.*)$': '<rootDir>/src/shared-components/$1',
    '^@clients/(.*)$': '<rootDir>/src/clients/$1',
    '^@labour/(.*)$': '<rootDir>/src/pages/Labour/$1',
    '^@subscription/(.*)$': '<rootDir>/src/pages/Subscription/$1',
    '^@subscribe/(.*)$': '<rootDir>/src/pages/Subscribe/$1',
    '^@subscriptions/(.*)$': '<rootDir>/src/pages/Subscriptions/$1',
    '^@lib/(.*)$': '<rootDir>/src/lib/$1',
  },
  testMatch: [
    '<rootDir>/src/**/__tests__/**/*.{ts,tsx}',
    '<rootDir>/src/**/*.test.{ts,tsx}',
    '<rootDir>/src/**/*.spec.{ts,tsx}'
  ],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json'],
  globals: {
    'import.meta': {
      env: {
        VITE_CONTACT_SERVICE_URL: 'http://localhost:3000',
        VITE_API_URL: 'http://localhost:3000',
        VITE_LABOUR_SERVICE_URL: 'http://localhost:3001',
      }
    }
  },
};