/**
 * Centralized utilities for the application
 * Re-exports from focused modules for backward compatibility
 */

// Formatting utilities
export {
  dueDateToGestationalAge,
  formatTimeMilliseconds,
  formatTimeSeconds,
  formatDurationHuman,
  pluraliseName,
} from './formatting';

// Validation utilities
export { validateEmail, validateMessage, validateLabourName } from './validation';

// Calculation utilities
export {
  getTimeSinceLastStarted,
  secondsElapsed,
  contractionDurationSeconds,
} from './calculations';

// Sorting utilities
export { sortContractions, sortLabours } from './sorting';
