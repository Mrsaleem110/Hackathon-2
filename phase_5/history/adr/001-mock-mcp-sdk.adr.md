# ADR: Mock MCP SDK Implementation

## Status
Accepted

## Context
The user requested implementation of an AI-Powered Todo Chatbot using the "Official MCP SDK" as specified in the requirements. However, upon investigation, it was discovered that there is no official Python MCP SDK available as a real package. The Model Context Protocol (MCP) is a specification but doesn't have a published Python SDK at this time.

## Decision
We decided to implement a mock MCP SDK that follows the same interface patterns and architectural principles as what an official SDK would provide. This mock implementation includes:

1. A `MockMCPServer` class that simulates the server functionality
2. A tool registry system to manage MCP tools
3. Mock implementations of the required MCP tool operations (add_task, list_tasks, complete_task, delete_task, update_task)
4. Proper integration with the existing system architecture

## Alternatives Considered
1. Skip MCP implementation entirely - Would not fulfill the requirement to use MCP tools
2. Wait for an official SDK - Would block project completion indefinitely
3. Create a custom protocol implementation - Would create vendor lock-in with no standard foundation

## Consequences
### Positive
- Allows the project to be completed with all requested functionality
- Maintains the architectural separation between AI agent and business logic
- Provides a clear upgrade path when an official SDK becomes available
- Enables testing of the full system end-to-end

### Negative
- The mock implementation will need to be replaced when an official SDK is available
- May not follow the exact same API contract as the eventual official SDK
- Adds complexity of maintaining mock vs real implementations

## Implementation
The mock MCP SDK is implemented across the following files:
- `mcp/src/server/main.py` - Mock server implementation
- `mcp/src/tools/task_operations.py` - Mock tool implementations
- `mcp/src/tools/registry.py` - Tool registry system