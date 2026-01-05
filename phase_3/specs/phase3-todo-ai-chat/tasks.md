# Phase 3: Todo AI Chat - Task Breakdown

## Overview
This document breaks down the implementation tasks for the AI-powered todo chat system into specific, actionable items for both backend and frontend development.

## Backend Tasks

### 1. Database Models
#### 1.1 Create Conversation SQLModel
- Define Conversation model with fields: id, user_id, created_at, updated_at, metadata
- Implement relationships with User and Message models
- Add proper indexing for performance
- Follow existing SQLModel patterns from Phase 2

#### 1.2 Create Message SQLModel
- Define Message model with fields: id, conversation_id, role, content, timestamp, metadata
- Implement relationships with Conversation model
- Add proper indexing for conversation_id and timestamp
- Follow existing SQLModel patterns from Phase 2

### 2. API Implementation
#### 2.1 Build chat router (/api/{user_id}/chat)
- Create Express router for chat endpoints
- Implement POST /api/{user_id}/chat endpoint
- Add authentication and authorization middleware
- Validate request payload and user permissions
- Handle proper error responses

#### 2.2 Fetch conversation history for each request
- Implement function to retrieve conversation history from DB
- Limit results to recent messages for performance
- Format messages for AI context
- Handle pagination if needed

#### 2.3 Save user and AI messages in DB
- Create function to save user messages to database
- Create function to save AI responses to database
- Ensure proper transaction handling
- Handle message ordering and timestamps

### 3. AI Integration
#### 3.1 Setup OpenAI Agent + Runner
- Configure OpenAI API credentials and settings
- Set up OpenAI Agent with appropriate instructions
- Implement runner to process user input and generate responses
- Handle conversation context and history

### 4. MCP Implementation
#### 4.1 Implement MCP server
- Set up MCP server using Official MCP SDK
- Configure server endpoints and authentication
- Implement server lifecycle management
- Add logging and monitoring

#### 4.2 Implement MCP tool: add_task
- Create add_task tool definition
- Map to Phase 2 createTask function
- Handle parameter validation and transformation
- Return appropriate response format

#### 4.3 Implement MCP tool: list_tasks
- Create list_tasks tool definition
- Map to Phase 2 getTasks function
- Handle parameter validation and transformation
- Return appropriate response format

#### 4.4 Implement MCP tool: complete_task
- Create complete_task tool definition
- Map to Phase 2 updateTask function
- Handle parameter validation and transformation
- Return appropriate response format

#### 4.5 Implement MCP tool: delete_task
- Create delete_task tool definition
- Map to Phase 2 deleteTask function
- Handle parameter validation and transformation
- Return appropriate response format

#### 4.6 Implement MCP tool: update_task
- Create update_task tool definition
- Map to Phase 2 updateTask function
- Handle parameter validation and transformation
- Return appropriate response format

## Frontend Tasks

### 1. UI Components
#### 1.1 Setup ChatKit UI components
- Integrate ChatKit or similar chat UI library
- Customize component styling to match application theme
- Implement message bubbles for user and AI
- Add input field with send button

### 2. API Integration
#### 2.1 Connect chat endpoint
- Implement API client for chat endpoint
- Handle authentication headers
- Manage request/response lifecycle
- Implement proper error handling

#### 2.2 Render conversation history
- Fetch and display existing conversation history
- Format messages appropriately (user vs AI)
- Handle message loading states
- Implement infinite scroll if needed

#### 2.3 Display AI responses
- Process and display AI responses in chat format
- Handle streaming responses if applicable
- Format tool call results appropriately
- Show confirmation prompts for actions

#### 2.4 Handle errors and loading indicators
- Display loading states during AI processing
- Show error messages for failed requests
- Implement retry mechanisms
- Provide user feedback for all states

## Implementation Order

### Phase 1: Backend Foundation
1. Create Conversation SQLModel
2. Create Message SQLModel
3. Implement MCP server
4. Implement MCP tools

### Phase 2: Backend API
1. Build chat router
2. Implement conversation history fetching
3. Implement message saving
4. Setup OpenAI Agent + Runner

### Phase 3: Frontend Implementation
1. Setup ChatKit UI components
2. Connect chat endpoint
3. Render conversation history
4. Display AI responses
5. Handle errors and loading indicators

## Dependencies
- Phase 2 task CRUD logic must be available
- Database connection and configuration
- OpenAI API credentials
- MCP SDK installation

## Testing Requirements
- Unit tests for all MCP tools
- Integration tests for chat API
- End-to-end tests for complete conversation flow
- Database transaction tests
- Error handling tests