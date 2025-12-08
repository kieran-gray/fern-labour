/**
 * TypeScript types for Labour Service V2 API Commands
 * Generated from Rust command definitions in packages/labour-shared/src/commands/
 */

// Value Objects / Enums

export enum SubscriberContactMethod {
  EMAIL = "EMAIL",
  SMS = "SMS",
  WHATSAPP = "WHATSAPP",
}

export enum SubscriberAccessLevel {
  BASIC = "BASIC",
  SUPPORTER = "SUPPORTER",
}

export enum SubscriberRole {
  BIRTH_PARTNER = "BIRTH_PARTNER",
  FRIENDS_AND_FAMILY = "FRIENDS_AND_FAMILY",
}

export enum LabourUpdateType {
  ANNOUNCEMENT = "ANNOUNCEMENT",
  STATUS_UPDATE = "STATUS_UPDATE",
  PRIVATE_NOTE = "PRIVATE_NOTE",
}

// Admin Commands

export type RebuildReadModelsCommand = {
  type: "RebuildReadModels";
  payload: {
    aggregate_id: string;
  };
};

export type AdminCommand = RebuildReadModelsCommand;

// Contraction Commands

export type StartContractionCommand = {
  type: "StartContraction";
  payload: {
    labour_id: string;
    start_time: string; // ISO 8601 datetime
  };
};

export type EndContractionCommand = {
  type: "EndContraction";
  payload: {
    labour_id: string;
    end_time: string; // ISO 8601 datetime
    intensity: number; // u8 in Rust, 0-255
  };
};

export type UpdateContractionCommand = {
  type: "UpdateContraction";
  payload: {
    labour_id: string;
    contraction_id: string;
    start_time?: string; // ISO 8601 datetime
    end_time?: string; // ISO 8601 datetime
    intensity?: number; // u8 in Rust, 0-255
  };
};

export type DeleteContractionCommand = {
  type: "DeleteContraction";
  payload: {
    labour_id: string;
    contraction_id: string;
  };
};

export type ContractionCommand =
  | StartContractionCommand
  | EndContractionCommand
  | UpdateContractionCommand
  | DeleteContractionCommand;

// Labour Commands

export type PlanLabourCommand = {
  type: "PlanLabour";
  payload: {
    first_labour: boolean;
    due_date: string; // ISO 8601 datetime
    labour_name?: string;
  };
};

export type UpdateLabourPlanCommand = {
  type: "UpdateLabourPlan";
  payload: {
    labour_id: string;
    first_labour: boolean;
    due_date: string; // ISO 8601 datetime
    labour_name?: string;
  };
};

export type BeginLabourCommand = {
  type: "BeginLabour";
  payload: {
    labour_id: string;
  };
};

export type CompleteLabourCommand = {
  type: "CompleteLabour";
  payload: {
    labour_id: string;
  };
};

export type SendLabourInviteCommand = {
  type: "SendLabourInvite";
  payload: {
    labour_id: string;
    invite_email: string;
  };
};

export type DeleteLabourCommand = {
  type: "DeleteLabour";
  payload: {
    labour_id: string;
  };
};

export type LabourCommand =
  | UpdateLabourPlanCommand
  | BeginLabourCommand
  | CompleteLabourCommand
  | SendLabourInviteCommand
  | DeleteLabourCommand;

// Public Labour Commands (for unauthenticated users)
export type PublicCommand = PlanLabourCommand;

// Labour Update Commands

export type PostLabourUpdateCommand = {
  type: "PostLabourUpdate";
  payload: {
    labour_id: string;
    labour_update_type: LabourUpdateType;
    message: string;
  };
};

export type UpdateLabourUpdateMessageCommand = {
  type: "UpdateLabourUpdateMessage";
  payload: {
    labour_id: string;
    labour_update_id: string;
    message: string;
  };
};

export type UpdateLabourUpdateTypeCommand = {
  type: "UpdateLabourUpdateType";
  payload: {
    labour_id: string;
    labour_update_id: string;
    labour_update_type: LabourUpdateType;
  };
};

export type DeleteLabourUpdateCommand = {
  type: "DeleteLabourUpdate";
  payload: {
    labour_id: string;
    labour_update_id: string;
  };
};

export type LabourUpdateCommand =
  | PostLabourUpdateCommand
  | UpdateLabourUpdateMessageCommand
  | UpdateLabourUpdateTypeCommand
  | DeleteLabourUpdateCommand;

// Subscriber Commands

export type RequestAccessCommand = {
  type: "RequestAccess";
  payload: {
    labour_id: string;
    token: string;
  };
};

export type UnsubscribeCommand = {
  type: "Unsubscribe";
  payload: {
    labour_id: string;
  };
};

export type UpdateNotificationMethodsCommand = {
  type: "UpdateNotificationMethods";
  payload: {
    labour_id: string;
    notification_methods: SubscriberContactMethod[];
  };
};

export type UpdateAccessLevelCommand = {
  type: "UpdateAccessLevel";
  payload: {
    labour_id: string;
    access_level: SubscriberAccessLevel;
  };
};

export type SubscriberCommand =
  | RequestAccessCommand
  | UnsubscribeCommand
  | UpdateNotificationMethodsCommand
  | UpdateAccessLevelCommand;

// Subscription Commands

export type ApproveSubscriberCommand = {
  type: "ApproveSubscriber";
  payload: {
    labour_id: string;
    subscription_id: string;
  };
};

export type RemoveSubscriberCommand = {
  type: "RemoveSubscriber";
  payload: {
    labour_id: string;
    subscription_id: string;
  };
};

export type BlockSubscriberCommand = {
  type: "BlockSubscriber";
  payload: {
    labour_id: string;
    subscription_id: string;
  };
};

export type UnblockSubscriberCommand = {
  type: "UnblockSubscriber";
  payload: {
    labour_id: string;
    subscription_id: string;
  };
};

export type UpdateSubscriberRoleCommand = {
  type: "UpdateSubscriberRole";
  payload: {
    labour_id: string;
    subscription_id: string;
    role: SubscriberRole;
  };
};

export type SubscriptionCommand =
  | ApproveSubscriberCommand
  | RemoveSubscriberCommand
  | BlockSubscriberCommand
  | UnblockSubscriberCommand
  | UpdateSubscriberRoleCommand;

// Top-level API Command (matches Rust ApiCommand enum)

export type ApiCommand =
  | { type: "Admin"; payload: AdminCommand }
  | { type: "Contraction"; payload: ContractionCommand }
  | { type: "Labour"; payload: LabourCommand }
  | { type: "LabourUpdate"; payload: LabourUpdateCommand }
  | { type: "Subscriber"; payload: SubscriberCommand }
  | { type: "Subscription"; payload: SubscriptionCommand };

// Response types (you can extend these based on your API responses)

export type ApiResponse<T = unknown> = {
  success: boolean;
  data?: T;
  error?: string;
};

export type CommandResponse = ApiResponse<void>;
