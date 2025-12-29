import { useEffect } from 'react';
import type {
  ContractionReadModel,
  LabourUpdateReadModel,
  PaginatedResponse,
} from '@base/clients/labour_service';
import { InfiniteData, useQueryClient } from '@tanstack/react-query';
import { useWebSocket } from '../contexts/WebsocketContext';
import { queryKeysV2 } from './queryKeys';

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

type InfiniteContractionData = InfiniteData<PaginatedResponse<ContractionReadModel>, unknown>;
type InfiniteLabourUpdateData = InfiniteData<PaginatedResponse<LabourUpdateReadModel>, unknown>;

function prependContraction(
  queryClient: ReturnType<typeof useQueryClient>,
  labourId: string,
  contraction: ContractionReadModel
) {
  const queryKey = queryKeysV2.contractions.infinite(labourId);
  queryClient.setQueryData<InfiniteContractionData>(queryKey, (old) => {
    if (!old || old.pages.length === 0) {
      return old;
    }

    const exists = old.pages.some((page) =>
      page.data.some((item) => item.contraction_id === contraction.contraction_id)
    );
    if (exists) {
      return old;
    }

    const [firstPage, ...rest] = old.pages;
    return {
      ...old,
      pages: [{ ...firstPage, data: [contraction, ...firstPage.data] }, ...rest],
    };
  });
}

function updateContraction(
  queryClient: ReturnType<typeof useQueryClient>,
  labourId: string,
  contractionId: string,
  updater: (c: ContractionReadModel) => ContractionReadModel
) {
  const queryKey = queryKeysV2.contractions.infinite(labourId);
  queryClient.setQueryData<InfiniteContractionData>(queryKey, (old) => {
    if (!old) {
      return old;
    }
    return {
      ...old,
      pages: old.pages.map((page) => ({
        ...page,
        data: page.data.map((item) =>
          item.contraction_id === contractionId ? updater(item) : item
        ),
      })),
    };
  });
}

function removeContraction(
  queryClient: ReturnType<typeof useQueryClient>,
  labourId: string,
  contractionId: string
) {
  const queryKey = queryKeysV2.contractions.infinite(labourId);
  queryClient.setQueryData<InfiniteContractionData>(queryKey, (old) => {
    if (!old) {
      return old;
    }
    return {
      ...old,
      pages: old.pages.map((page) => ({
        ...page,
        data: page.data.filter((item) => item.contraction_id !== contractionId),
      })),
    };
  });
}

function prependLabourUpdate(
  queryClient: ReturnType<typeof useQueryClient>,
  labourId: string,
  labourUpdate: LabourUpdateReadModel
) {
  const queryKey = queryKeysV2.labourUpdates.infinite(labourId);
  queryClient.setQueryData<InfiniteLabourUpdateData>(queryKey, (old) => {
    if (!old || old.pages.length === 0) {
      return old;
    }

    const exists = old.pages.some((page) =>
      page.data.some((item) => item.labour_update_id === labourUpdate.labour_update_id)
    );
    if (exists) {
      return old;
    }

    const [firstPage, ...rest] = old.pages;
    return {
      ...old,
      pages: [{ ...firstPage, data: [labourUpdate, ...firstPage.data] }, ...rest],
    };
  });
}

function updateLabourUpdate(
  queryClient: ReturnType<typeof useQueryClient>,
  labourId: string,
  labourUpdateId: string,
  updater: (u: LabourUpdateReadModel) => LabourUpdateReadModel
) {
  const queryKey = queryKeysV2.labourUpdates.infinite(labourId);
  queryClient.setQueryData<InfiniteLabourUpdateData>(queryKey, (old) => {
    if (!old) {
      return old;
    }
    return {
      ...old,
      pages: old.pages.map((page) => ({
        ...page,
        data: page.data.map((item) =>
          item.labour_update_id === labourUpdateId ? updater(item) : item
        ),
      })),
    };
  });
}

function removeLabourUpdate(
  queryClient: ReturnType<typeof useQueryClient>,
  labourId: string,
  labourUpdateId: string
) {
  const queryKey = queryKeysV2.labourUpdates.infinite(labourId);
  queryClient.setQueryData<InfiniteLabourUpdateData>(queryKey, (old) => {
    if (!old) {
      return old;
    }
    return {
      ...old,
      pages: old.pages.map((page) => ({
        ...page,
        data: page.data.filter((item) => item.labour_update_id !== labourUpdateId),
      })),
    };
  });
}

