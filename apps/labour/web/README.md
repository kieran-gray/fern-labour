# Frontend

## Overview

The Frontend is a modern React Single Page Application (SPA) for the labour tracking system. It provides an intuitive interface for users to track pregnancy labour progress, manage contractions, invite birth partners, and view labour history. The application features real-time updates, responsive design, and secure authentication.

**Key Features:**
- Labour session management and contraction tracking
- Real-time labour progress visualization with charts
- Birth partner subscription and invitation system
- Responsive design with mobile-first approach
- Secure authentication via Keycloak OIDC
- QR code generation for easy partner invites
- Contact form integration with spam protection

## Architecture & Dependencies

**Framework & Technologies:**
- **React 18** - Modern React with hooks and concurrent features
- **TypeScript** - Type-safe development with strict configuration
- **Vite** - Fast build tool and development server
- **Mantine UI** - Component library with built-in dark mode
- **React Query** - Server state management and caching
- **React Router** - Client-side routing with protected routes
- **React OIDC Context** - Keycloak authentication integration
- **Recharts** - Data visualization for labour progress
- **Axios** - HTTP client for API communication

**Architecture Pattern:**
- **Component-based architecture** with shared components
- **Page-based routing** with lazy loading
- **Context providers** for global state management
- **Custom hooks** for business logic abstraction
- **Auto-generated API clients** from OpenAPI specifications

**Directory Structure:**
```
src/
├── pages/              # Page components (Labour, Subscription, etc.)
├── shared-components/  # Reusable UI components
├── clients/           # Auto-generated API clients
├── utils.ts           # Utility functions
├── config.ts          # Application configuration
├── Router.tsx         # Route definitions
├── App.tsx           # Main application component
└── main.tsx          # Application entry point
```

## Setup Instructions

### Prerequisites

1. **Node.js 18+** and **npm**
2. **Backend services** running (labour_service, contact_service)
3. **Keycloak** authentication server
4. **Environment variables** configured

### Installation

1. **Install Dependencies:**
   ```bash
   npm install
   ```

2. **Environment Configuration:**
   Set up environment variables (typically handled via Docker build args):
   ```bash
   # Keycloak Configuration
   VITE_KEYCLOAK_AUTHORITY=http://localhost:8080/realms/labour_tracker
   VITE_KEYCLOAK_METADATA_URL=http://localhost:8080/realms/labour_tracker/.well-known/openid_configuration
   VITE_KEYCLOAK_CLIENT_ID=labour_tracker_frontend
   VITE_POST_LOGOUT_REDIRECT=http://localhost:3000
   
   # API Endpoints
   VITE_LABOUR_SERVICE_URL=http://localhost:8000
   VITE_CONTACT_SERVICE_URL=http://localhost:8002
   
   # Cloudflare Turnstile
   VITE_CLOUDFLARE_SITEKEY=your_turnstile_site_key
   ```

3. **Generate API Clients:**
   ```bash
   npm run generate-client
   ```

### Running Locally

**Via Docker Compose (Recommended):**
```bash
# From project root
make run
```

**Direct Development:**
```bash
# Start development server with hot reload
npm run dev

# Open browser to http://localhost:5173
```

## Deployment

### Docker Build
The application uses multi-stage Docker builds:
- **Development stage** - Full development environment with hot reload
- **Build stage** - Production build generation
- **Production stage** - Nginx serving static files

### Environment Variables
Build-time variables are injected during Docker build:

```dockerfile
ARG VITE_KEYCLOAK_AUTHORITY
ARG VITE_LABOUR_SERVICE_URL
ARG VITE_CONTACT_SERVICE_URL
# ... other variables
```

### Production Build
```bash
# Create production build
npm run build

# Preview production build locally
npm run preview
```

## Testing

### Running Tests
```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Run full test suite (includes lint and typecheck)
npm test
```

### Test Structure
- **Framework:** Jest with TypeScript support
- **Location:** `src/**/*.Test.ts` and `src/**/__tests__/`
- **Coverage:** Collected from all TypeScript files in src
- **Mocking:** Jest mocks for external dependencies

