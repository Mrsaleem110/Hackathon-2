<!-- SYNC IMPACT REPORT -->
<!-- Version change: N/A → 1.0.0 -->
<!-- Modified principles: None (new constitution) -->
<!-- Added sections: Core Identity & Purpose, Architecture Integrity, Technology Stack, Security & Compliance, Performance Standards, Testing & Quality, Deployment Requirements, Governance -->
<!-- Removed sections: None -->
<!-- Templates requiring updates: ⚠ pending - plan-template.md, spec-template.md, tasks-template.md -->
<!-- Follow-up TODOs: RATIFICATION_DATE needs to be set -->

# AI-Powered Todo Chatbot Constitution

## Core Identity & Purpose
This project is an AI-powered todo management chatbot enabling natural language task management with advanced cloud-native features. The system follows a three-tier architecture with event-driven patterns.

## Non-Negotiable Principles

### 1. Architecture Integrity
- **Three-Tier Separation**: Frontend (ChatKit UI), Backend (FastAPI), MCP Server must remain decoupled
- **Event-Driven Core**: All major operations must publish events to Kafka/Redpanda
- **Dapr-First Integration**: Use Dapr building blocks instead of direct client libraries
- **Stateless Design**: Backend services must remain stateless; state goes to Dapr or Neon

### 2. Technology Stack (Locked)
- **Frontend**: OpenAI ChatKit UI (Node.js) - Deployed as static assets
- **Backend**: FastAPI (Python) - Serverless/Vercel ready
- **MCP Server**: Official MCP SDK (Python) - Containerized
- **Database**: Neon PostgreSQL with SQLModel ORM
- **Event Streaming**: Kafka/Redpanda (Cloud or Self-hosted)
- **Runtime**: Dapr sidecar for all services
- **Orchestration**: Kubernetes (Minikube local → AKS/GKE/OKE cloud)

### 3. Security & Compliance
- Authentication via BETTER_AUTH with JWT tokens
- All secrets in Dapr secret store or Kubernetes secrets
- No hardcoded credentials in code or environment files
- TLS for all external communications

### 4. Performance Standards
- Async/await pattern throughout Python code
- Database queries optimized with proper indexing
- Event publishing non-blocking
- Reminder accuracy within 1 second (using Dapr Jobs API)

### 5. Testing & Quality
- Minimum 80% test coverage (pytest)
- All Kafka event schemas validated
- Error handling for all async operations
- Structured logging for all services

### 6. Deployment Requirements
- Local: Minikube with Dapr fully configured
- Cloud: AKS/GKE/OKE with production-grade setup
- CI/CD: GitHub Actions automated pipeline
- Monitoring: Basic metrics and logging configured

## Governance
Constitution supersedes all other practices. All major changes must comply with these principles. Amendments require proper documentation and approval process.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): Original adoption date needed | **Last Amended**: 2026-02-17