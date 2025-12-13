/**
 * Labour Service V2 Client
 *
 * This client provides methods to interact with the V2 Cloudflare Workers API
 * using the command pattern defined in the Rust backend.
 */

import type {
  AdminCommand,
  ContractionCommand,
  LabourCommand,
  LabourUpdateCommand,
  SubscriberCommand,
  SubscriptionCommand,
  CommandResponse,
  ApiResponse,
  SubscriberContactMethod,
  SubscriberAccessLevel,
  SubscriberRole,
  LabourUpdateType,
  LabourQuery,
  ContractionQuery,
  LabourUpdateQuery,
  Cursor,
  LabourReadModel,
  ContractionReadModel,
  LabourUpdateReadModel,
  PaginatedResponse,
  QueryResponse,
} from './types';

export interface LabourServiceV2Config {
  baseUrl: string;
  getAccessToken?: () => string | null | Promise<string | null>;
}

export class LabourServiceV2Client {
  private config: LabourServiceV2Config;

  constructor(config: LabourServiceV2Config) {
    this.config = config;
  }

  private async getHeaders(): Promise<Record<string, string>> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (this.config.getAccessToken) {
      const token = await this.config.getAccessToken();
      if (token) {
        headers.Authorization = `Bearer ${token}`;
      }
    }

