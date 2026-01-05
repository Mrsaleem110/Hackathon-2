from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Dict, Any
from datetime import datetime
import uuid
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str

from ..models.conversation import Conversation, Message
from ..db.database import get_session
from ..agents.todo_agent import TodoAgent
from ..mcp.tools import TodoTools

# Import Phase 2 task service (assuming it exists)
# This would need to be adapted to your actual Phase 2 implementation
from ..models.item import Item  # Use the Item model instead of Task model

router = APIRouter(prefix="/api/{user_id}/chat", tags=["chat"])


@router.post("/")
async def chat(user_id: str, request: ChatRequest, session: Session = Depends(get_session)):
    message = request.message
    """
    Main chat endpoint that processes user messages and returns AI responses
    """
    try:
        # Initialize the todo agent
        agent = TodoAgent()

        # Get or create conversation for this user
        conversation = session.exec(
            select(Conversation).where(Conversation.user_id == user_id)
        ).first()

        if not conversation:
            # Create new conversation if one doesn't exist
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

        # Fetch recent conversation history (last 10 messages for context)
        conversation_messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.timestamp.desc())
            .limit(10)
        ).all()

        # Reverse to get chronological order
        conversation_history = []
        for msg in reversed(conversation_messages):
            conversation_history.append({
                "role": msg.role,
                "content": msg.content
            })

        # Save user message to database
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=message,
            extra_data={}
        )
        session.add(user_message)
        session.commit()

        # Process message with AI agent
        agent_response = agent.process_message(message, conversation_history)

        # Handle different types of agent responses
        if agent_response["type"] == "tool_call":
            tool_calls = agent_response["tool_calls"]
            tool_results = []

            # Execute each tool call
            for tool_call in tool_calls:
                tool_name = tool_call["name"]
                arguments = tool_call["arguments"]

                # Create a basic item service to pass to TodoTools
                # In a real implementation, you would have a proper item service
                from ..models.item import Item, ItemCreate, ItemUpdate, Priority
                from sqlmodel import select as sql_select
                from datetime import datetime

                class ItemService:
                    async def create_task(self, task_data):
                        from datetime import datetime
                        due_date = task_data.get("due_date")
                        # Convert empty string to None for the Item model
                        if due_date == "":
                            due_date = None

                        # Convert user_id to integer since Item model expects integer owner_id
                        try:
                            owner_id = int(user_id)
                        except ValueError:
                            # If user_id is not a valid integer, we might need to find the user by other means
                            # For now, let's assume it's an integer
                            owner_id = 1  # Default fallback

                        item = Item(
                            title=task_data.get("title", ""),
                            description=task_data.get("description", ""),
                            completed=False,  # Default to not completed
                            due_date=due_date,
                            owner_id=owner_id,
                            priority=Priority.MEDIUM  # Default to medium priority
                        )
                        session.add(item)
                        session.commit()
                        session.refresh(item)
                        return {"id": item.id, "title": item.title, "description": item.description, "completed": item.completed}

                    async def get_tasks(self, filters):
                        status_filter = filters.get("status", "all")
                        query = sql_select(Item).where(Item.owner_id == int(user_id))

                        if status_filter == "completed":
                            query = query.where(Item.completed == True)
                        elif status_filter == "pending":
                            query = query.where(Item.completed == False)

                        items = session.exec(query).all()
                        return [{"id": item.id, "title": item.title, "description": item.description, "completed": item.completed} for item in items]

                    async def update_task(self, task_id, update_data):
                        # Try to convert task_id to integer first (for numeric ID matching)
                        item = None
                        try:
                            item_id = int(task_id)
                            item = session.exec(sql_select(Item).where(Item.id == item_id).where(Item.owner_id == int(user_id))).first()
                        except ValueError:
                            # If task_id is not numeric, try to find by title (case-insensitive partial match)
                            items = session.exec(sql_select(Item).where(Item.owner_id == int(user_id))).all()
                            for potential_item in items:
                                if task_id.lower() in potential_item.title.lower() or task_id.lower() in (potential_item.description or "").lower():
                                    item = potential_item
                                    break

                        if item:
                            # Map update fields to Item model fields
                            for key, value in update_data.items():
                                if key == "status":
                                    # Map status to completed field
                                    if value == "completed":
                                        setattr(item, "completed", True)
                                    elif value == "pending":
                                        setattr(item, "completed", False)
                                elif hasattr(item, key):
                                    setattr(item, key, value)
                            session.add(item)
                            session.commit()
                            session.refresh(item)
                            return {"id": item.id, "title": item.title, "description": item.description, "completed": item.completed}
                        return None

                    async def delete_task(self, task_id):
                        # Convert task_id to integer if it's a string representation of an integer
                        try:
                            item_id = int(task_id)
                        except ValueError:
                            # If task_id is not numeric, try to find by title
                            items = session.exec(sql_select(Item).where(Item.owner_id == int(user_id))).all()
                            for item in items:
                                if task_id.lower() in item.title.lower() or task_id.lower() in (item.description or "").lower():
                                    session.delete(item)
                                    session.commit()
                                    return True
                            return False

                        # First try to delete by exact ID match
                        item = session.exec(sql_select(Item).where(Item.id == item_id).where(Item.owner_id == int(user_id))).first()
                        if item:
                            session.delete(item)
                            session.commit()
                            return True

                        return False

                # Create TodoTools instance with the item service
                tools = TodoTools(ItemService())

                # Execute the tool call based on the tool name
                try:
                    if tool_name == "list_tasks":
                        result = await tools.list_tasks(**arguments)
                        tool_result = {"name": tool_name, "arguments": arguments, "result": result, "status": "success"}
                    elif tool_name == "add_task":
                        result = await tools.add_task(**arguments)
                        tool_result = {"name": tool_name, "arguments": arguments, "result": result, "status": "success"}
                    elif tool_name == "complete_task":
                        result = await tools.complete_task(**arguments)
                        tool_result = {"name": tool_name, "arguments": arguments, "result": result, "status": "success"}
                    elif tool_name == "delete_task":
                        result = await tools.delete_task(**arguments)
                        tool_result = {"name": tool_name, "arguments": arguments, "result": result, "status": "success"}
                    elif tool_name == "update_task":
                        result = await tools.update_task(**arguments)
                        tool_result = {"name": tool_name, "arguments": arguments, "result": result, "status": "success"}
                    else:
                        tool_result = {"name": tool_name, "arguments": arguments, "result": f"Unknown tool: {tool_name}", "status": "error"}
                except Exception as e:
                    tool_result = {"name": tool_name, "arguments": arguments, "result": f"Error executing tool: {str(e)}", "status": "error"}

                tool_results.append(tool_result)

            # Create response content based on tool results
            if tool_results and tool_results[0]["status"] == "success":
                result_data = tool_results[0]["result"]
                if tool_results[0]["name"] == "list_tasks":
                    if result_data:
                        task_list = "\n".join([f"- {task['title']} ({'completed' if task.get('completed', False) else 'pending'})" for task in result_data])
                        response_content = f"Here are your tasks:\n{task_list}"
                    else:
                        response_content = "You don't have any tasks yet."
                elif tool_results[0]["name"] == "add_task":
                    response_content = f"I've added the task: {result_data.get('title', 'New task')}"
                elif tool_results[0]["name"] == "complete_task":
                    response_content = "I've marked the task as completed!"
                elif tool_results[0]["name"] == "delete_task":
                    response_content = "I've deleted the task!"
                elif tool_results[0]["name"] == "update_task":
                    response_content = f"I've updated the task: {result_data.get('title', 'Updated task')}"
                else:
                    response_content = f"Action completed: {tool_results[0]['name']}"
            else:
                response_content = f"Sorry, I couldn't complete that action: {tool_results[0]['result'] if tool_results else 'Unknown error'}"

            # Create AI response message
            ai_message = Message(
                conversation_id=conversation.id,
                role="assistant",
                content=response_content,
                extra_data={"tool_call": tool_results[0] if tool_results else {}}
            )

        elif agent_response["type"] == "error":
            # Handle error response
            response_content = agent_response["content"]

            # Create AI response message
            ai_message = Message(
                conversation_id=conversation.id,
                role="assistant",
                content=response_content,
                extra_data={"error": True}
            )

        else:
            # Handle regular message response
            response_content = agent_response["content"]

            # Create AI response message
            ai_message = Message(
                conversation_id=conversation.id,
                role="assistant",
                content=response_content,
                extra_data={}
            )

        # Save AI response to database
        session.add(ai_message)
        session.commit()

        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()

        # Return the response
        return {
            "conversation_id": conversation.id,
            "response": response_content,
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")


@router.get("/history")
async def get_conversation_history(user_id: str, session: Session = Depends(get_session)):
    """
    Get conversation history for a user
    """
    try:
        # Get conversation for this user
        conversation = session.exec(
            select(Conversation).where(Conversation.user_id == user_id)
        ).first()

        if not conversation:
            return {"messages": []}

        # Fetch all messages in this conversation
        messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.timestamp.asc())
        ).all()

        # Format messages for response
        formatted_messages = [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "extra_data": msg.extra_data
            }
            for msg in messages
        ]

        return {
            "conversation_id": conversation.id,
            "messages": formatted_messages
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")