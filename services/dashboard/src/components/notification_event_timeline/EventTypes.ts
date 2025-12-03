export interface EventMetadata {
  aggregate_id: string;
  sequence: number;
  event_version: number;
  timestamp: string;
  user_id: string;
}

export type NotificationEvent =
  | {
      NotificationRequested: {
        notification_id: string;
        channel: string;
        destination: {
          type: string;
          value: string;
        };
        template_data: {
          type: string;
          [key: string]: unknown;
        };
        metadata: Record<string, unknown> | null;
      };
    }
  | {
      RenderedContentStored: {
        notification_id: string;
        rendered_content: {
          Email?: {
            subject: string;
            html_body: string;
          };
          Sms?: {
            body: string;
          };
          WhatsApp?: {
            body: string;
          };
        };
      };
    }
  | {
      NotificationDispatched: {
        notification_id: string;
        external_id: string;
      };
    }
  | {
      NotificationDelivered: {
        notification_id: string;
      };
    }
  | {
      NotificationFailed: {
        notification_id: string;
        error: string;
      };
    };

export interface Event {
  metadata: EventMetadata;
  event: NotificationEvent;
}
