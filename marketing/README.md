# Marketing

## Overview

The Marketing site is a Next.js-powered static website that serves as the landing page and marketing presence for the Fern Labour application. It features a modern, responsive design with interactive animations, comprehensive product information, and integrated contact functionality. The site focuses on converting visitors into users through compelling storytelling and clear calls-to-action.

**Key Features:**
- Landing page with hero section and feature showcases
- Interactive animations and motion graphics
- Pricing information and feature comparisons
- FAQ section with comprehensive product information
- Contact form with spam protection (Cloudflare Turnstile)
- Privacy policy and terms of service pages
- Static site generation for optimal performance
- SEO optimization and social media integration

## Architecture & Dependencies

**Framework & Technologies:**
- **Next.js 15** - React framework with pages router and static export
- **TypeScript** - Type-safe development with strict configuration
- **Mantine UI** - Component library with custom theming
- **Motion** - Animation library for interactive elements
- **PostCSS** - CSS processing with Mantine preset
- **ESLint** - Code quality enforcement with Mantine config
- **Bundle Analyzer** - Build optimization analysis

**Architecture Pattern:**
- **Static Site Generation (SSG)** with Next.js export
- **Component-based architecture** with reusable UI elements
- **Page-based routing** with Next.js pages router
- **Build-time optimization** for fast loading

**Directory Structure:**
```
├── pages/              # Next.js pages (index, contact, privacy, etc.)
├── components/         # Reusable UI components
│   ├── Landing/       # Landing page sections
│   ├── Contact/       # Contact form components
│   ├── Footer/        # Site footer
│   └── PillHeader/    # Navigation header
├── public/            # Static assets (images, icons, etc.)
├── theme.ts           # Mantine theme configuration
└── next.config.mjs    # Next.js configuration
```

## Setup Instructions

### Prerequisites

1. **Node.js 18+** and **npm** (or **yarn 4.6.0+**)
2. **Contact Service** (for contact form functionality)
3. **Cloudflare Turnstile** (for spam protection)

### Installation

1. **Install Dependencies:**
   ```bash
   npm install
   # or
   yarn install
   ```

2. **Environment Configuration:**
   Set up environment variables (typically handled via Docker build args):
   ```bash
   # API Integration
   NEXT_PUBLIC_CONTACT_SERVICE_URL=http://localhost:8002
   NEXT_PUBLIC_FRONTEND_URL=http://localhost:5173
   NEXT_PUBLIC_INSTAGRAM_URL=https://instagram.com/fernlabour
   
   # Cloudflare Turnstile
   NEXT_PUBLIC_CLOUDFLARE_SITEKEY=your_turnstile_site_key
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
# or
yarn dev

# Open browser to http://localhost:3000
```

## Deployment

### Static Site Export
The site is configured for static export, generating a fully static website:

```bash
# Build and export static site
npm run export

# Output generated in 'out/' directory
```

### Docker Build
Multi-stage Docker build for production:
- **Development stage** - Full development environment
- **Build stage** - Static site generation
- **Production stage** - Nginx serving static files

### Environment Variables
Build-time variables are injected during Docker build:

```dockerfile
ARG NEXT_PUBLIC_CONTACT_SERVICE_URL
ARG NEXT_PUBLIC_FRONTEND_URL
ARG NEXT_PUBLIC_CLOUDFLARE_SITEKEY
# ... other variables
```

### SEO & Performance
- Static generation for optimal loading speed
- Image optimization with Next.js Image component
- Meta tags and Open Graph integration
- Responsive design for all device types

## Testing

### Running Tests
```bash
# Type checking
npm run typecheck

# Linting
npm run lint

# Auto-fix linting issues
npm run lint:fix

# Check Prettier formatting
npm run prettier:check

# Format code with Prettier
npm run prettier:write

# Full test suite (lint + typecheck)
npm test
```

### Code Quality
- **TypeScript strict mode** enforced
- **ESLint** with Mantine configuration
- **Prettier** for consistent formatting
- **Bundle analysis** for performance optimization

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_FRONTEND_URL` | Main application URL | `http://localhost:5173` |
| `NEXT_PUBLIC_CONTACT_SERVICE_URL` | Contact form API endpoint | `http://localhost:8002` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_INSTAGRAM_URL` | Instagram profile link | Social media integration |
| `NEXT_PUBLIC_CLOUDFLARE_SITEKEY` | Turnstile site key | Development key |

All environment variables prefixed with `NEXT_PUBLIC_` are exposed to the browser.

## Key Pages & Features

### Core Pages

**Home (`/`):**
- Hero section with compelling value proposition
- Product story and benefits showcase
- Feature highlights with animations
- Pricing information
- FAQ section
- Call-to-action buttons linking to main app

**Contact (`/contact`):**
- Contact form with category selection
- Spam protection via Cloudflare Turnstile
- Integration with contact service
- Responsive form design

**Privacy Policy (`/privacy`):**
- Comprehensive privacy policy
- GDPR compliance information
- Data handling practices

**Terms of Service (`/terms-of-service`):**
- Service terms and conditions
- User responsibilities and rights
- Legal compliance information

**404 Page:**
- Custom not found page
- Navigation back to main sections

### Landing Page Components

**Hero Section:**
- Compelling headline and value proposition
- Call-to-action button to main application
- Professional visuals and branding

**Storytelling Sections:**
- Problem/solution narrative
- User journey visualization
- Emotional connection building
- Benefits highlighting

**Features Showcase:**
- Interactive feature demonstrations
- Visual feature comparisons
- Mobile app screenshots
- Use case scenarios

**Pricing Section:**
- Clear pricing structure
- Feature comparison table
- Call-to-action buttons
- Value proposition reinforcement

**FAQ Section:**
- Common questions and answers
- Product information
- Support contact information

## Contributing Notes

### Code Standards
- **TypeScript strict mode** enforced
- **Component composition** over inheritance
- **Responsive design** mobile-first approach
- **Accessibility** features and ARIA attributes
- **SEO optimization** for all pages

### Development Workflow
1. Create feature branch from `main`
2. Implement changes with TypeScript
3. Test responsive design on multiple devices
4. Run `npm test` to validate code quality
5. Submit pull request with descriptive commits

### Component Guidelines
- Use Next.js Image component for all images
- Implement proper TypeScript interfaces
- Follow Mantine UI patterns and theming
- Ensure mobile responsiveness
- Add proper meta tags for SEO

### Content Management
- Copy stored in component files for easy editing
- Images optimized and stored in public directory
- Consistent brand voice and messaging
- Regular content updates and improvements

### Performance Optimization
- Static site generation for fast loading
- Image optimization and lazy loading
- Bundle size monitoring and optimization
- Core Web Vitals optimization
- CDN deployment for global performance

### SEO & Analytics
- Proper meta tags and Open Graph data
- Structured data for search engines
- Performance monitoring
- Conversion tracking setup
- Search console integration