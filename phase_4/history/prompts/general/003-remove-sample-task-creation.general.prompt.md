---
id: "003"
title: "Remove sample task creation from fallback API"
stage: "general"
date_iso: "2026-02-02"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "Chohan Laptop's"
command: "remove-sample-tasks"
labels: ["tasks", "cleanup", "bug-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "backend/vercel_api.py"
tests_yaml: []
---

# Remove sample task creation from fallback API

## User Request
User reported that sample tasks were appearing in the dashboard with the message "Task service temporarily unavailable. Please configure environment variables in Vercel dashboard."

## Analysis
Found that the fallback API in `vercel_api.py` was returning sample tasks from the POST `/tasks` endpoint instead of proper responses. This was causing sample data to appear in the UI.

## Changes Made

### 1. Fixed POST /tasks endpoint
- Changed from returning a sample task with title "Sample Task" to returning a proper structure without sample data
- Maintained the error message for configuration issues but removed sample task data

### 2. Fixed PUT /tasks/{task_id} endpoint
- Changed from returning "Updated Sample Task" to returning empty title
- Maintained functionality while removing sample data

### 3. Kept GET /tasks endpoint unchanged
- Already returning empty array which is correct behavior

## Outcome
- ✅ Sample tasks no longer appear in dashboard
- ✅ Proper error messages maintained for configuration issues
- ✅ API response structure preserved for frontend compatibility
- ✅ No more "Sample Task" appearing in UI

## Evaluation
The sample task issue has been resolved. The API will no longer inject sample task data while still providing appropriate error messages for configuration issues.