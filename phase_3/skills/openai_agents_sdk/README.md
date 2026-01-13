# OpenAI Agents SDK Skills

This module provides skills for creating and managing OpenAI agents using the OpenAI Agents SDK.

## Overview

The OpenAI Agents SDK skills provide a comprehensive set of tools for:
- Creating and configuring OpenAI agents
- Setting up agent handoffs between specialized agents
- Implementing input/output guardrails
- Running complex agent orchestrations

## Skills

### `create_openai_agent`
Create a new OpenAI agent with specified parameters.

**Parameters:**
- `name`: Name of the agent
- `instructions`: Instructions for the agent's behavior
- `model`: Model to use for the agent (optional, defaults to gpt-4)
- `handoff_description`: Description for handoff scenarios (optional)
- `tools`: List of tools available to the agent (optional)

### `create_openai_handoff_agent`
Create an agent with handoff capabilities to other agents.

**Parameters:**
- `name`: Name of the agent
- `instructions`: Instructions for the agent's behavior
- `handoff_targets`: List of agent configurations that this agent can handoff to
- `model`: Model to use for the agent (optional, defaults to gpt-4)

### `create_openai_guardrail_agent`
Create an agent with guardrail functionality for input/output validation.

**Parameters:**
- `name`: Name of the agent
- `instructions`: Instructions for the agent's behavior
- `output_type`: Expected output type for validation (optional)
- `model`: Model to use for the agent (optional, defaults to gpt-4)

### `run_openai_agent_orchestration`
Run an agent orchestration with potential handoffs and guardrails.

**Parameters:**
- `initial_agent`: Configuration of the initial agent to start with
- `user_input`: Input from the user to process
- `max_steps`: Maximum number of steps to execute (prevents infinite loops)

### `add_guardrail_to_openai_agent`
Add a guardrail function to an existing agent configuration.

**Parameters:**
- `agent_config`: Existing agent configuration to add guardrail to
- `guardrail_func_name`: Name of the guardrail function to add

### `create_homework_guardrail`
Create and add a homework-specific guardrail to an agent.

**Parameters:**
- `agent_config`: Agent configuration to add the homework guardrail to

### `create_complex_agent_orchestration`
Run a complex agent orchestration with multiple agents, handoffs, and guardrails.

**Parameters:**
- `agents`: List of agent configurations
- `user_input`: Input from the user to process
- `max_steps`: Maximum number of steps to execute (prevents infinite loops)

## Examples

### Creating a Simple Agent
```python
from skills.openai_agents_sdk.openai_agent_skills import create_openai_agent

agent_result = await create_openai_agent(
    name="Math Tutor",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
    model="gpt-4"
)
```

### Creating an Agent with Handoffs
```python
from skills.openai_agents_sdk.openai_agent_skills import create_openai_handoff_agent

triage_result = await create_openai_handoff_agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoff_targets=[
        {
            "name": "History Tutor",
            "handoff_description": "Specialist agent for historical questions"
        },
        {
            "name": "Math Tutor",
            "handoff_description": "Specialist agent for math questions"
        }
    ]
)
```

### Adding a Guardrail
```python
from skills.openai_agents_sdk.openai_agent_skills import create_homework_guardrail

guarded_agent = await create_homework_guardrail(agent_config=triage_result["agent_config"])
```

### Running an Orchestration
```python
from skills.openai_agents_sdk.openai_agent_skills import run_openai_agent_orchestration

orchestration_result = await run_openai_agent_orchestration(
    initial_agent=guarded_agent["updated_agent_config"],
    user_input="who was the first president of the united states?",
    max_steps=5
)
```

## Dependencies

- `openai-agents>=0.6.5`
- `pydantic>=2.5.0`

## Installation

```bash
pip install -r requirements.txt
```

## Testing

Run the example implementation:

```bash
python openai_agent_skills.py
```