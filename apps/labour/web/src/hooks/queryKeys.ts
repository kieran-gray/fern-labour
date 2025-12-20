/**
 * Centralized query key factory for React Query cache management
 * Provides consistent and type-safe query keys across the application
 */

export const queryKeysV2 = {
  labour: {
    all: ['labour-v2'] as const,
    byId: (labourId: string) => [...queryKeysV2.labour.all, labourId] as const,
    history: (userId: string) => [...queryKeysV2.labour.all, 'history', userId] as const,
    active: (userId: string) => [...queryKeysV2.labour.all, 'active', userId] as const,
  },
  contractions: {
    all: ['contractions-v2'] as const,
    byLabour: (labourId: string) => [...queryKeysV2.contractions.all, labourId] as const,
    paginated: (labourId: string, cursor: string | null) =>
      [...queryKeysV2.contractions.byLabour(labourId), 'paginated', cursor] as const,
    byId: (labourId: string, contractionId: string) =>
      [...queryKeysV2.contractions.byLabour(labourId), contractionId] as const,
  },
  labourUpdates: {
    all: ['labour-updates-v2'] as const,
    byLabour: (labourId: string) => [...queryKeysV2.labourUpdates.all, labourId] as const,
    paginated: (labourId: string, cursor: string | null) =>
      [...queryKeysV2.labourUpdates.byLabour(labourId), 'paginated', cursor] as const,
    byId: (labourId: string, labourUpdateId: string) =>
      [...queryKeysV2.labourUpdates.byLabour(labourId), labourUpdateId] as const,
  },
  subscriptionToken: {
    all: ['subscription-token-v2'] as const,
    byLabour: (labourId: string) => [...queryKeysV2.subscriptionToken.all, labourId] as const,
  },
  subscriptions: {
    all: ['subscriptions-v2'] as const,
    byLabour: (labourId: string) => [...queryKeysV2.subscriptions.all, labourId] as const,
    byUser: (userId: string) => [...queryKeysV2.subscriptions.all, userId] as const,
    byLabourAndUser: (labourId: string, userId: string) =>
      [...queryKeysV2.subscriptions.all, labourId, userId] as const,
    paginated: (labourId: string, cursor: string | null) =>
      [...queryKeysV2.subscriptions.byLabour(labourId), 'paginated', cursor] as const,
    byId: (labourId: string, subscriptionId: string) =>
      [...queryKeysV2.subscriptions.byLabour(labourId), subscriptionId] as const,
  },
  users: {
    all: ['users-v2'] as const,
    byLabour: (labourId: string) => [...queryKeysV2.users.all, labourId] as const,
  },
} as const;

export type QueryKeys = typeof queryKeysV2;
export type LabourKeys = typeof queryKeysV2.labour;
export type SubscriptionKeys = typeof queryKeysV2.subscriptions;
