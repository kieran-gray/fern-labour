import { useMutation, UseMutationOptions, UseMutationResult } from '@tanstack/react-query';
import { EventType, OutboxManager } from '../storage/outbox';
import { offlineLogger } from '../utils/logger';
import { useGuestMode } from './useGuestMode';
import { useSyncEngine } from './useSyncEngine';

interface OfflineMutationOptions<TData, TError, TVariables>
  extends Omit<UseMutationOptions<TData, TError, TVariables>, 'mutationFn'> {
  /**
   * The event type for outbox queueing
   */
  eventType: EventType;

  /**
   * Extract aggregate ID from variables or data
   */
  getAggregateId: (variables: TVariables) => string;

  /**
   * The actual mutation function to execute online
   */
  mutationFn: (variables: TVariables) => Promise<TData>;

  /**
   * Optional: Custom payload extraction for outbox
   * Defaults to using variables as payload
   */
  getPayload?: (variables: TVariables) => unknown;

  /**
   * Optional: Skip outbox queueing (for read-only operations)
   * Defaults to false
   */
  skipOutbox?: boolean;
}

/**
 * Enhanced mutation hook that automatically handles offline queueing
 * Preserves existing optimistic update behavior while adding event sourcing
 */
export function useOfflineMutation<TData, TError = Error, TVariables = void>(
  options: OfflineMutationOptions<TData, TError, TVariables>
): UseMutationResult<TData, TError, TVariables> {
  const { isGuestMode } = useGuestMode();
  const { triggerSync } = useSyncEngine();

  const {
    eventType,
    getAggregateId,
    mutationFn,
    getPayload = (variables) => variables,
    skipOutbox = false,
    onMutate,
    onSuccess,
    onError,
    onSettled,
    ...mutationOptions
  } = options;

  return useMutation<TData, TError, TVariables>({
    ...mutationOptions,

    mutationFn: async (variables: TVariables) => {
      const aggregateId = getAggregateId(variables);
      const payload = getPayload(variables);
      let addedEventId: string | null = null;

      if (!skipOutbox) {
        const evt = await OutboxManager.addEvent(aggregateId, eventType, payload, isGuestMode);
        addedEventId = evt.id;
        offlineLogger.info('mutation:queued', { eventType, aggregateId, isGuestMode, payload });
      }

      if (navigator.onLine && !isGuestMode) {
        try {
          const result = await mutationFn(variables);
          if (addedEventId) {
            await OutboxManager.markEventSynced(addedEventId);
          }
          triggerSync();
          offlineLogger.info('mutation:executed', { eventType, aggregateId });
          return result;
        } catch (err) {
          triggerSync();
          offlineLogger.warn('mutation:onlineError', {
            eventType,
            aggregateId,
            error: String(err),
          });
          if (err instanceof Error) {
            throw err;
          }
          throw new Error(String(err));
        }
      }
      if (!isGuestMode) {
        triggerSync();
      }
      offlineLogger.info('mutation:offlineOrGuest', { eventType, aggregateId, isGuestMode });
      return null as TData;
    },

    onMutate: async (variables: TVariables) => {
      if (onMutate) {
        return await onMutate(variables);
      }
    },

    onSuccess: (data: TData, variables: TVariables, context: unknown) => {
      if (onSuccess) {
        onSuccess(data, variables, context);
      }
    },

    onError: (error: TError, variables: TVariables, context: unknown) => {
      if (onError) {
        onError(error, variables, context);
      }
    },

    onSettled: (
      data: TData | undefined,
      error: TError | null,
      variables: TVariables,
      context: unknown
    ) => {
      if (onSettled) {
        onSettled(data, error, variables, context);
      }
      triggerSync();
    },
  });
}

/**
 * Helper hook for mutations that don't need offline queueing
 * Just wraps the regular useMutation with consistent patterns
 */
export function useOnlineMutation<TData, TError = Error, TVariables = void>(
  options: UseMutationOptions<TData, TError, TVariables>
): UseMutationResult<TData, TError, TVariables> {
  const { triggerSync } = useSyncEngine();

  return useMutation<TData, TError, TVariables>({
    ...options,
    onSettled: (data, error, variables, context) => {
      if (options.onSettled) {
        options.onSettled(data, error, variables, context);
      }
      triggerSync();
    },
  });
}
