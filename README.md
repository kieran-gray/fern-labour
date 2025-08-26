# Fern Labour

> **Peace of mind for you. Presence for them.**

Fern Labour empowers expectant mothers to effortlessly plan and track their labour while seamlessly sharing updates with loved ones. Our platform ensures that distance never diminishes the connection during life's most precious moments, providing both comfort to mothers and meaningful participation for their support network.

## 🌿 Our Mission

At Fern Labour, we believe that every expectant mother deserves the peace of mind that comes from being connected to their loved ones during childbirth. Whether your support network is across the room or across the world, we enable real-time sharing of your journey while maintaining complete control over your privacy and information.

Our platform eliminates the stress of constant messaging during labour, replacing it with automated, intelligent updates that keep everyone informed without overwhelming the mother. From the first contraction to the joyful announcement of arrival, we ensure your loved ones feel present for every meaningful moment.

## ✨ Key Features

### 🕐 **Intelligent Contraction Tracking**
- **Automated hospital readiness alerts** based on clinical patterns (3-1-1 for first-time mothers, 5-1-1 for experienced mothers)
- **Precise timing and pattern analysis** to help you know when labour is progressing
- **One-tap status sharing** eliminates the need for constant manual updates

### 📱 **Multi-Channel Real-Time Notifications**  
- **SMS, WhatsApp, and Email delivery** ensures messages reach loved ones on their preferred platform
- **Live updates during labour progression** keep everyone connected to your journey
- **Customizable notification preferences** for different stages of labour

### 👥 **Complete Subscriber Control**
- **Invite, approve, or remove loved ones at will** - you decide who stays informed
- **Granular privacy controls** let you share exactly what you want, when you want
- **Subscriber management dashboard** for easy oversight of your support network

### 🔒 **Privacy & Data Security Focus**
- **Encrypted data storage on secure UK servers** ensures your information stays protected
- **SSL encryption for all data transmission** protects your updates in transit
- **Full user control including data deletion** - your data, your choice
- **Subscriber approval required** - no unwanted access to your information

### 💚 **Mother-Centric Pricing**
- **Free accounts for mothers** - essential features at no cost
- **Free basic subscriptions for loved ones** - staying connected shouldn't cost extra
- **Optional enhanced notifications (£2.50)** for real-time updates and extended features

## 🏗️ Monorepo Architecture

This repository contains a complete microservices ecosystem built with modern technologies and domain-driven design principles:

```
fern-labour/
├── labour_service/          # Core labour tracking and subscription management
├── contact_service/         # Customer support and messaging
├── notification_service/    # Multi-channel notification delivery
├── frontend/               # React web application
├── marketing/              # Next.js marketing website
├── keycloak/               # Authentication and authorization
├── dev/                    # Development utilities and database scripts
└── docker-compose.yml      # Full-stack orchestration
```

### Service Ecosystem

**🏥 labour_service** - *The heart of the platform*  
Manages the complete labour lifecycle including contraction tracking, clinical pattern analysis, subscriber relationships, and payment processing. Implements intelligent alerting based on established medical guidelines and handles the complex business logic of labour progression monitoring.

**📞 contact_service** - *Customer connection hub*  
Processes "Contact Us" form submissions from the marketing site and internal support requests. Integrates with Slack for instant team notifications and includes Cloudflare Turnstile protection against spam and abuse.

**📨 notification_service** - *Communication orchestrator*  
Handles templated message generation and delivery across SMS, WhatsApp, and email channels. Features retry logic, delivery status tracking, and CLI tools for notification management. Integrates with Twilio and SMTP providers for reliable message delivery.

**💻 frontend** - *The mother's digital companion*  
A responsive React SPA providing an intuitive interface for labour tracking, contraction monitoring, subscriber management, and real-time updates. Features QR code generation for easy partner invites and comprehensive labour history visualization.

