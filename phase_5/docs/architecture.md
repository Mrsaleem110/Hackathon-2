# Architecture Overview

This document provides an overview of the system architecture for the AI-Powered Todo Chatbot with Advanced Cloud Deployment features.

## System Components

### Backend Services
- **Main Backend** (`/backend`): FastAPI application handling core business logic, task management, and API endpoints
- **Recurring Task Service** (`/services/recurring`): Handles processing of completed recurring tasks and creation of new occurrences
- **Notification Service** (`/services/notification`): Manages reminder notifications and delivery across multiple channels

### Frontend
- **React UI** (`/frontend`): ChatKit-based interface with advanced task management features including recurrence, filtering, and search

### Infrastructure Components
- **Dapr (Distributed Application Runtime)**: Provides building blocks for microservices including pub/sub, state management, and service invocation
- **Kafka/Redpanda**: Event streaming platform for asynchronous communication between services
- **PostgreSQL**: Primary database for task and user data storage
- **Kubernetes**: Container orchestration platform for deployment and scaling

## Event-Driven Architecture

The system uses an event-driven architecture with the following key components:

### Event Publishers
- Main backend publishes task events (created, updated, completed, deleted)
- Recurring task events are published when recurrence patterns are processed
- Reminder events are published when tasks have scheduled reminders

### Event Consumers
- **Recurring Task Service**: Consumes task completion events to create new recurring task occurrences
- **Notification Service**: Consumes reminder events to deliver notifications to users
- **Audit Service**: Consumes all events for logging and compliance

### Event Schema
```json
{
  "event_type": "created|updated|completed|deleted|reminder|recurring",
  "task_id": "uuid",
  "user_id": "string",
  "timestamp": "ISO datetime",
  "payload": {
    "title": "string",
    "description": "string",
    "priority": "high|medium|low",
    "due_date": "ISO datetime",
    "tags": ["string"],
    "recurrence_info": {
      "has_recurrence": "boolean",
      "series_id": "uuid"
    }
  },
  "version": "1.0.0"
}
```

## Deployment Architecture

### Kubernetes Deployments
- Each service runs in its own Kubernetes deployment with Dapr sidecar
- Services communicate via Dapr service invocation
- Configuration and secrets are managed through Kubernetes ConfigMaps and Secrets

### Dapr Configuration
- Pub/Sub component configured for Kafka/Redpanda
- State store component configured for PostgreSQL
- Service invocation enabled for inter-service communication
- Tracing enabled for observability

## Security Architecture

### Authentication
- JWT-based authentication using BETTER_AUTH
- API endpoints secured with authentication middleware
- Dapr secrets store for credential management

### Data Protection
- All sensitive data stored in encrypted format
- Connection to database and external services via TLS
- Secrets managed through Dapr and Kubernetes secret stores

## Scalability Considerations

### Horizontal Pod Autoscaling
- Deployments configured with HPA based on CPU and memory metrics
- Event consumers can be scaled independently based on queue depth

### Database Scaling
- PostgreSQL configured for connection pooling
- Read replicas for read-heavy operations
- Proper indexing for search and filter operations

## Monitoring and Observability

### Logging
- Structured logging across all services
- Centralized log aggregation
- Correlation IDs for request tracing

### Metrics
- Application-level metrics exposed via Prometheus
- Kubernetes infrastructure metrics
- Dapr-specific metrics for service communication

## Development Workflow

### Local Development
- Docker Compose for local development environment
- Dapr configured for local Kubernetes mode
- Hot-reloading enabled for faster development cycles

### Testing Strategy
- Unit tests for all business logic
- Integration tests for service communication
- End-to-end tests for critical user flows
- Contract tests for API endpoints