from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime

from ..database.connection import get_session
from ..models.conversation import Conversation
from ..models.message import Message, MessageCreate, MessageRole
from ..models.task import Task
from ..services.conversation_service import ConversationService
from ..services.message_service import MessageService
try:
    from ..agents.chat_agent import ChatAgent
    CHAT_AGENT_AVAILABLE = True
except ImportError as e:
    print(f"WARNING: ChatAgent could not be imported: {e}")
    print("Chat functionality will be limited.")
    CHAT_AGENT_AVAILABLE = False
except Exception as e:
    print(f"WARNING: Error importing ChatAgent: {e}")
    print("Chat functionality will be limited.")
    CHAT_AGENT_AVAILABLE = False
from ..auth import get_current_user, require_auth, User

router = APIRouter()

@router.post("/api/{user_id}/chat")
async def chat_endpoint(
    user_id: str,
    request: Dict[str, Any],
    current_user: User = Depends(require_auth()),
    session: Session = Depends(get_session)
):
    """
    Process a chat message and return AI response with tool calls.
    """
    try:
        # Ensure the authenticated user matches the user_id in the path
        if current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You can only access your own conversations"
            )

        # Additionally, verify user_id from request payload matches for extra security
        request_user_id = request.get("user_id")
        if request_user_id and request_user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: User ID in request payload does not match path parameter"
            )

        # Extract message and conversation_id from request
        message_content = request.get("message")
        if not message_content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message content is required"
            )

        conversation_id_str = request.get("conversation_id")
        conversation_id = None
        if conversation_id_str:
            try:
                conversation_id = uuid.UUID(conversation_id_str)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid conversation_id format"
                )

        # Get or create conversation
        if conversation_id:
            conversation = session.get(Conversation, conversation_id)
            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found"
                )
            if conversation.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied to this conversation"
                )
        else:
            # Create new conversation
            conversation_create = Conversation(user_id=user_id)
            conversation = ConversationService.create_conversation(session, conversation_create)
            conversation_id = conversation.id

        # Create user message
        user_message = MessageCreate(
            conversation_id=conversation_id,
            user_id=user_id,
            role=MessageRole.USER,
            content=message_content
        )
        MessageService.create_message(session, user_message)

        # Get recent conversation history for context
        recent_messages = MessageService.get_recent_messages_by_conversation(session, conversation_id, limit=10)
        conversation_history = []
        for msg in recent_messages:
            conversation_history.append({
                "role": msg.role.value,
                "content": msg.content
            })

        # Process message with AI agent
        if CHAT_AGENT_AVAILABLE:
            try:
                agent = ChatAgent()
                result = agent.process_message(message_content, user_id, conversation_history)

                # Debug logging to see what the AI agent returns
                print(f"DEBUG: AI Agent result for message '{message_content}': {result}")

                # Store original response to potentially modify after tool execution
                original_response = result["response"]
            except Exception as e:
                print(f"ERROR: Failed to process message with AI agent: {e}")
                # Fallback response if AI agent fails
                result = {
                    "response": f"I received your message: '{message_content}'. [AI Agent temporarily unavailable]",
                    "tool_calls": []
                }
        else:
            # Fallback response if ChatAgent is not available
            result = {
                "response": f"I received your message: '{message_content}'. [AI functionality currently unavailable]",
                "tool_calls": []
            }

        # Execute any tool calls returned by the AI agent
        print(f"DEBUG: Checking for tool calls in result: {result['tool_calls']}")
        if result["tool_calls"]:
            tool_executions = []  # Track what tools were executed for response generation

            for tool_call in result["tool_calls"]:
                tool_name = tool_call["name"]
                tool_args = tool_call["arguments"]
                print(f"DEBUG: Processing tool call - Name: {tool_name}, Args: {tool_args}")

                # Ensure user_id matches for security
                if tool_args.get("user_id") != user_id:
                    continue  # Skip this tool call if user_id doesn't match

                try:
                    if tool_name == "add_task":
                        from ..services.task_service import TaskService
                        from ..models.task import TaskCreate

                        print(f"DEBUG: Attempting to create task with args: {tool_args}")

                        task_create = TaskCreate(
                            title=tool_args["title"],
                            description=tool_args.get("description", ""),
                            user_id=user_id,
                            completed=False
                        )
                        created_task = TaskService.create_task(session, task_create)
                        print(f"DEBUG: Successfully created task with ID: {created_task.id}, Title: {created_task.title}")

                        tool_executions.append({
                            "name": "add_task",
                            "success": True,
                            "task_title": created_task.title,
                            "task_id": str(created_task.id)
                        })

                    elif tool_name == "list_tasks":
                        from ..services.task_service import TaskService

                        print(f"DEBUG: Attempting to list tasks for user: {user_id}")
                        user_tasks = TaskService.get_tasks_by_user(session, user_id)

                        # Format tasks for the AI to include in its response
                        if user_tasks:
                            task_list_text = "Here are your current tasks:\n"
                            for task in user_tasks:
                                status = "✓ Completed" if task.completed else "○ Pending"
                                task_list_text += f"- [{status}] {task.title}"
                                if task.description:
                                    task_list_text += f": {task.description}"
                                task_list_text += f" (ID: {task.id})\n"
                        else:
                            task_list_text = "You don't have any tasks yet."

                        # Update the result response to include the task list
                        result["response"] = task_list_text
                        tool_executions.append({
                            "name": "list_tasks",
                            "success": True,
                            "task_count": len(user_tasks)
                        })
                        print(f"DEBUG: Listed {len(user_tasks)} tasks for user")

                    elif tool_name == "complete_task":
                        from ..services.task_service import TaskService

                        task_id = uuid.UUID(tool_args["task_id"])
                        print(f"DEBUG: Attempting to complete task with ID: {task_id}")
                        completed_task = TaskService.complete_task(session, task_id)

                        if completed_task:
                            tool_executions.append({
                                "name": "complete_task",
                                "success": True,
                                "task_title": completed_task.title
                            })
                        else:
                            tool_executions.append({
                                "name": "complete_task",
                                "success": False,
                                "error": "Task not found"
                            })

                    elif tool_name == "delete_task":
                        from ..services.task_service import TaskService

                        task_id = uuid.UUID(tool_args["task_id"])
                        print(f"DEBUG: Attempting to delete task with ID: {task_id}")
                        success = TaskService.delete_task(session, task_id)

                        if success:
                            tool_executions.append({
                                "name": "delete_task",
                                "success": True
                            })
                        else:
                            tool_executions.append({
                                "name": "delete_task",
                                "success": False,
                                "error": "Task not found"
                            })

                    elif tool_name == "update_task":
                        from ..services.task_service import TaskService
                        from ..models.task import TaskUpdate

                        task_id = uuid.UUID(tool_args["task_id"])
                        print(f"DEBUG: Attempting to update task with ID: {task_id}")
                        task_update = TaskUpdate(
                            title=tool_args.get("title"),
                            description=tool_args.get("description"),
                            completed=tool_args.get("completed")
                        )
                        updated_task = TaskService.update_task(session, task_id, task_update)

                        if updated_task:
                            tool_executions.append({
                                "name": "update_task",
                                "success": True,
                                "task_title": updated_task.title
                            })
                        else:
                            tool_executions.append({
                                "name": "update_task",
                                "success": False,
                                "error": "Task not found"
                            })

                except KeyError as e:
                    # Specific error for missing keys in tool_args
                    print(f"ERROR: Missing required argument for {tool_name} tool: {str(e)}")
                    print(f"Tool args received: {tool_args}")
                    tool_executions.append({
                        "name": tool_name,
                        "success": False,
                        "error": f"Missing required argument: {str(e)}"
                    })
                    continue

                except Exception as e:
                    # Log the error but continue processing other tool calls
                    print(f"ERROR executing tool call {tool_name}: {str(e)}")
                    import traceback
                    print(f"Full traceback: {traceback.format_exc()}")
                    tool_executions.append({
                        "name": tool_name,
                        "success": False,
                        "error": str(e)
                    })
                    continue

            # Generate a consolidated response based on tool executions
            if tool_executions:
                # If list_tasks was executed and already updated the response, keep that
                list_task_execution = next((te for te in tool_executions if te["name"] == "list_tasks"), None)
                if list_task_execution:
                    # The response was already set by the list_tasks execution
                    pass
                else:
                    # Build a response summarizing the tool executions
                    success_actions = [te for te in tool_executions if te["success"]]
                    failed_actions = [te for te in tool_executions if not te["success"]]

                    if success_actions:
                        action_descriptions = []
                        for action in success_actions:
                            if action["name"] == "add_task":
                                action_descriptions.append(f"Added task '{action['task_title']}'")
                            elif action["name"] == "complete_task":
                                action_descriptions.append(f"Completed task '{action['task_title']}'")
                            elif action["name"] == "delete_task":
                                action_descriptions.append("Deleted a task")
                            elif action["name"] == "update_task":
                                action_descriptions.append(f"Updated task '{action['task_title']}'")

                        if action_descriptions:
                            result["response"] = "I've completed the following actions:\n" + "\n".join([f"• {desc}" for desc in action_descriptions])

                            # Add any failures to the response as well
                            if failed_actions:
                                failure_descriptions = []
                                for action in failed_actions:
                                    failure_descriptions.append(f"Failed to {action['name'].replace('_', ' ')}: {action.get('error', 'Unknown error')}")
                                result["response"] += "\n\nSome actions failed:\n" + "\n".join([f"• {desc}" for desc in failure_descriptions])
                    elif failed_actions:
                        failure_descriptions = []
                        for action in failed_actions:
                            failure_descriptions.append(f"Failed to {action['name'].replace('_', ' ')}: {action.get('error', 'Unknown error')}")
                        result["response"] = "Some actions failed:\n" + "\n".join([f"• {desc}" for desc in failure_descriptions])

        # Create assistant message with the AI response
        assistant_message = MessageCreate(
            conversation_id=conversation_id,
            user_id=user_id,  # The AI acts on behalf of the system/user
            role=MessageRole.ASSISTANT,
            content=result["response"]
        )
        MessageService.create_message(session, assistant_message)

        # Update conversation timestamp
        ConversationService.update_conversation(session, conversation_id)

        # Return the response with conversation_id and tool calls
        return {
            "conversation_id": str(conversation_id),
            "response": result["response"],
            "tool_calls": result["tool_calls"]  # Still return tool calls for frontend display if needed
        }

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle any other exceptions
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )