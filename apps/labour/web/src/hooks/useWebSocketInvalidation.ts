import { useEffect } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { useWebSocket } from '../contexts/WebsocketContext';

type LabourEvent = {
  type: string;
  data: {
    labour_id?: string;
    contraction_id?: string;
    labour_update_id?: string;
    subscription_id?: string;
    subscriber_id?: string;
  };
};

function getQueryKeysForEvent(event: LabourEvent): string[][] {
  const { type, data } = event;

  switch (type) {
    case 'LabourPlanned':
      return [
        ['labour-v2', data.labour_id!],
        ['labour-v2', 'active'],
        ['labour-v2', 'history'],
      ];

    case 'LabourPlanUpdated':
      return [['labour-v2', data.labour_id!]];

    case 'LabourBegun':
      return [
        ['labour-v2', data.labour_id!],
        ['labour-updates-v2', data.labour_id!],
      ];

    case 'LabourCompleted':
      return [
        ['labour-v2', data.labour_id!],
        ['labour-v2', 'active'],
        ['labour-v2', 'history'],
      ];

    case 'LabourInviteSent':
      return [];

    case 'LabourDeleted':
      return [
        ['labour-v2', data.labour_id!],
        ['labour-v2', 'active'],
        ['labour-v2', 'history'],
      ];

    case 'ContractionStarted':
      return [
        ['contractions-v2', data.labour_id!],
        ['labour-v2', data.labour_id!],
      ];

    case 'ContractionEnded':
      return [['contractions-v2', data.labour_id!]];

    case 'ContractionUpdated':
      return [['contractions-v2', data.labour_id!]];

    case 'ContractionDeleted':
      return [['contractions-v2', data.labour_id!]];

    case 'LabourUpdatePosted':
      return [['labour-updates-v2', data.labour_id!]];

    case 'LabourUpdateMessageUpdated':
      return [['labour-updates-v2', data.labour_id!]];

    case 'LabourUpdateTypeUpdated':
      return [['labour-updates-v2', data.labour_id!]];

    case 'LabourUpdateDeleted':
      return [['labour-updates-v2', data.labour_id!]];

    case 'SubscriberRequested':
      return [['subscriptions-v2']];

    case 'SubscriberUnsubscribed':
      return [['subscriptions-v2']];

    case 'SubscriberNotificationMethodsUpdated':
      return [['subscriptions-v2', data.labour_id!]];

    case 'SubscriberAccessLevelUpdated':
      return [['subscriptions-v2']];

    case 'SubscriberApproved':
      return [['subscriptions-v2'], ['users-v2', data.labour_id!]];

    case 'SubscriberRemoved':
      return [['subscriptions-v2'], ['users-v2', data.labour_id!]];

    case 'SubscriberBlocked':
      return [['subscriptions-v2']];

    case 'SubscriberUnblocked':
      return [['subscriptions-v2']];

    case 'SubscriberRoleUpdated':
      return [['subscriptions-v2']];

    case 'SubscriptionTokenSet':
      return [['subscription-token-v2']];

    default:
      return [];
  }
}

export function useWebSocketInvalidation() {
  const queryClient = useQueryClient();
  const { subscribe } = useWebSocket();

  useEffect(() => {
    const unsubscribe = subscribe((message) => {
      const parsed = typeof message === 'string' ? JSON.parse(message) : message;
      const event = parsed as LabourEvent;
      const queryKeys = getQueryKeysForEvent(event);

      if (queryKeys.length > 0) {
        queryKeys.forEach((queryKey) => {
          queryClient.invalidateQueries({ queryKey });
        });
      }
    });

    return unsubscribe;
  }, [subscribe, queryClient]);
}