**🌐 marketing** - *The welcoming front door*  
A high-performance Next.js static site showcasing Fern Labour's value proposition, featuring interactive animations, comprehensive FAQ, pricing information, and integrated contact forms that connect directly to the platform ecosystem.

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** - Container orchestration
- **Google Cloud SDK** - For private package registry authentication
- **Node.js 18+** - For frontend development
- **Python 3.12+** - For backend services

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fern-labour
   ```

2. **Authenticate with Google Cloud** (for private dependencies)
   ```bash
   gcloud auth login
   gcloud init
   gcloud auth application-default login
   ```

3. **Configure environment variables**
   ```bash
   # Copy environment templates
   cp .env.example .env
   cp labour_service/.env.example labour_service/.env
   cp contact_service/.env.example contact_service/.env
   cp notification_service/.env.example notification_service/.env
   ```

4. **Set up local DNS** (for Keycloak integration)
   ```bash
   echo "127.0.0.1 keycloak" >> /etc/hosts
   ```

5. **Launch the full stack**
   ```bash
   make run
   ```

### Access Points

Once running, the platform will be available at:

- **Frontend Application**: http://localhost:5173
- **Marketing Site**: http://localhost:3000  
- **Labour Service API**: http://localhost:8000
- **Contact Service API**: http://localhost:8002
- **Notification Service API**: http://localhost:8001
- **Keycloak Authentication**: http://localhost:8080
- **MailCatcher (Dev Email)**: http://localhost:1080

## 🛠️ Detailed Service Architecture

### Labour Service (Port 8000)
**Core Business Logic & Data Management**

- **Labour Session Management**: Complete lifecycle from onset to completion
- **Contraction Analysis**: Pattern recognition and hospital readiness alerts
- **Subscriber Relationships**: Invitation, approval, and management workflows
- **Payment Integration**: Stripe-powered subscription handling
- **Clinical Intelligence**: 3-1-1 and 5-1-1 pattern detection algorithms

*Technologies*: FastAPI, SQLAlchemy, Dishka DI, Stripe, Keycloak, PostgreSQL

### Contact Service (Port 8002)  
**Customer Support & Communication Gateway**

- **Form Processing**: Multi-category contact form handling
- **Spam Protection**: Cloudflare Turnstile integration
- **Team Notifications**: Slack webhook integration for instant alerts
- **Message Storage**: Encrypted contact history and follow-up tracking

*Technologies*: FastAPI, PostgreSQL, Slack SDK, Cloudflare Turnstile

### Notification Service (Port 8001)
**Multi-Channel Message Delivery**

- **Template Engine**: Jinja2-powered dynamic content generation
- **Channel Management**: SMS (Twilio), WhatsApp (Twilio), Email (SMTP)
- **Delivery Tracking**: Status monitoring, retry logic, and failure handling
- **CLI Management**: Administrative tools for notification oversight

*Technologies*: FastAPI, Twilio SDK, Jinja2, PostgreSQL, SMTP

### Frontend (Port 5173)
**Mother's Digital Experience**

- **Labour Tracking**: Real-time contraction timer and progress visualization
- **Subscriber Management**: Invite generation, QR codes, and relationship control
- **History & Analytics**: Comprehensive labour session analysis and charts
- **Mobile-First Design**: Responsive interface optimized for all devices

*Technologies*: React 18, TypeScript, Vite, Mantine UI, React Query, Recharts

### Marketing Site (Port 3000)
**Brand Presence & Conversion**

- **Landing Experience**: Hero sections, feature showcases, and testimonials
- **Contact Integration**: Direct connection to contact service with spam protection
- **SEO Optimization**: Static generation for search engine performance
- **Performance Focus**: Optimized loading and Core Web Vitals

*Technologies*: Next.js 15, TypeScript, Static Export, Mantine UI

## 🔧 Environment Variables & Configuration

### Core Platform Configuration

```bash
# Database & Infrastructure
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<secure-password>
DATABASE_ENCRYPTION_KEY=<encryption-key>

# Authentication (Keycloak)
KEYCLOAK_SERVER_URL=http://keycloak:8080
KEYCLOAK_REALM=labour_tracker
KEYCLOAK_CLIENT_ID=labour_tracker_backend
KEYCLOAK_CLIENT_SECRET=<client-secret>

# Event Messaging (PubSub)
GCP_PROJECT_ID=test
PUBSUB_EMULATOR_HOST=pub-sub-emulator:8085
```

### Notification Service Configuration

```bash
# SMS & WhatsApp (Twilio)
TWILIO_ACCOUNT_SID=<account-sid>
TWILIO_AUTH_TOKEN=<auth-token>
SMS_FROM_NUMBER=<twilio-phone-number>
MESSAGING_SERVICE_SID=<service-sid>

# Email Delivery (SMTP)
SMTP_HOST=<smtp-server>
SMTP_PORT=587
SMTP_USER=<smtp-username>
SMTP_PASSWORD=<smtp-password>
EMAILS_FROM_EMAIL=noreply@fernlabour.com
```

### Contact Service Configuration

```bash
# Slack Integration
SLACK_ALERT_BOT_TOKEN=<bot-token>
SLACK_ALERT_BOT_CHANNEL=#support

# Spam Protection
CLOUDFLARE_SECRET_KEY=<turnstile-secret>
CLOUDFLARE_URL=https://challenges.cloudflare.com/turnstile/v0/siteverify
```

### Frontend Configuration

```bash
# API Endpoints
VITE_LABOUR_SERVICE_URL=http://localhost:8000
VITE_CONTACT_SERVICE_URL=http://localhost:8002

# Authentication
VITE_KEYCLOAK_AUTHORITY=http://localhost:8080/realms/labour_tracker
VITE_KEYCLOAK_CLIENT_ID=labour_tracker_frontend

# Spam Protection
VITE_CLOUDFLARE_SITEKEY=<turnstile-site-key>
```

### Security & Privacy Considerations

- **Data Encryption**: All sensitive data encrypted at rest using secure keys
- **UK Server Hosting**: Ensures GDPR compliance and data sovereignty  
- **SSL/TLS**: All communications encrypted in transit
- **Access Controls**: Role-based permissions and subscriber approval workflows
- **Data Retention**: User-controlled data deletion and privacy management

## 🧪 Testing & Quality Assurance

### Service Testing

```bash
# Python Services (labour_service, contact_service, notification_service)
cd <service-directory>
make test          # Run full test suite with coverage
make check         # Run linting, type checking, and tests
make lint          # Code quality checks only

# Frontend
cd frontend/
npm test           # Jest tests, linting, and type checking
npm run typecheck  # TypeScript validation only

# Marketing
cd marketing/  
npm test           # Linting and type checking
```

### Code Quality Standards

- **100% test coverage** requirement for all Python services
- **TypeScript strict mode** enforced across frontend applications
- **Domain-driven design** patterns with comprehensive unit testing
- **Integration tests** for cross-service communication
- **End-to-end testing** for critical user workflows

### CI/CD Pipeline Considerations

- **Automated testing** on all pull requests
- **Security scanning** for dependencies and vulnerabilities  
- **Docker image optimization** for production deployments
- **Database migration testing** in staging environments
- **UK-based deployment** infrastructure for compliance

## 📞 Support & Community

For questions, issues, or contributions:

- **Technical Issues**: Create an issue in this repository
- **Feature Requests**: Submit via our contact form at [fernlabour.com/contact](https://fernlabour.com/contact)
- **Security Concerns**: Email security@fernlabour.com
- **General Inquiries**: Contact us through our website
