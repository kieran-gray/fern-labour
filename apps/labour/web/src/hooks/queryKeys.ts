/**
 * Centralized query key factory for React Query cache management
 * Provides consistent and type-safe query keys across the application
 *
 * Key structure follows the pattern:
 * - [domain] - top level for broad invalidation
 * - [domain, 'list', ...filters] - for list queries (including infinite)
 * - [domain, 'detail', ...ids] - for single entity queries
 *
 */

export const queryKeysV2 = {
  labour: {
    all: ['labour'] as const,
    lists: () => [...queryKeysV2.labour.all, 'list'] as const,
    list: (filters: { userId?: string; status?: string }) =>
      [...queryKeysV2.labour.lists(), filters] as const,
    details: () => [...queryKeysV2.labour.all, 'detail'] as const,
    detail: (labourId: string) => [...queryKeysV2.labour.details(), labourId] as const,
    history: (userId: string) =>
      [...queryKeysV2.labour.lists(), { userId, type: 'history' }] as const,
    active: (userId: string) => [...queryKeysV2.labour.all, 'active', userId] as const,
  },

  contractions: {
    all: ['contractions'] as const,
    lists: () => [...queryKeysV2.contractions.all, 'list'] as const,
    list: (labourId: string) => [...queryKeysV2.contractions.lists(), labourId] as const,
    infinite: (labourId: string) =>
      [...queryKeysV2.contractions.all, 'infinite', labourId] as const,
    details: () => [...queryKeysV2.contractions.all, 'detail'] as const,
    detail: (labourId: string, contractionId: string) =>
      [...queryKeysV2.contractions.details(), labourId, contractionId] as const,
  },

  labourUpdates: {
    all: ['labourUpdates'] as const,
    lists: () => [...queryKeysV2.labourUpdates.all, 'list'] as const,
    list: (labourId: string) => [...queryKeysV2.labourUpdates.lists(), labourId] as const,
    infinite: (labourId: string) =>
      [...queryKeysV2.labourUpdates.all, 'infinite', labourId] as const,
    details: () => [...queryKeysV2.labourUpdates.all, 'detail'] as const,
    detail: (labourId: string, labourUpdateId: string) =>
      [...queryKeysV2.labourUpdates.details(), labourId, labourUpdateId] as const,
  },

  subscriptionToken: {
    all: ['subscriptionToken'] as const,
    detail: (labourId: string) =>
      [...queryKeysV2.subscriptionToken.all, 'detail', labourId] as const,
  },

  subscriptions: {
    all: ['subscriptions'] as const,
    lists: () => [...queryKeysV2.subscriptions.all, 'list'] as const,
    listByLabour: (labourId: string) =>
      [...queryKeysV2.subscriptions.lists(), { labourId }] as const,
    listByUser: (userId: string) => [...queryKeysV2.subscriptions.lists(), { userId }] as const,
    details: () => [...queryKeysV2.subscriptions.all, 'detail'] as const,
    detail: (labourId: string, subscriptionId: string) =>
      [...queryKeysV2.subscriptions.details(), labourId, subscriptionId] as const,
    userSubscription: (labourId: string, userId: string) =>
      [...queryKeysV2.subscriptions.all, 'userSubscription', labourId, userId] as const,
  },

  users: {
    all: ['users'] as const,
    lists: () => [...queryKeysV2.users.all, 'list'] as const,
    listByLabour: (labourId: string) => [...queryKeysV2.users.lists(), labourId] as const,
  },
} as const;

export type QueryKeys = typeof queryKeysV2;
export type LabourKeys = typeof queryKeysV2.labour;
export type ContractionKeys = typeof queryKeysV2.contractions;
export type LabourUpdateKeys = typeof queryKeysV2.labourUpdates;
export type SubscriptionKeys = typeof queryKeysV2.subscriptions;
