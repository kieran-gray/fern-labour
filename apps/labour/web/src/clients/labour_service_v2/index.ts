/**
 * Labour Service V2 Client
 *
 * TypeScript client for the V2 Cloudflare Workers Labour API.
 * This client is manually maintained based on the Rust command definitions
 * in packages/labour-shared/src/commands/
 */

export { LabourServiceV2Client } from './client';
export type { LabourServiceV2Config } from './client';

export {
  SubscriberContactMethod,
  SubscriberAccessLevel,
  SubscriberRole,
  LabourUpdateType,
} from './types';

export type {
  // Admin Commands
  AdminCommand,
  RebuildReadModelsCommand,
  // Contraction Commands
  ContractionCommand,
  StartContractionCommand,
  EndContractionCommand,
  UpdateContractionCommand,
  DeleteContractionCommand,
  // Labour Commands
  LabourCommand,
  PublicCommand,
  PlanLabourCommand,
  UpdateLabourPlanCommand,
  BeginLabourCommand,
  CompleteLabourCommand,
  SendLabourInviteCommand,
  DeleteLabourCommand,
  // Labour Update Commands
  LabourUpdateCommand,
  PostLabourUpdateCommand,
  UpdateLabourUpdateMessageCommand,
  UpdateLabourUpdateTypeCommand,
  DeleteLabourUpdateCommand,
  // Subscriber Commands
  SubscriberCommand,
  RequestAccessCommand,
  UnsubscribeCommand,
  UpdateNotificationMethodsCommand,
  UpdateAccessLevelCommand,
  // Subscription Commands
  SubscriptionCommand,
  ApproveSubscriberCommand,
  RemoveSubscriberCommand,
  BlockSubscriberCommand,
  UnblockSubscriberCommand,
  UpdateSubscriberRoleCommand,
  // Top-level API Command
  ApiCommand,
  // Response types
  ApiResponse,
  CommandResponse,
} from './types';
