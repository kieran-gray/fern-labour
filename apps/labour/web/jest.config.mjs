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
    '\\.(gif|ttf|eot|svg|png)$': '<rootDir>/src/test/__mocks__/fileMock.js',
  },
  testMatch: [
    '<rootDir>/src/**/__tests__/**/*.{ts,tsx}',
    '<rootDir>/src/**/*.test.{ts,tsx}',
    '<rootDir>/src/**/*.spec.{ts,tsx}'
  ],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json'],
};