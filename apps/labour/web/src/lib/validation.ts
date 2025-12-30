import {
  CONTACT_MESSAGE_MAX_LENGTH,
  EMAIL_MAX_LENGTH,
  EMAIL_REGEX,
  LABOUR_NAME_MAX_LENGTH,
} from './constants';

export function validateEmail(email: string): boolean {
  if (!email || typeof email !== 'string') {
    return false;
  }
  return EMAIL_REGEX.test(email) && email.length <= EMAIL_MAX_LENGTH;
}

export function validateMessage(message: string): string | null {
  if (!message || typeof message !== 'string') {
    return 'Invalid message format.';
  }
  if (message.length > CONTACT_MESSAGE_MAX_LENGTH) {
    return `Message exceeds maximum length of ${CONTACT_MESSAGE_MAX_LENGTH} characters.`;
  }
  return null;
}

export function validateLabourName(labourName: string | null): string | null {
  if (typeof labourName === 'string' && labourName.length > LABOUR_NAME_MAX_LENGTH) {
    return `Labour Name exceeds maximum length of ${LABOUR_NAME_MAX_LENGTH} characters.`;
  }
  return null;
}