function handleEvent(queryClient: ReturnType<typeof useQueryClient>, event: LabourEvent) {
  const { type, data } = event;

  switch (type) {
    case 'LabourPlanned':
      queryClient.invalidateQueries({ queryKey: queryKeysV2.labour.detail(data.labour_id!) });
      queryClient.invalidateQueries({ queryKey: queryKeysV2.labour.active(data.labour_id!) });
      queryClient.invalidateQueries({ queryKey: queryKeysV2.labour.lists() });
      break;

    case 'LabourPlanUpdated':
      queryClient.invalidateQueries({ queryKey: queryKeysV2.labour.detail(data.labour_id!) });
      break;

    case 'LabourBegun':
      queryClient.invalidateQueries({ queryKey: queryKeysV2.labour.detail(data.labour_id!) });
      queryClient.invalidateQueries({
        queryKey: queryKeysV2.labourUpdates.infinite(data.labour_id!),
      });
      break;

    case 'LabourCompleted':
      queryClient.invalidateQueries({ queryKey: queryKeysV2.labour.detail(data.labour_id!) });
      queryClient.invalidateQueries({ queryKey: queryKeysV2.labour.lists() });
      break;

    case 'LabourDeleted':
      queryClient.removeQueries({ queryKey: queryKeysV2.labour.detail(data.labour_id!) });
      queryClient.invalidateQueries({ queryKey: queryKeysV2.labour.lists() });
      break;

    case 'LabourInviteSent':
      break;

    case 'ContractionStarted':
      if (data.contraction) {
        prependContraction(queryClient, data.labour_id!, data.contraction);
      } else {
        queryClient.invalidateQueries({
          queryKey: queryKeysV2.contractions.infinite(data.labour_id!),
        });
      }
      queryClient.invalidateQueries({ queryKey: queryKeysV2.labour.detail(data.labour_id!) });
      break;

    case 'ContractionEnded':
      if (data.contraction) {
        updateContraction(
          queryClient,
          data.labour_id!,
          data.contraction_id!,
          () => data.contraction!
        );
      } else {
        queryClient.invalidateQueries({
          queryKey: queryKeysV2.contractions.infinite(data.labour_id!),
        });
      }
      break;

    case 'ContractionUpdated':
      if (data.contraction) {
        updateContraction(
          queryClient,
          data.labour_id!,
          data.contraction_id!,
          () => data.contraction!
        );
      } else {
        queryClient.invalidateQueries({
          queryKey: queryKeysV2.contractions.infinite(data.labour_id!),
        });
      }
      break;

    case 'ContractionDeleted':
      removeContraction(queryClient, data.labour_id!, data.contraction_id!);
      break;

    case 'LabourUpdatePosted':
      if (data.labour_update) {
        prependLabourUpdate(queryClient, data.labour_id!, data.labour_update);
      } else {
        queryClient.invalidateQueries({
          queryKey: queryKeysV2.labourUpdates.infinite(data.labour_id!),
        });
      }
      break;

    case 'LabourUpdateMessageUpdated':
      if (data.labour_update) {
        updateLabourUpdate(
          queryClient,
          data.labour_id!,
          data.labour_update_id!,
          () => data.labour_update!
        );
      } else {
        queryClient.invalidateQueries({
          queryKey: queryKeysV2.labourUpdates.infinite(data.labour_id!),
        });
      }
      break;

    case 'LabourUpdateTypeUpdated':
      if (data.labour_update) {
        updateLabourUpdate(
          queryClient,
          data.labour_id!,
          data.labour_update_id!,
          () => data.labour_update!
        );
      } else {
        queryClient.invalidateQueries({
          queryKey: queryKeysV2.labourUpdates.infinite(data.labour_id!),
        });
      }
      break;

    case 'LabourUpdateDeleted':
      removeLabourUpdate(queryClient, data.labour_id!, data.labour_update_id!);
      break;

    case 'SubscriberRequested':
    case 'SubscriberUnsubscribed':
    case 'SubscriberAccessLevelUpdated':
    case 'SubscriberBlocked':
    case 'SubscriberUnblocked':
    case 'SubscriberRoleUpdated':
      queryClient.invalidateQueries({ queryKey: queryKeysV2.subscriptions.all });
      queryClient.invalidateQueries({ queryKey: queryKeysV2.users.listByLabour(data.labour_id!) });
      break;

    case 'SubscriberNotificationMethodsUpdated':
      queryClient.invalidateQueries({
        queryKey: queryKeysV2.subscriptions.listByLabour(data.labour_id!),
      });
      queryClient.invalidateQueries({
        queryKey: ['subscriptions', 'userSubscription', data.labour_id],
      });
      break;

    case 'SubscriberApproved':
    case 'SubscriberRemoved':
      queryClient.invalidateQueries({ queryKey: queryKeysV2.subscriptions.all });
      queryClient.invalidateQueries({ queryKey: queryKeysV2.users.listByLabour(data.labour_id!) });
      break;

    case 'SubscriptionTokenSet':
      queryClient.invalidateQueries({ queryKey: queryKeysV2.subscriptionToken.all });
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
