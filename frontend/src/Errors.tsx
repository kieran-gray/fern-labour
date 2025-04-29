export class NotFoundError extends Error {
  constructor(message = 'Resource not found') {
    super(message);
    this.name = 'NotFoundError';
  }
}

export class PermissionDenied extends Error {
  constructor(message = 'You do not have permission to access this resource') {
    super(message);
    this.name = 'PermissionDenied';
  }
}