### Code Quality
```bash
# Type checking
npm run typecheck

# Linting (ESLint + Stylelint)
npm run lint

# Auto-fix linting issues
npm run lint:fix

# Format code with Prettier
npm run prettier:write

# Check Prettier formatting
npm run prettier:check
```

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_KEYCLOAK_AUTHORITY` | Keycloak realm authority URL | `http://localhost:8080/realms/labour_tracker` |
| `VITE_KEYCLOAK_CLIENT_ID` | Keycloak client ID | `labour_tracker_frontend` |
| `VITE_KEYCLOAK_METADATA_URL` | OIDC metadata endpoint | `http://localhost:8080/realms/labour_tracker/.well-known/openid_configuration` |
| `VITE_LABOUR_SERVICE_URL` | Labour service API base URL | `http://localhost:8000` |
| `VITE_CONTACT_SERVICE_URL` | Contact service API base URL | `http://localhost:8002` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_POST_LOGOUT_REDIRECT` | Post-logout redirect URL | Marketing site URL |
| `VITE_CLOUDFLARE_SITEKEY` | Turnstile site key for contact forms | Development key |

Environment variables prefixed with `VITE_` are exposed to the browser.

## API Integration

### Auto-Generated Clients
API clients are automatically generated from backend OpenAPI specifications:

```bash
# Generate clients from running services
npm run generate-client
```

This creates type-safe clients in `src/clients/` directory:
- `labour_service/` - Labour and subscription management
- `contact_service/` - Contact form submissions

### Client Usage
```typescript
import { LabourService } from '@clients/labour_service';

// Initialize client with authentication
const labourClient = new LabourService({
  baseUrl: import.meta.env.VITE_LABOUR_SERVICE_URL,
  // Auth token automatically added by interceptors
});

// Use generated methods
const labours = await labourClient.getLabours();
```

### Authentication
- **OIDC/OAuth2** via Keycloak integration
- **JWT tokens** automatically attached to API requests
- **Automatic token refresh** handled by React OIDC Context
- **Protected routes** require authentication

## Key Pages & Features

### Core Pages

**Home (`/`):**
- App mode selection (birthing person vs birth partner)
- Quick access to main features

**Labour (`/labour`):**
- Active labour session management
- Real-time contraction tracking with timer
- Labour progress visualization
- Quick action buttons for contraction start/stop

**Labour History (`/labour-history`):**
- Historical labour sessions with charts
- Detailed contraction timeline views
- Export and sharing capabilities

**Subscription (`/subscription`):**
- Birth partner invitation management
- QR code generation for easy sharing
- Subscription status monitoring

**Subscribe (`/subscribe/:token`):**
- Birth partner subscription interface
- Contact method selection (SMS, email)
- Subscription confirmation

**Contact (`/contact`):**
- Contact form with spam protection
- Category-based message routing
- Integration with contact service

### Shared Components

**AppShell:**
- Navigation header with user menu
- Authentication status display
- Responsive mobile navigation

**ProtectedApp:**
- Authentication wrapper for protected routes
- Automatic login redirect
- Loading states during auth check

**Modal System:**
- Consistent modal styling
- Mobile-responsive dialogs
- Accessibility features

**Charts & Visualizations:**
- Labour progress tracking
- Contraction frequency analysis
- Historical data visualization

## Contributing Notes

### Code Standards
- **TypeScript strict mode** enforced
- **ESLint** with React and accessibility rules
- **Prettier** for consistent code formatting
- **Component composition** over inheritance
- **Custom hooks** for reusable logic

### Development Workflow
1. Create feature branch from `main`
2. Implement changes with TypeScript
3. Add tests for new functionality
4. Run `npm test` to validate all checks
5. Submit pull request with descriptive commits

### Component Guidelines
- Use functional components with hooks
- Implement proper TypeScript interfaces
- Follow Mantine UI patterns and theming
- Ensure mobile responsiveness
- Add proper accessibility attributes

### State Management
- **React Query** for server state
- **React Context** for global client state
- **Local component state** for UI state
- **Custom hooks** for complex state logic

### Performance Considerations
- **Lazy loading** for route-based code splitting
- **React Query caching** for API responses
- **Memoization** for expensive calculations
- **Image optimization** and proper loading states
- **Bundle analysis** with build tools

### Testing Strategy
- **Unit tests** for utility functions
- **Component tests** for UI logic
- **Integration tests** for user workflows
- **Type safety** as first line of defense
- **Manual testing** for responsive design