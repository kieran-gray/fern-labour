import { useEffect } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { useWebSocket } from '../contexts/WebsocketContext';

type LabourEvent = {
  LabourPlanned?: { labour_id: string };
  LabourPlanUpdated?: { labour_id: string };
  LabourBegun?: { labour_id: string };
  LabourCompleted?: { labour_id: string };
  LabourInviteSent?: { labour_id: string };
  LabourDeleted?: { labour_id: string };
  ContractionStarted?: { labour_id: string; contraction_id: string };
  ContractionEnded?: { labour_id: string; contraction_id: string };
  ContractionUpdated?: { labour_id: string; contraction_id: string };
  ContractionDeleted?: { labour_id: string; contraction_id: string };
  LabourUpdatePosted?: { labour_id: string; labour_update_id: string };
  LabourUpdateMessageUpdated?: { labour_id: string; labour_update_id: string };
  LabourUpdateTypeUpdated?: { labour_id: string; labour_update_id: string };
  LabourUpdateDeleted?: { labour_id: string; labour_update_id: string };
  SubscriberRequested?: { labour_id: string; subscription_id: string };
  SubscriberUnsubscribed?: { labour_id: string; subscription_id: string };
  SubscriberNotificationMethodsUpdated?: { labour_id: string; subscription_id: string };
  SubscriberAccessLevelUpdated?: { labour_id: string; subscription_id: string };
  SubscriberApproved?: { labour_id: string; subscription_id: string };
  SubscriberRemoved?: { labour_id: string; subscription_id: string };
  SubscriberBlocked?: { labour_id: string; subscription_id: string };
  SubscriberUnblocked?: { labour_id: string; subscription_id: string };
  SubscriberRoleUpdated?: { labour_id: string; subscription_id: string };
};

function getQueryKeysForEvent(event: LabourEvent): string[][] {
  if (event.LabourPlanned) {
    return [
      ['labour-v2', event.LabourPlanned.labour_id],
      ['labour-v2', 'active'],
      ['labour-v2', 'history'],
    ];
  }

  if (event.LabourPlanUpdated) {
    return [['labour-v2', event.LabourPlanUpdated.labour_id]];
  }

  if (event.LabourBegun) {
    return [
      ['labour-v2', event.LabourBegun.labour_id],
      ['labour-updates-v2', event.LabourBegun.labour_id],
    ];
  }

  if (event.LabourCompleted) {
    return [
      ['labour-v2', event.LabourCompleted.labour_id],
      ['labour-v2', 'active'],
      ['labour-v2', 'history'],
    ];
  }

  if (event.LabourInviteSent) {
    return [];
  }

  if (event.LabourDeleted) {
    return [
      ['labour-v2', event.LabourDeleted.labour_id],
      ['labour-v2', 'active'],
      ['labour-v2', 'history'],
    ];
  }

  if (event.ContractionStarted) {
    return [
      ['contractions-v2', event.ContractionStarted.labour_id],
      ['labour-v2', event.ContractionStarted.labour_id],
    ];
  }

  if (event.ContractionEnded) {
    return [
      ['contractions-v2', event.ContractionEnded.labour_id],
    ];
  }

  if (event.ContractionUpdated) {
    return [
      ['contractions-v2', event.ContractionUpdated.labour_id],
    ];
  }

  if (event.ContractionDeleted) {
    return [
      ['contractions-v2', event.ContractionDeleted.labour_id],
    ];
  }

  if (event.LabourUpdatePosted) {
    return [
      ['labour-updates-v2', event.LabourUpdatePosted.labour_id],
    ];
  }

  if (event.LabourUpdateMessageUpdated) {
    return [
      ['labour-updates-v2', event.LabourUpdateMessageUpdated.labour_id],
    ];
  }

  if (event.LabourUpdateTypeUpdated) {
    return [
      ['labour-updates-v2', event.LabourUpdateTypeUpdated.labour_id],
    ];
  }

  if (event.LabourUpdateDeleted) {
    return [
      ['labour-updates-v2', event.LabourUpdateDeleted.labour_id],
    ];
  }

  if (event.SubscriberRequested) {
    return [
      ['subscriptions-v2'],
    ];
  }

  if (event.SubscriberUnsubscribed) {
    return [
      ['subscriptions-v2'],
    ];
  }

  if (event.SubscriberNotificationMethodsUpdated) {
    return [
      ['subscriptions-v2', event.SubscriberNotificationMethodsUpdated.labour_id],
    ];
  }

  if (event.SubscriberAccessLevelUpdated) {
    return [
      ['subscriptions-v2'],
    ];
  }

  if (event.SubscriberApproved) {
    return [
      ['subscriptions-v2'],
      ['users-v2', event.SubscriberApproved.labour_id],
    ];
  }

  if (event.SubscriberRemoved) {
    return [
      ['subscriptions-v2'],
      ['users-v2', event.SubscriberRemoved.labour_id],
    ];
  }

  if (event.SubscriberBlocked) {
    return [
      ['subscriptions-v2'],
    ];
  }

  if (event.SubscriberUnblocked) {
    return [
      ['subscriptions-v2'],
    ];
  }

  if (event.SubscriberRoleUpdated) {
    return [
      ['subscriptions-v2'],
    ];
  }

  return [];
}

export function useWebSocketInvalidation() {
  const queryClient = useQueryClient();
  const { subscribe } = useWebSocket();

  useEffect(() => {
    const unsubscribe = subscribe((message) => {
      const parsed =
        typeof message === 'string'
          ? JSON.parse(message)
          : message;
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
