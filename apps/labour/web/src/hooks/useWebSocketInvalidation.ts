import { useEffect } from 'react';
import type { ContractionReadModel, LabourUpdateReadModel } from '@base/clients/labour_service';
import { useQueryClient } from '@tanstack/react-query';
import { useWebSocket } from '../contexts/WebsocketContext';
import { queryKeys } from './queryKeys';
import {
  prependToInfiniteQuery,
  removeFromInfiniteQuery,
  updateInfiniteQueryItem,
} from './useInfiniteQueries';

type LabourEventData = {
  labour_id?: string;
  contraction_id?: string;
  labour_update_id?: string;
  subscription_id?: string;
  subscriber_id?: string;
  contraction?: ContractionReadModel;
  labour_update?: LabourUpdateReadModel;
};

type LabourEvent = {
  type: string;
  data: LabourEventData;
};

function handleEvent(queryClient: ReturnType<typeof useQueryClient>, event: LabourEvent) {
  const { type, data } = event;

  switch (type) {
    case 'LabourPlanned':
      queryClient.invalidateQueries({ queryKey: queryKeys.labour.detail(data.labour_id!) });
      queryClient.invalidateQueries({ queryKey: queryKeys.labour.active(data.labour_id!) });
      queryClient.invalidateQueries({ queryKey: queryKeys.labour.lists() });
      break;

    case 'LabourPlanUpdated':
      queryClient.invalidateQueries({ queryKey: queryKeys.labour.detail(data.labour_id!) });
      break;

    case 'LabourBegun':
      queryClient.invalidateQueries({ queryKey: queryKeys.labour.detail(data.labour_id!) });
      queryClient.invalidateQueries({
        queryKey: queryKeys.labourUpdates.infinite(data.labour_id!),
      });
      break;

    case 'LabourCompleted':
      queryClient.invalidateQueries({ queryKey: queryKeys.labour.detail(data.labour_id!) });
      queryClient.invalidateQueries({ queryKey: queryKeys.labour.lists() });
      break;

    case 'LabourDeleted':
      queryClient.removeQueries({ queryKey: queryKeys.labour.detail(data.labour_id!) });
      queryClient.invalidateQueries({ queryKey: queryKeys.labour.lists() });
      break;

    case 'LabourInviteSent':
      break;

    case 'ContractionStarted':
      if (data.contraction) {
        prependToInfiniteQuery(
          queryClient,
          queryKeys.contractions.infinite(data.labour_id!),
          data.contraction,
          'contraction_id'
        );
      } else {
        queryClient.invalidateQueries({
          queryKey: queryKeys.contractions.infinite(data.labour_id!),
        });
      }
      queryClient.invalidateQueries({ queryKey: queryKeys.labour.detail(data.labour_id!) });
      break;

    case 'ContractionEnded':
      if (data.contraction) {
        updateInfiniteQueryItem(
          queryClient,
          queryKeys.contractions.infinite(data.labour_id!),
          data.contraction_id!,
          () => data.contraction!,
          'contraction_id'
        );
      } else {
        queryClient.invalidateQueries({
          queryKey: queryKeys.contractions.infinite(data.labour_id!),
        });
      }
      break;

    case 'ContractionUpdated':
      if (data.contraction) {
        updateInfiniteQueryItem(
          queryClient,
          queryKeys.contractions.infinite(data.labour_id!),
          data.contraction_id!,
          () => data.contraction!,
          'contraction_id'
        );
      } else {
        queryClient.invalidateQueries({
          queryKey: queryKeys.contractions.infinite(data.labour_id!),
        });
      }
      break;

    case 'ContractionDeleted':
      removeFromInfiniteQuery(
        queryClient,
        queryKeys.contractions.infinite(data.labour_id!),
        data.contraction_id!,
        'contraction_id'
      );
      break;

    case 'LabourUpdatePosted':
      if (data.labour_update) {
        prependToInfiniteQuery(
          queryClient,
          queryKeys.labourUpdates.infinite(data.labour_id!),
          data.labour_update,
          'labour_update_id'
        );
      } else {
        queryClient.invalidateQueries({
          queryKey: queryKeys.labourUpdates.infinite(data.labour_id!),
        });
      }
      break;

    case 'LabourUpdateMessageUpdated':
      if (data.labour_update) {
        updateInfiniteQueryItem(
          queryClient,
          queryKeys.labourUpdates.infinite(data.labour_id!),
          data.labour_update_id!,
          () => data.labour_update!,
          'labour_update_id'
        );
      } else {
        queryClient.invalidateQueries({
          queryKey: queryKeys.labourUpdates.infinite(data.labour_id!),
        });
      }
      break;

    case 'LabourUpdateTypeUpdated':
      if (data.labour_update) {
        updateInfiniteQueryItem(
          queryClient,
          queryKeys.labourUpdates.infinite(data.labour_id!),
          data.labour_update_id!,
          () => data.labour_update!,
          'labour_update_id'
        );
      } else {
        queryClient.invalidateQueries({
          queryKey: queryKeys.labourUpdates.infinite(data.labour_id!),
        });
      }
      break;

    case 'LabourUpdateDeleted':
      removeFromInfiniteQuery(
        queryClient,
        queryKeys.labourUpdates.infinite(data.labour_id!),
        data.labour_update_id!,
        'labour_update_id'
      );
      break;

    case 'SubscriberRequested':
    case 'SubscriberUnsubscribed':
    case 'SubscriberAccessLevelUpdated':
    case 'SubscriberBlocked':
    case 'SubscriberUnblocked':
    case 'SubscriberRoleUpdated':
      queryClient.invalidateQueries({ queryKey: queryKeys.subscriptions.all });
      queryClient.invalidateQueries({ queryKey: queryKeys.users.listByLabour(data.labour_id!) });
      break;

    case 'SubscriberNotificationMethodsUpdated':
      queryClient.invalidateQueries({
        queryKey: queryKeys.subscriptions.listByLabour(data.labour_id!),
      });
      queryClient.invalidateQueries({
        queryKey: ['subscriptions', 'userSubscription', data.labour_id],
      });
      break;

    case 'SubscriberApproved':
    case 'SubscriberRemoved':
      queryClient.invalidateQueries({ queryKey: queryKeys.subscriptions.all });
      queryClient.invalidateQueries({ queryKey: queryKeys.users.listByLabour(data.labour_id!) });
      break;

    case 'SubscriptionTokenSet':
      queryClient.invalidateQueries({ queryKey: queryKeys.subscriptionToken.all });
      break;

    default:
      break;
  }
}

export function useWebSocketInvalidation() {
  const queryClient = useQueryClient();
  const { subscribe } = useWebSocket();

  useEffect(() => {
    const unsubscribe = subscribe((message) => {
      const parsed = typeof message === 'string' ? JSON.parse(message) : message;
      const event = parsed as LabourEvent;
      handleEvent(queryClient, event);
    });

    return unsubscribe;
  }, [subscribe, queryClient]);
}
