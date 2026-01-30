# Tasks: Authentication Fixes for Chat Messaging

## Feature: Authentication Fixes for Chat Messaging
**Directory**: `specs/003-auth-fixes` | **Priority**: High | **Status**: Planned

## Phase 1: Setup Tasks
- [ ] T001 Create tasks file per implementation plan
- [ ] T002 Review existing auth implementation in frontend and backend
- [ ] T003 Identify current auth session resolution issues

## Phase 2: Foundational Tasks
- [X] T010 [P] Update AuthContext to ensure user.id availability before ChatKit initialization
- [X] T011 [P] Create utility functions for JWT payload normalization in backend
- [X] T012 [P] Add environment variable validation for both frontend and backend

## Phase 3: [US1] Fix frontend auth session resolution
- [X] T020 [US1] Update AuthContext.jsx to verify user.id exists before marking as authenticated
- [X] T021 [P] [US1] Modify useAuth hook to return additional verification for user.id presence
- [X] T022 [P] [US1] Update ProtectedRoute component to wait for complete auth state resolution
- [X] T023 [US1] Modify App.jsx routing to ensure user.id is available before mounting ChatInterface
- [X] T024 [US1] Add loading state to ChatInterface while auth state resolves
- [X] T025 [US1] Create test to verify user.id is available before ChatInterface renders

## Phase 4: [US2] Block ChatKit sendMessage if userId is null
- [X] T030 [US2] Update ChatInterface.jsx to check userId availability before sending messages
- [X] T031 [P] [US2] Add early return in sendMessage function if userId is null/undefined
- [X] T032 [P] [US2] Implement error state display when userId is missing
- [X] T033 [US2] Add console warning when sendMessage is called without userId
- [X] T034 [US2] Create unit test for sendMessage with null userId scenario
- [X] T035 [US2] Add user-friendly error message when auth fails during chat

## Phase 5: [US3] Inject userId explicitly into chat payload
- [X] T040 [US3] Modify ChatInterface.jsx to include userId in all chat API requests
- [X] T041 [P] [US3] Update OpenAIChatKitUI.jsx to ensure userId is passed in request payload
- [X] T042 [P] [US3] Verify chat endpoint URL construction includes userId parameter
- [X] T043 [US3] Add validation to ensure userId is included in all chat request bodies
- [X] T044 [US3] Create integration test for chat API with userId validation
- [X] T045 [US3] Update API documentation to reflect userId inclusion requirement

## Phase 6: [US4] Normalize JWT decoding in FastAPI
- [X] T050 [US4] Update backend auth.py to normalize JWT payload structure
- [X] T051 [P] [US4] Create JWT utility functions to handle different payload formats (sub vs user_id)
- [X] T052 [P] [US4] Modify require_auth middleware to consistently extract user ID
- [X] T053 [US4] Add JWT payload validation to ensure required fields exist
- [X] T054 [US4] Update token creation to include consistent user identification fields
- [X] T055 [US4] Create test suite for JWT decoding and validation

## Phase 7: [US5] Validate env vars on Vercel (FRONTEND + BACKEND)
- [X] T060 [US5] Create environment validation script for backend deployment
- [X] T061 [P] [US5] Add frontend environment validation for Vercel deployment
- [X] T062 [P] [US5] Update vercel.json to ensure proper environment variable handling
- [X] T063 [US5] Create deployment checklist for auth environment variables
- [X] T064 [US5] Add runtime environment validation in both frontend and backend
- [X] T065 [US5] Document environment variable requirements for Vercel deployment

## Phase 8: Testing & Validation
- [X] T070 [P] Create end-to-end test for complete auth flow before chat messaging
- [X] T071 [P] Add integration tests for JWT validation and user ID extraction
- [X] T072 Test error handling when userId is missing from various scenarios
- [X] T073 Validate that all auth guards work as expected in production
- [X] T074 Deploy to Vercel and verify auth fixes work in production

## Phase 9: Polish & Cross-Cutting Concerns
- [X] T080 Update documentation to reflect auth fixes implementation
- [X] T081 Add error logging for auth-related issues
- [X] T082 Create monitoring for auth failures
- [X] T083 Clean up deprecated auth code if any
- [X] T084 Update README with auth troubleshooting guide

## Dependencies
- User Story 1 (Frontend auth session resolution) must be completed before User Story 2 (Block ChatKit sendMessage)
- User Story 4 (JWT normalization) should be completed before User Story 3 (Inject userId explicitly)
- User Story 5 (Env var validation) can be done in parallel with other stories

## Parallel Execution Examples
- T020-T025 can run in parallel with T030-T035 (different components)
- T050-T055 can run in parallel with T060-T065 (backend vs deployment)
- T010-T012 foundational tasks should complete before user stories begin

## Implementation Strategy
- **MVP Scope**: Complete User Story 1 (frontend auth session resolution) and User Story 2 (block sendMessage if null)
- **Incremental Delivery**: Each user story provides value independently, can be deployed separately
- **Validation Points**: Each phase includes tests to verify correctness before proceeding