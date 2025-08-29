/**
 * Centralized query key factory for React Query cache management
 * Provides consistent and type-safe query keys across the application
 */

export const queryKeys = {
  // Labour-related queries
  labour: {
    all: ['labour'] as const,
    user: (userId: string) => [...queryKeys.labour.all, userId] as const,
    active: (userId: string) => [...queryKeys.labour.user(userId), 'active'] as const,
    byId: (labourId: string) => [...queryKeys.labour.all, 'byId', labourId] as const,
    history: (userId: string) => [...queryKeys.labour.all, 'history', userId] as const,
  },

  // Subscription-related queries
  subscriptions: {
    all: ['subscriptions'] as const,
    subscriber: (userId: string) => [...queryKeys.subscriptions.all, 'subscriber', userId] as const,
    labour: (userId: string) => [...queryKeys.subscriptions.all, 'labour', userId] as const,
    byId: (subscriptionId: string, userId: string) =>
      [...queryKeys.subscriptions.all, 'byId', subscriptionId, userId] as const,
  },

  // Birthing person queries
  birthingPerson: {
    all: ['birthingPerson'] as const,
    user: (userId: string) => [...queryKeys.birthingPerson.all, userId] as const,
  },

  // Subscriber queries
  subscriber: {
    all: ['subscriber'] as const,
    user: (userId: string) => [...queryKeys.subscriber.all, userId] as const,
  },

  // Token/auth queries
  token: {
    all: ['token'] as const,
    user: (userId: string) => [...queryKeys.token.all, userId] as const,
  },

  // Contact form queries
  contact: {
    all: ['contact'] as const,
    form: ['contact', 'form'] as const,
  },
} as const;

// Type helpers for query key inference
export type QueryKeys = typeof queryKeys;
export type LabourKeys = typeof queryKeys.labour;
export type SubscriptionKeys = typeof queryKeys.subscriptions;
