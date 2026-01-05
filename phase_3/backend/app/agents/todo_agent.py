import google.generativeai as genai
from typing import Dict, Any, List
import json
import os
import re


class TodoAgent:
    def __init__(self):
        # Initialize Google Gemini client
        api_key = os.getenv("GEMINI_API_KEY")

        # Check if API key is available
        if api_key:
            try:
                genai.configure(api_key=api_key)

                # Try different model names in order of preference
                model_names = ['gemini-1.5-pro', 'gemini-1.0-pro', 'gemini-pro', 'gemini-1.5-flash']
                self.model = None

                for model_name in model_names:
                    try:
                        self.model = genai.GenerativeModel(model_name)
                        print(f"Successfully initialized model: {model_name}")
                        self.use_real_ai = True
                        break
                    except Exception as e:
                        print(f"Failed to initialize model {model_name}: {str(e)}")
                        continue

                if self.model is None:
                    print("Could not initialize any Gemini model, using mock AI")
                    self.use_real_ai = False
            except Exception as e:
                print(f"Error configuring Google AI: {str(e)}, using mock AI")
                self.use_real_ai = False
        else:
            print("GEMINI_API_KEY not found, using mock AI")
            self.use_real_ai = False

        # System prompt for the todo assistant
        self.system_prompt = """
        You are a helpful todo list assistant. You can help users manage their tasks by:
        1. Adding new tasks
        2. Listing existing tasks
        3. Completing tasks
        4. Deleting tasks
        5. Updating tasks

        Always confirm actions with the user before executing them.
        Use the available tools to perform operations on the todo list.
        Be friendly and conversational in your responses.
        """

    def process_message(self, user_message: str, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Process a user message and return an AI response
        """
        try:
            if self.use_real_ai and self.model:
                # Use real Google Gemini AI
                # Prepare the prompt for Google Gemini
                # Create a structured prompt that guides Gemini to return structured responses
                prompt_parts = [
                    self.system_prompt,
                    "\n\nImportant: When you need to perform actions on the todo list, respond in the following structured format:",
                    "\nFor adding a task: [ADD_TASK] {\"title\": \"task title\", \"description\": \"task description\", \"due_date\": \"optional due date\"} [/ADD_TASK]",
                    "\nFor listing tasks: [LIST_TASKS] {\"status\": \"all|pending|completed\"} [/LIST_TASKS]",
                    "\nFor completing a task: [COMPLETE_TASK] {\"task_id\": \"task id\"} [/COMPLETE_TASK]",
                    "\nFor deleting a task: [DELETE_TASK] {\"task_id\": \"task id\"} [/DELETE_TASK]",
                    "\nFor updating a task: [UPDATE_TASK] {\"task_id\": \"task id\", \"title\": \"new title\", \"description\": \"new description\", \"due_date\": \"new due date\", \"status\": \"new status\"} [/UPDATE_TASK]",
                    "\nIf you're just having a conversation or providing information, respond normally without the structured format.",
                    "\n\nPrevious conversation history:"
                ]

                # Add conversation history
                for msg in conversation_history:
                    role = msg["role"]
                    content = msg["content"]
                    prompt_parts.append(f"\n{role.capitalize()}: {content}")

                prompt_parts.append(f"\nUser: {user_message}")
                prompt_parts.append("\nAssistant:")

                # Combine all parts into a single prompt
                full_prompt = "".join(prompt_parts)

                # Call the Google Gemini API
                try:
                    response = self.model.generate_content(full_prompt)
                    # Extract text content
                    response_text = response.text if response.text else "I couldn't process your request."
                except Exception as api_error:
                    print(f"Google AI API call failed: {str(api_error)}, using mock AI")
                    # If API call fails, use mock response instead
                    response_text = self._get_mock_response(user_message)

            else:
                # Use mock AI for testing purposes
                response_text = self._get_mock_response(user_message)

            # Check if the response contains structured commands (tool calls)
            tool_call_pattern = r'\[([A-Z]+)_TASKS?\]\s*({.*?})\s*\[/\1_TASKS?\]'
            matches = re.findall(tool_call_pattern, response_text, re.DOTALL)

            if matches:
                # Process the first tool call found
                tool_name, args_json = matches[0]

                # Convert tool name to function name
                tool_function_name = tool_name.lower()
                if tool_function_name == "add":
                    tool_function_name = "add_task"
                elif tool_function_name == "list":
                    tool_function_name = "list_tasks"
                elif tool_function_name == "complete":
                    tool_function_name = "complete_task"
                elif tool_function_name == "delete":
                    tool_function_name = "delete_task"
                elif tool_function_name == "update":
                    tool_function_name = "update_task"

                try:
                    arguments = json.loads(args_json)
                    # Extract the actual response content (before or after the structured command)
                    response_content = re.sub(tool_call_pattern, '', response_text).strip()

                    return {
                        "type": "tool_call",
                        "content": response_content,
                        "tool_calls": [
                            {
                                "name": tool_function_name,
                                "arguments": arguments
                            }
                        ]
                    }
                except json.JSONDecodeError:
                    # If JSON parsing fails, return as a regular message
                    return {
                        "type": "message",
                        "content": response_text,
                        "tool_calls": []
                    }
            else:
                # No structured commands found, return as a regular message
                return {
                    "type": "message",
                    "content": response_text,
                    "tool_calls": []
                }

        except Exception as e:
            return {
                "type": "error",
                "content": f"Sorry, I encountered an error processing your request: {str(e)}",
                "tool_calls": []
            }

    def _get_mock_response(self, user_message: str) -> str:
        """
        Generate a mock response for testing when real AI is not available
        """
        user_message_lower = user_message.lower()

        if "hello" in user_message_lower or "hi" in user_message_lower:
            return "Hello! I'm your todo assistant. How can I help you with your tasks today?"
        elif "add" in user_message_lower or "create" in user_message_lower:
            # Extract potential task information
            import re
            words = user_message.split()
            task_title = " ".join([w for w in words if w.lower() not in ["add", "create", "task", "please"]]) or "Sample task"
            return f"[ADD_TASK] {{\"title\": \"{task_title}\", \"description\": \"Added from user request\"}} [/ADD_TASK] I've added the task '{task_title}' to your list!"
        elif ("list" in user_message_lower or "show" in user_message_lower) and ("task" in user_message_lower or "todo" in user_message_lower or "list" in user_message_lower):
            return "[LIST_TASKS] {\"status\": \"all\"} [/LIST_TASKS] Here are your tasks!"
        elif "show me my list" in user_message_lower or ("show" in user_message_lower and "my" in user_message_lower and "list" in user_message_lower) or "view my tasks" in user_message_lower or "my tasks" in user_message_lower or "what are my tasks" in user_message_lower or "see my tasks" in user_message_lower:
            return "[LIST_TASKS] {\"status\": \"all\"} [/LIST_TASKS] Here are your tasks!"
        elif "complete" in user_message_lower or "done" in user_message_lower:
            # For complete, provide more helpful response since we don't know specific task IDs
            return "I can help you complete a task. Please specify which task you want to complete by name, or say 'show me my list' to see your tasks first."
        elif "update" in user_message_lower or "change" in user_message_lower or "modify" in user_message_lower:
            # For update, try to extract task information
            import re
            # Look for patterns like "update task 'title' to 'new title'" or similar
            # Extract the old task name and new information
            words = user_message_lower.split()
            task_title = None
            new_title = None
            new_description = ""

            # Basic parsing for update commands
            if "to" in words:
                to_index = words.index("to")
                if to_index > 1:  # There's something before "to"
                    # Extract task to update
                    task_title_words = []
                    i = 1  # Start after "update"/"change"/"modify"
                    while i < to_index:
                        if words[i] not in ["the", "task", "a", "an", "my", "update", "change", "modify"]:
                            task_title_words.append(words[i])
                        i += 1
                    task_title = " ".join(task_title_words)

                    # Extract new title
                    new_title_words = []
                    i = to_index + 1
                    while i < len(words):
                        if words[i] not in ["to", "and", "with", "description", "as"]:
                            new_title_words.append(words[i])
                        else:
                            break
                        i += 1
                    new_title = " ".join(new_title_words)

            if task_title and new_title:
                return f"[UPDATE_TASK] {{\"task_id\": \"{task_title}\", \"title\": \"{new_title}\"}} [/UPDATE_TASK] I'm updating the task '{task_title}' to '{new_title}'."
            else:
                # If we can't parse, ask for clarification
                return "I can help you update a task. Please specify which task you want to update and what changes to make. For example: 'Update my groceries task to shopping'."
        elif "delete" in user_message_lower:
            # For delete, try to extract task name from the message for better matching
            import re
            # Remove common words to isolate the task name
            words_to_remove = ["delete", "the", "a", "an", "task", "please", "now", "my", "all"]
            clean_message = user_message_lower
            for word in words_to_remove:
                clean_message = re.sub(r'\b' + word + r'\b', '', clean_message, flags=re.IGNORECASE)
            clean_message = clean_message.strip()

            if clean_message and clean_message != "":
                # User specified a task name - pass it as the task_id for name-based matching
                return f"[DELETE_TASK] {{\"task_id\": \"{clean_message}\"}} [/DELETE_TASK] I'm trying to delete the task '{clean_message}'."
            else:
                # No specific task name provided - provide guidance
                return "I can help you delete a task. Please specify which task by name, or say 'show me my list' to see your tasks first."
        else:
            return f"I understand you said: '{user_message}'. I can help you manage your tasks. Try asking me to add, list, complete, update, or delete tasks."