    return headers;
  }

  private async sendCommand<T = void>(command: unknown): Promise<ApiResponse<T>> {
    const headers = await this.getHeaders();
    const url = `${this.config.baseUrl}/api/v1/command`;

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers,
        body: JSON.stringify(command),
      });

      if (!response.ok) {
        const errorText = await response.text();
        return {
          success: false,
          error: errorText || `HTTP ${response.status}: ${response.statusText}`,
        };
      }

      const data = response.status === 204 ? undefined : await response.json();

      return {
        success: true,
        data,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred',
      };
    }
  }

  private async sendPlanLabour(dto: {
    first_labour: boolean;
    due_date: string;
    labour_name?: string;
  }): Promise<ApiResponse<{ labour_id: string }>> {
    const headers = await this.getHeaders();
    const url = `${this.config.baseUrl}/api/v1/labour/plan`;

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers,
        body: JSON.stringify(dto),
      });

      if (!response.ok) {
        const errorText = await response.text();
        return {
          success: false,
          error: errorText || `HTTP ${response.status}: ${response.statusText}`,
        };
      }

      const data = await response.json();

      return {
        success: true,
        data,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred',
      };
    }
  }

  // Admin Commands

  async rebuildReadModels(aggregateId: string): Promise<CommandResponse> {
    const command: AdminCommand = {
      type: 'RebuildReadModels',
      payload: { aggregate_id: aggregateId },
    };
    return this.sendCommand({ type: 'Admin', payload: command });
  }

  // Contraction Commands

  async startContraction(labourId: string, startTime: Date): Promise<CommandResponse> {
    const command: ContractionCommand = {
      type: 'StartContraction',
      payload: {
        labour_id: labourId,
        start_time: startTime.toISOString(),
      },
    };
    return this.sendCommand({ type: 'Contraction', payload: command });
  }

  async endContraction(
    labourId: string,
    endTime: Date,
    intensity: number
  ): Promise<CommandResponse> {
    const command: ContractionCommand = {
      type: 'EndContraction',
      payload: {
        labour_id: labourId,
        end_time: endTime.toISOString(),
        intensity,
      },
    };
    return this.sendCommand({ type: 'Contraction', payload: command });
  }

  async updateContraction(params: {
    labourId: string;
    contractionId: string;
    startTime?: Date;
    endTime?: Date;
    intensity?: number;
  }): Promise<CommandResponse> {
    const command: ContractionCommand = {
      type: 'UpdateContraction',
      payload: {
        labour_id: params.labourId,
        contraction_id: params.contractionId,
        start_time: params.startTime?.toISOString(),
        end_time: params.endTime?.toISOString(),
        intensity: params.intensity,
      },
    };
    return this.sendCommand({ type: 'Contraction', payload: command });
  }

  async deleteContraction(
    labourId: string,
    contractionId: string
  ): Promise<CommandResponse> {
    const command: ContractionCommand = {
      type: 'DeleteContraction',
      payload: {
        labour_id: labourId,
        contraction_id: contractionId,
      },
    };
    return this.sendCommand({ type: 'Contraction', payload: command });
  }

  // Labour Commands

  async planLabour(params: {
    firstLabour: boolean;
    dueDate: Date;
    labourName?: string;
  }): Promise<ApiResponse<{ labour_id: string }>> {
    return this.sendPlanLabour({
      first_labour: params.firstLabour,
      due_date: params.dueDate.toISOString(),
      labour_name: params.labourName,
    });
  }

  async updateLabourPlan(params: {
    labourId: string;
    firstLabour: boolean;
    dueDate: Date;
    labourName?: string;
  }): Promise<CommandResponse> {
    const command: LabourCommand = {
      type: 'UpdateLabourPlan',
      payload: {
        labour_id: params.labourId,
        first_labour: params.firstLabour,
        due_date: params.dueDate.toISOString(),
        labour_name: params.labourName,
      },
    };
    return this.sendCommand({ type: 'Labour', payload: command });
  }

  async beginLabour(labourId: string): Promise<CommandResponse> {
    const command: LabourCommand = {
      type: 'BeginLabour',
      payload: { labour_id: labourId },
    };
    return this.sendCommand({ type: 'Labour', payload: command });
  }

  async completeLabour(params: {labourId: string, notes: string}): Promise<CommandResponse> {
    const command: LabourCommand = {
      type: 'CompleteLabour',
      payload: { labour_id: params.labourId, notes: params.notes },
    };
    return this.sendCommand({ type: 'Labour', payload: command });
  }

  async sendLabourInvite(labourId: string, inviteEmail: string): Promise<CommandResponse> {
    const command: LabourCommand = {
      type: 'SendLabourInvite',
      payload: {
        labour_id: labourId,
        invite_email: inviteEmail,
      },
    };
    return this.sendCommand({ type: 'Labour', payload: command });
  }

  async deleteLabour(labourId: string): Promise<CommandResponse> {
    const command: LabourCommand = {
      type: 'DeleteLabour',
      payload: { labour_id: labourId },
    };
    return this.sendCommand({ type: 'Labour', payload: command });
  }

  // Labour Update Commands

  async postLabourUpdate(
    labourId: string,
    updateType: LabourUpdateType,
    message: string
  ): Promise<CommandResponse> {
    const command: LabourUpdateCommand = {
      type: 'PostLabourUpdate',
      payload: {
        labour_id: labourId,
        labour_update_type: updateType,
        message,
      },
    };
    return this.sendCommand({ type: 'LabourUpdate', payload: command });
  }

  async updateLabourUpdateMessage(
    labourId: string,
    labourUpdateId: string,
    message: string
  ): Promise<CommandResponse> {
    const command: LabourUpdateCommand = {
      type: 'UpdateLabourUpdateMessage',
      payload: {
        labour_id: labourId,
        labour_update_id: labourUpdateId,
        message,
      },
    };
    return this.sendCommand({ type: 'LabourUpdate', payload: command });
  }

  async updateLabourUpdateType(
    labourId: string,
    labourUpdateId: string,
    updateType: LabourUpdateType
  ): Promise<CommandResponse> {
    const command: LabourUpdateCommand = {
      type: 'UpdateLabourUpdateType',
      payload: {
        labour_id: labourId,
        labour_update_id: labourUpdateId,
        labour_update_type: updateType,
      },
    };
    return this.sendCommand({ type: 'LabourUpdate', payload: command });
  }

  async deleteLabourUpdate(
    labourId: string,
    labourUpdateId: string
  ): Promise<CommandResponse> {
    const command: LabourUpdateCommand = {
      type: 'DeleteLabourUpdate',
      payload: {
        labour_id: labourId,
        labour_update_id: labourUpdateId,
      },
    };
    return this.sendCommand({ type: 'LabourUpdate', payload: command });
  }

  // Subscriber Commands

  async requestAccess(labourId: string, token: string): Promise<CommandResponse> {
    const command: SubscriberCommand = {
      type: 'RequestAccess',
      payload: {
        labour_id: labourId,
        token,
      },
    };
    return this.sendCommand({ type: 'Subscriber', payload: command });
  }

  async unsubscribe(labourId: string): Promise<CommandResponse> {
    const command: SubscriberCommand = {
      type: 'Unsubscribe',
      payload: { labour_id: labourId },
    };
    return this.sendCommand({ type: 'Subscriber', payload: command });
  }

  async updateNotificationMethods(
    labourId: string,
    methods: SubscriberContactMethod[]
  ): Promise<CommandResponse> {
    const command: SubscriberCommand = {
      type: 'UpdateNotificationMethods',
      payload: {
        labour_id: labourId,
        notification_methods: methods,
      },
    };
    return this.sendCommand({ type: 'Subscriber', payload: command });
  }

  async updateAccessLevel(
    labourId: string,
    accessLevel: SubscriberAccessLevel
  ): Promise<CommandResponse> {
    const command: SubscriberCommand = {
      type: 'UpdateAccessLevel',
      payload: {
        labour_id: labourId,
        access_level: accessLevel,
      },
    };
    return this.sendCommand({ type: 'Subscriber', payload: command });
  }

  // Subscription Commands

  async approveSubscriber(
    labourId: string,
    subscriptionId: string
  ): Promise<CommandResponse> {
    const command: SubscriptionCommand = {
      type: 'ApproveSubscriber',
      payload: {
        labour_id: labourId,
        subscription_id: subscriptionId,
      },
    };
    return this.sendCommand({ type: 'Subscription', payload: command });
  }

  async removeSubscriber(labourId: string, subscriptionId: string): Promise<CommandResponse> {
    const command: SubscriptionCommand = {
      type: 'RemoveSubscriber',
      payload: {
        labour_id: labourId,
        subscription_id: subscriptionId,
      },
    };
    return this.sendCommand({ type: 'Subscription', payload: command });
  }

  async blockSubscriber(labourId: string, subscriptionId: string): Promise<CommandResponse> {
    const command: SubscriptionCommand = {
      type: 'BlockSubscriber',
      payload: {
        labour_id: labourId,
        subscription_id: subscriptionId,
      },
    };
    return this.sendCommand({ type: 'Subscription', payload: command });
  }

  async unblockSubscriber(
    labourId: string,
    subscriptionId: string
  ): Promise<CommandResponse> {
    const command: SubscriptionCommand = {
      type: 'UnblockSubscriber',
      payload: {
        labour_id: labourId,
        subscription_id: subscriptionId,
      },
    };
    return this.sendCommand({ type: 'Subscription', payload: command });
  }

  async updateSubscriberRole(
    labourId: string,
    subscriptionId: string,
    role: SubscriberRole
  ): Promise<CommandResponse> {
    const command: SubscriptionCommand = {
      type: 'UpdateSubscriberRole',
      payload: {
        labour_id: labourId,
        subscription_id: subscriptionId,
        role,
      },
    };
    return this.sendCommand({ type: 'Subscription', payload: command });
  }

  // Query Methods

  private async sendQuery<T>(query: unknown): Promise<QueryResponse<T>> {
    const headers = await this.getHeaders();
    const url = `${this.config.baseUrl}/api/v1/query`;

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers,
        body: JSON.stringify(query),
      });

      if (!response.ok) {
        const errorText = await response.text();
        return {
          success: false,
          error: errorText || `HTTP ${response.status}: ${response.statusText}`,
        };
      }

      const data = await response.json();

      return {
        success: true,
        data,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred',
      };
    }
  }

  // Labour Queries

  async getLabour(labourId: string): Promise<QueryResponse<LabourReadModel>> {
    const query: LabourQuery = {
      type: 'GetLabour',
      payload: { labour_id: labourId },
    };
    return this.sendQuery({ type: 'Labour', payload: query });
  }

  // Contraction Queries

  async getContractions(
    labourId: string,
    limit: number = 20,
    cursor?: Cursor
  ): Promise<QueryResponse<PaginatedResponse<ContractionReadModel>>> {
    const query: ContractionQuery = {
      type: 'GetContractions',
      payload: {
        labour_id: labourId,
        limit,
        cursor,
      },
    };
    return this.sendQuery({ type: 'Contraction', payload: query });
  }

  async getContractionById(
    labourId: string,
    contractionId: string
  ): Promise<QueryResponse<PaginatedResponse<ContractionReadModel>>> {
    const query: ContractionQuery = {
      type: 'GetContractionById',
      payload: {
        labour_id: labourId,
        contraction_id: contractionId,
      },
    };
    return this.sendQuery({ type: 'Contraction', payload: query });
  }

  // Labour Update Queries

  async getLabourUpdates(
    labourId: string,
    limit: number = 20,
    cursor?: Cursor
  ): Promise<QueryResponse<PaginatedResponse<LabourUpdateReadModel>>> {
    const query: LabourUpdateQuery = {
      type: 'GetLabourUpdates',
      payload: {
        labour_id: labourId,
        limit,
        cursor,
      },
    };
    return this.sendQuery({ type: 'LabourUpdate', payload: query });
  }

  async getLabourUpdateById(
    labourId: string,
    labourUpdateId: string
  ): Promise<QueryResponse<PaginatedResponse<LabourUpdateReadModel>>> {
    const query: LabourUpdateQuery = {
      type: 'GetLabourUpdateById',
      payload: {
        labour_id: labourId,
        labour_update_id: labourUpdateId,
      },
    };
    return this.sendQuery({ type: 'LabourUpdate', payload: query });
  }
}
