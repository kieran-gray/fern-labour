export default {
  preset: 'ts-jest/presets/default-esm',
  testEnvironment: 'node',
  extensionsToTreatAsEsm: ['.ts'],
  globals: {
    'ts-jest': {
      useESM: true
    }
  },
  roots: ['./src'],
  testMatch: ['**/__tests__/**/*.ts', '**/?(*.)+(spec|Test).ts'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
  ],
  moduleNameMapper: {
    '^@base/(.*)$': '<rootDir>/src/$1',
    '^@shared/(.*)$': '<rootDir>/src/shared-components/$1',
    '^@clients/(.*)$': '<rootDir>/src/clients/$1',
    '^@labour/(.*)$': '<rootDir>/src/pages/Labour/$1',
    '^@subscription/(.*)$': '<rootDir>/src/pages/Subscription/$1',
    '^@subscribe/(.*)$': '<rootDir>/src/pages/Subscribe/$1',
    '^@subscriptions/(.*)$': '<rootDir>/src/pages/Subscriptions/$1',
  },
};