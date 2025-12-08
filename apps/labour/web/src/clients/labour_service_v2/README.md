# Labour Service V2 Client

TypeScript client for the V2 Cloudflare Workers Labour API. This client is manually maintained and based on the Rust command definitions in `packages/labour-shared/src/commands/`.

## Overview

Unlike the V1 client which is auto-generated from OpenAPI specs, this V2 client is manually typed to match the command pattern used in the Cloudflare Workers backend. The types are derived directly from the Rust command enums to ensure type safety across the stack.

## API Endpoints

The V2 API uses two main endpoints:

- **POST /api/v1/labour/plan** - Create a new labour (takes PlanLabourDTO)
- **POST /api/v1/command** - Execute all other commands (takes ApiCommand with type and payload)

## Installation

```typescript
import { LabourServiceV2Client, LabourUpdateType } from '@/clients/labour_service_v2';
```

## Usage

### Initialize the Client

```typescript
const client = new LabourServiceV2Client({
  baseUrl: 'https://your-worker.workers.dev',
  getAccessToken: async () => {
    // Return your auth token
    return await getAuthToken();
  },
});
```

### Examples

#### Create a New Labour

```typescript
const response = await client.planLabour({
  firstLabour: true,
  dueDate: new Date('2025-06-15'),
  labourName: 'Baby Smith',
});

if (response.success && response.data) {
  console.log('Labour created:', response.data.labour_id);
}
```

#### Start a Contraction

```typescript
const response = await client.startContraction(
  labourId,
  new Date() // start time
);

if (response.success) {
  console.log('Contraction started');
}
```

#### Post a Labour Update

```typescript
const response = await client.postLabourUpdate(
  labourId,
  LabourUpdateType.STATUS_UPDATE,
  'Contractions are 5 minutes apart'
);
```

#### Manage Subscribers

```typescript
// Approve a subscriber
await client.approveSubscriber(labourId, subscriptionId);

// Update notification methods
await client.updateNotificationMethods(labourId, [
  SubscriberContactMethod.EMAIL,
  SubscriberContactMethod.SMS,
]);

// Update subscriber role
await client.updateSubscriberRole(
  labourId,
  subscriptionId,
  SubscriberRole.BIRTH_PARTNER
);
```

## Command Categories

### Admin Commands
- `rebuildReadModels(aggregateId)` - Rebuild read models for a labour aggregate

### Contraction Commands
- `startContraction(labourId, startTime)` - Start a new contraction
- `endContraction(labourId, endTime, intensity)` - End a contraction
- `updateContraction(params)` - Update contraction details
- `deleteContraction(labourId, contractionId)` - Delete a contraction

### Labour Commands
- `planLabour(params)` - Create a new labour (public endpoint)
- `updateLabourPlan(params)` - Update labour plan details
- `beginLabour(labourId)` - Mark labour as begun
- `completeLabour(labourId)` - Mark labour as completed
- `sendLabourInvite(labourId, email)` - Send invitation to subscriber
- `deleteLabour(labourId)` - Delete a labour

### Labour Update Commands
- `postLabourUpdate(labourId, type, message)` - Post a new update
- `updateLabourUpdateMessage(labourId, updateId, message)` - Update message
- `updateLabourUpdateType(labourId, updateId, type)` - Update type
- `deleteLabourUpdate(labourId, updateId)` - Delete an update

### Subscriber Commands
- `requestAccess(labourId, token)` - Request access with invite token
- `unsubscribe(labourId)` - Unsubscribe from labour
- `updateNotificationMethods(labourId, methods)` - Update notification preferences
- `updateAccessLevel(labourId, level)` - Update access level

### Subscription Commands
- `approveSubscriber(labourId, subscriptionId)` - Approve pending subscriber
- `removeSubscriber(labourId, subscriptionId)` - Remove subscriber
- `blockSubscriber(labourId, subscriptionId)` - Block subscriber
- `unblockSubscriber(labourId, subscriptionId)` - Unblock subscriber
- `updateSubscriberRole(labourId, subscriptionId, role)` - Update role

## Response Format

All commands return an `ApiResponse` with the following structure:

```typescript
type ApiResponse<T = unknown> = {
  success: boolean;
  data?: T;
  error?: string;
};
```

## Enums

### SubscriberContactMethod
- `EMAIL`
- `SMS`
- `WHATSAPP`

### SubscriberAccessLevel
- `BASIC`
- `SUPPORTER`

### SubscriberRole
- `BIRTH_PARTNER`
- `FRIENDS_AND_FAMILY`

### LabourUpdateType
- `ANNOUNCEMENT`
- `STATUS_UPDATE`
- `PRIVATE_NOTE`

## Migration from V1

When migrating from the V1 client to V2:

1. Replace the client import:
   ```typescript
   // Old
   import { LabourService } from '@/clients/labour_service';

   // New
   import { LabourServiceV2Client } from '@/clients/labour_service_v2';
   ```

2. Update method calls to use the new command-based API
3. Handle the new response format (`ApiResponse`)
4. Update types to use the V2 type definitions

## Keeping Types in Sync

The types in this client are manually maintained. When updating the Rust command definitions in `packages/labour-shared/src/commands/`, make sure to update the corresponding TypeScript types in:

- `types.ts` - Command and enum type definitions
- `client.ts` - Client method implementations

## Notes

- All dates are handled as JavaScript `Date` objects and automatically converted to ISO 8601 strings
- UUIDs are represented as strings
- The intensity field for contractions is a number (0-255, matching Rust's u8)
- Optional fields are represented with TypeScript's `?` operator
