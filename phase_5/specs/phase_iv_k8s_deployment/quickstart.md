# Quickstart Guide: Advanced Cloud Deployment

## Prerequisites

- Kubernetes cluster (Minikube, AKS, GKE, or OKE)
- kubectl configured to connect to the cluster
- Helm 3.x installed
- Dapr CLI installed
- Docker installed for local development
- Access to container registry (for cloud deployment)

## Local Development Setup

### 1. Initialize Dapr
```bash
dapr init
```

### 2. Clone the repository
```bash
git clone [repository-url]
cd [repository-name]
```

### 3. Set up local development environment
```bash
# Navigate to the infrastructure directory
cd .infra

# Start local development environment with docker-compose
docker-compose up -d
```

### 4. Deploy to local Kubernetes (Minikube)
```bash
# Ensure Minikube is running
minikube start

# Install Dapr in the Kubernetes cluster
dapr init -k

# Navigate to the k8s directory
cd k8s

# Deploy all services
kubectl apply -f dapr/
kubectl apply -f kafka/
kubectl apply -f backend/
kubectl apply -f frontend/
kubectl apply -f mcp-server/
kubectl apply -f monitoring/

# Verify all deployments
kubectl get pods
kubectl get services
kubectl get daprcomponents
```

## Configuration

### Environment Variables
Set the following environment variables:

**Backend (.env):**
```env
DATABASE_URL=postgresql://user:password@neon-postgres:5432/todobot
KAFKA_BROKERS=kafka:9092
DAPR_APP_ID=backend-service
BETTER_AUTH_SECRET=your-jwt-secret
```

**MCP Server (.env):**
```env
DAPR_APP_ID=mcp-server
KAFKA_BROKERS=kafka:9092
```

### Dapr Components
The following Dapr components are configured:

**pubsub.yaml:**
- Kafka pub/sub for event-driven communication
- Used for task events, reminders, and updates

**statestore.yaml:**
- State management for conversation history
- Redis or compatible store

**secrets.yaml:**
- Secure storage for credentials
- Integration with Kubernetes secrets

## Building and Deploying

### 1. Build container images
```bash
# Build backend image
docker build -t todo-backend:latest ./backend

# Build frontend image
docker build -t todo-frontend:latest ./frontend

# Build MCP server image
docker build -t mcp-server:latest ./mcp-server
```

### 2. Tag and push images (for cloud deployment)
```bash
# Tag images for your registry
docker tag todo-backend:latest your-registry/todo-backend:latest
docker tag todo-frontend:latest your-registry/todo-frontend:latest
docker tag mcp-server:latest your-registry/mcp-server:latest

# Push to registry
docker push your-registry/todo-backend:latest
docker push your-registry/todo-frontend:latest
docker push your-registry/mcp-server:latest
```

### 3. Update Helm values
Edit `k8s/values.yaml` to update image tags:
```yaml
backend:
  image:
    repository: your-registry/todo-backend
    tag: latest

frontend:
  image:
    repository: your-registry/todo-frontend
    tag: latest

mcpServer:
  image:
    repository: your-registry/mcp-server
    tag: latest
```

## Event-Driven Architecture

### Kafka Topics
The system uses the following Kafka topics:
- `task-events` - Task creation, updates, completion
- `reminders` - Reminder scheduling and notifications
- `task-updates` - Task synchronization events

### Event Schema
All events follow this schema:
```json
{
  "event_type": "created|updated|completed|deleted|reminder",
  "task_id": "uuid",
  "timestamp": "ISO8601",
  "payload": {...}
}
```

## Testing

### Unit Tests
```bash
# Backend tests
cd backend
pytest tests/unit

# MCP server tests
cd mcp-server
pytest tests/unit
```

### Integration Tests
```bash
# Run integration tests
cd backend
pytest tests/integration

# Contract tests
cd backend
pytest tests/contract
```

## Monitoring and Observability

### Metrics
- Prometheus endpoint: `http://localhost:9090`
- Grafana dashboard: `http://localhost:3000`
- Dapr metrics available at each service's `/metrics` endpoint

### Logs
- View all logs: `kubectl get pods -o name | xargs -I {} kubectl logs {}`
- View Dapr logs: `dapr logs`

### Health Checks
- Backend health: `http://<backend-service>/health`
- MCP server health: `http://<mcp-service>/health`
- Dapr health: `http://localhost:3500/v1.0/healthz`

## Troubleshooting

### Common Issues
1. **Pods stuck in Pending state**: Check if Dapr is installed in the cluster
2. **Service unavailable**: Verify Dapr sidecars are injected properly
3. **Database connection errors**: Check if Neon PostgreSQL is accessible
4. **Event processing failures**: Check Kafka connectivity and topic existence

### Useful Commands
```bash
# Check Dapr status
dapr status -k

# List Dapr components
dapr components -k

# View sidecar logs
kubectl logs <pod-name> daprd

# Debug Dapr configuration
dapr configurations -k
```