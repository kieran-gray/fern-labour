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
  LabourPhase,
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
  // Query Types
  Cursor,
  LabourQuery,
  GetLabourQuery,
  ContractionQuery,
  GetContractionsQuery,
  GetContractionByIdQuery,
  LabourUpdateQuery,
  GetLabourUpdatesQuery,
  GetLabourUpdateByIdQuery,
  ApiQuery,
  // Read Model Types
  LabourReadModel,
  Duration,
  ContractionReadModel,
  LabourUpdateReadModel,
  // Paginated Response
  PaginatedResponse,
  // Response types
  ApiResponse,
  CommandResponse,
  QueryResponse,
} from './types';
