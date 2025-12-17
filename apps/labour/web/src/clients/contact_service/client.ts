import type { ContactResponse, CreateContactMessageRequest } from './types';

export interface ContactServiceConfig {
  baseUrl: string;
}

export class ContactServiceClient {
  private config: ContactServiceConfig;

  constructor(config: ContactServiceConfig) {
    this.config = config;
  }

  async createContactMessage(request: CreateContactMessageRequest): Promise<ContactResponse> {
    const url = `${this.config.baseUrl}/api/v1/contact-us/`;

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        const errorText = await response.text();
        return {
          success: false,
          error: errorText || `HTTP ${response.status}: ${response.statusText}`,
        };
      }

      return {
        success: true,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred',
      };
    }
  }
}
