# OpenAI Agents SDK Subagent

This subagent specializes in creating and managing OpenAI agents using the OpenAI Agents SDK.

## Overview

The OpenAI Agents SDK Subagent is a specialized agent that can:
- Create and configure OpenAI agents
- Set up agent handoffs between specialized agents
- Implement input/output guardrails
- Run complex agent orchestrations
- Manage the lifecycle of agents

## Capabilities

- `create-agent`: Create new OpenAI agents with custom instructions
- `create-handoff-agent`: Create agents with the ability to transfer to specialists
- `create-guardrail-agent`: Create agents with validation capabilities
- `run-agent-orchestration`: Execute multi-agent workflows
- `add-guardrail-to-agent`: Add content filtering to existing agents
- `create-homework-guardrail`: Implement content-specific filtering
- `create-complex-orchestration`: Manage complex multi-agent scenarios
- `manage-agents`: Track and manage agent lifecycles

## Configuration

The subagent can be configured with:

- `default_model`: Default model to use for agents (default: "gpt-4")
- `max_orchestration_steps`: Maximum steps for orchestrations (default: 10)
- `enable_logging`: Enable detailed logging (default: true)

## Tasks

### `create_agent`
Create a new OpenAI agent with specified parameters.

**Parameters:**
- `name`: Name of the agent (required)
- `instructions`: Instructions for the agent's behavior (required)
- `model`: Model to use for the agent (optional, defaults to gpt-4)
- `handoff_description`: Description for handoff scenarios (optional)

### `create_handoff_agent`
Create an agent with handoff capabilities to other agents.

**Parameters:**
- `name`: Name of the agent (required)
- `instructions`: Instructions for the agent's behavior (required)
- `handoff_targets`: List of agent configurations that this agent can handoff to (required)
- `model`: Model to use for the agent (optional, defaults to gpt-4)

### `create_guardrail_agent`
Create an agent with guardrail functionality for input/output validation.

**Parameters:**
- `name`: Name of the agent (required)
- `instructions`: Instructions for the agent's behavior (required)
- `output_type`: Expected output type for validation (optional)
- `model`: Model to use for the agent (optional, defaults to gpt-4)

### `run_orchestration`
Run an agent orchestration with potential handoffs and guardrails.

**Parameters:**
- `agent_id`: ID of the initial agent to start with (required)
- `user_input`: Input from the user to process (required)
- `max_steps`: Maximum number of steps to execute (optional, defaults to 10)

### `add_guardrail_to_agent`
Add a guardrail function to an existing agent configuration.

**Parameters:**
- `agent_id`: ID of the agent to add guardrail to (required)
- `guardrail_func_name`: Name of the guardrail function to add (required)

### `create_homework_guardrail_for_agent`
Create and add a homework-specific guardrail to an agent.

**Parameters:**
- `agent_id`: ID of the agent to add the homework guardrail to (required)

### `get_agent_info`
Get information about a specific agent.

**Parameters:**
- `agent_id`: ID of the agent to get information for (required)

### `list_agents`
List all registered agents (no parameters required).

## Usage Examples

### Creating an Agent
```
create_agent:
  name: "Math Tutor"
  instructions: "You provide help with math problems. Explain your reasoning at each step and include examples"
  model: "gpt-4"
```

### Creating an Agent with Handoffs
```
create_handoff_agent:
  name: "Triage Agent"
  instructions: "You determine which agent to use based on the user's homework question"
  handoff_targets:
    - name: "History Tutor"
      handoff_description: "Specialist agent for historical questions"
    - name: "Math Tutor"
      handoff_description: "Specialist agent for math questions"
```

### Running an Orchestration
```
run_orchestration:
  agent_id: "abc123"
  user_input: "Solve this equation: 2x + 5 = 15"
  max_steps: 5
```

### Adding a Guardrail
```
add_guardrail_to_agent:
  agent_id: "def456"
  guardrail_func_name: "homework_guardrail"
```

## Dependencies

- `skills.openai_agents_sdk`
- `openai-agents>=0.6.5`
- `pydantic>=2.5.0`

## Installation

The subagent requires the OpenAI Agents SDK skills to be installed. Make sure the skills directory is properly set up with the openai_agents_sdk skill.