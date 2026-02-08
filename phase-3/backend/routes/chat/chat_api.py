"""Chat API endpoint for AI-powered conversation interface."""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uuid
import os
from datetime import datetime
from models.conversation_models import Conversation, Message
from database.conversation_db import (
    get_db_session, create_conversation, get_conversation_by_id,
    create_message, get_messages_for_conversation, validate_conversation_ownership
)
from auth.auth import get_current_user, TokenData
from mcp_tools.task_operations import execute_mcp_tool
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
import asyncio
import json
from typing import Dict, Any, List

# Import OpenAI client for Groq (which uses OpenAI-compatible API)
try:
    from openai import OpenAI
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("OpenAI library not found. Install with: pip install openai")


router = APIRouter()
security = HTTPBearer()


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    conversation_id: Optional[str] = Field(None, description="UUID of existing conversation (optional)")
    message: str = Field(..., min_length=1, max_length=10000, description="Natural language request message")


class ToolCallResult(BaseModel):
    """Model for tool call results."""
    tool_name: str
    arguments: Dict[str, Any]
    result: Dict[str, Any]


class ChatResponseData(BaseModel):
    """Data portion of chat response."""
    conversation_id: str
    response: str
    tool_calls: List[ToolCallResult] = []


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    success: bool
    data: Optional[ChatResponseData] = None
    error: Optional[Dict[str, str]] = None


def validate_uuid(uuid_string: str) -> bool:
    """Validate UUID format."""
    try:
        uuid.UUID(uuid_string)
        return True
    except ValueError:
        return False


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def process_chat_request(
    user_id: str,
    chat_request: ChatRequest,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Process natural language request for task management and return AI-generated response."""
    
    print("\n=== STEP 1: AUTHENTICATION AND VALIDATION ===")
    print(f"Received request for user_id: {user_id}")
    print(f"Current user from token: {current_user.user_id}")
    print(f"Conversation ID provided: {chat_request.conversation_id}")
    print(f"Message length: {len(chat_request.message) if chat_request.message else 0}")

    # Verify that the user_id in the URL matches the authenticated user's ID
    if current_user.user_id != user_id:
        print(f"ERROR in STEP 1: User ID mismatch - URL: {user_id}, Token: {current_user.user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id does not match authenticated user"
        )
    else:
        print("STEP 1: Authentication successful")

    # Validate UUID format if conversation_id is provided
    if chat_request.conversation_id and not validate_uuid(chat_request.conversation_id):
        print(f"ERROR in STEP 1: Invalid conversation_id format: {chat_request.conversation_id}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid conversation_id format"
        )

    # Validate message content
    if not chat_request.message.strip():
        print("ERROR in STEP 1: Empty message received")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Message cannot be empty"
        )
    else:
        print("STEP 1: Validation passed")

    try:
        print("\n=== STEP 2: CONVERSATION MANAGEMENT ===")
        # Get or create conversation
        conversation = None
        if chat_request.conversation_id:
            print(f"Attempting to retrieve conversation: {chat_request.conversation_id}")
            # Verify that the conversation belongs to the authenticated user
            conversation = await get_conversation_by_id(db, chat_request.conversation_id, user_id)
            if not conversation:
                print(f"ERROR in STEP 2: Conversation not found or unauthorized: {chat_request.conversation_id}")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied: Conversation does not belong to authenticated user"
                )
            else:
                print("STEP 2: Retrieved existing conversation successfully")
        else:
            print("Creating new conversation")
            # Create a new conversation
            conversation = await create_conversation(db, user_id)
            print("STEP 2: Created new conversation successfully")

        conversation_id = str(conversation.id)
        print(f"Using conversation_id: {conversation_id}")

        print("\n=== STEP 3: SAVE USER MESSAGE ===")
        # Save user message to conversation history
        try:
            print(f"Saving user message: '{chat_request.message[:50]}...'")  # First 50 chars
            user_message = await create_message(
                db,
                conversation_id,
                user_id,
                "user",
                chat_request.message
            )
            print("STEP 3: User message saved successfully")
        except Exception as e:
            print(f"ERROR in STEP 3: Failed to save user message - {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error saving message to conversation: {str(e)}"
            )

        print("\n=== STEP 4: PREPARE CONVERSATION HISTORY ===")
        # Safely prepare conversation history for the AI agent
        try:
            print(f"Attempting to retrieve messages for conversation: {conversation_id}")
            conversation_history = await get_messages_for_conversation(db, conversation_id, user_id)
            print(f"Retrieved {len(conversation_history) if conversation_history else 0} messages from conversation history")
            
            # Validate and sanitize conversation history
            formatted_history = []
            if conversation_history:
                for idx, msg in enumerate(conversation_history):
                    # Defensive programming: validate each message object
                    if not hasattr(msg, 'role') or not hasattr(msg, 'content'):
                        print(f"Warning: Message at index {idx} missing required attributes: {msg}")
                        continue
                    
                    # Sanitize role and content
                    role = getattr(msg, 'role', 'user') or 'user'
                    content = getattr(msg, 'content', '') or ''
                    
                    # Validate role is acceptable
                    if role not in ['user', 'assistant']:
                        print(f"Warning: Invalid role '{role}' for message at index {idx}, defaulting to 'user'")
                        role = 'user'
                    
                    formatted_history.append({
                        "role": role,
                        "content": content
                    })
                    print(f"Formatted message {idx}: role='{role}', content_len={len(content)}")
            else:
                print("No conversation history found, proceeding with empty history")
            
            print(f"Successfully formatted {len(formatted_history)} messages for AI processing")
            print("STEP 4: Conversation history prepared successfully")
            
        except Exception as history_error:
            print(f"ERROR in STEP 4: Failed to prepare conversation history - {str(history_error)}")
            print(f"Full traceback: {repr(history_error)}")
            
            # Return a safe error response instead of crashing
            ai_response = "Sorry, I encountered an issue retrieving the conversation history. Please try again."
            
            # Store the error response in the conversation
            try:
                ai_message = await create_message(
                    db,
                    conversation_id,
                    user_id,
                    "assistant",
                    ai_response
                )
                print("STEP 4: Error response saved to conversation successfully")
            except Exception as save_error:
                print(f"ERROR in STEP 4: Failed to save error response - {str(save_error)}")
            
            # Return the error response
            response_data = ChatResponseData(
                conversation_id=conversation_id,
                response=ai_response,
                tool_calls=[]
            )
            
            print("STEP 4: Returning error response to prevent crash")
            return ChatResponse(success=True, data=response_data)

        print("\n=== STEP 5: GROQ API INITIALIZATION ===")
        # Check if Groq/OpenAI client is available
        if not GROQ_AVAILABLE:
            print("ERROR in STEP 5: OpenAI library not available")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OpenAI library not installed. Run: pip install openai"
            )
        else:
            print("STEP 5: OpenAI library available")

        # Get Groq API key from environment
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            print("ERROR in STEP 5: GROQ_API_KEY not configured in environment")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Groq API key not configured"
            )
        else:
            print("STEP 5: GROQ_API_KEY found in environment")

        # Initialize Groq client (uses OpenAI-compatible API)
        try:
            client = OpenAI(
                api_key=groq_api_key,
                base_url="https://api.groq.com/openai/v1"  # Groq's OpenAI-compatible endpoint
            )
            print("STEP 5: Groq client initialized successfully")
        except Exception as e:
            print(f"ERROR in STEP 5: Failed to initialize Groq client - {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to initialize Groq client: {str(e)}"
            )

        # Define the tools that the AI can use (MCP tools)
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task to the user's task list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "The title of the task"},
                            "description": {"type": "string", "description": "Detailed description of the task"},
                            "priority": {"type": "string", "enum": ["high", "medium", "low"], "description": "Priority level"},
                            "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags for categorizing the task"},
                            "due_date": {"type": "string", "description": "Due date in ISO format"},
                            "is_recurring": {"type": "boolean", "description": "Whether the task repeats"},
                            "recurrence_pattern": {"type": "string", "enum": ["daily", "weekly", "monthly"], "description": "Pattern for recurring tasks"}
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List tasks with optional filtering",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "enum": ["completed", "incomplete"], "description": "Filter by completion status"},
                            "priority": {"type": "string", "enum": ["high", "medium", "low"], "description": "Filter by priority"},
                            "search": {"type": "string", "description": "Search term for title or description"},
                            "sort": {"type": "string", "enum": ["due_date", "priority", "title", "created_at"], "description": "Sort order"},
                            "order": {"type": "string", "enum": ["asc", "desc"], "description": "Sort direction"},
                            "page": {"type": "integer", "description": "Page number for pagination"},
                            "limit": {"type": "integer", "description": "Number of tasks per page"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Toggle completion status of a task by ID or name",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "ID of the task to complete (optional)"},
                            "task_name": {"type": "string", "description": "Name/title of the task to complete (optional)"}
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task by ID or name",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "ID of the task to delete (optional)"},
                            "task_name": {"type": "string", "description": "Name/title of the task to delete (optional)"}
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update properties of a task by ID or name",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "ID of the task to update (optional)"},
                            "task_name": {"type": "string", "description": "Name/title of the task to update (optional)"},
                            "title": {"type": "string", "description": "New title of the task"},
                            "description": {"type": "string", "description": "New description of the task"},
                            "priority": {"type": "string", "enum": ["high", "medium", "low"], "description": "New priority level"},
                            "tags": {"type": "array", "items": {"type": "string"}, "description": "New tags for the task"},
                            "due_date": {"type": "string", "description": "New due date in ISO format"},
                            "is_recurring": {"type": "boolean", "description": "Whether the task repeats"},
                            "recurrence_pattern": {"type": "string", "enum": ["daily", "weekly", "monthly"], "description": "Pattern for recurring tasks"}
                        },
                        "required": []
                    }
                }
            }
        ]

        print("\n=== STEP 6: GROQ API CALL ===")
        # Create the AI agent and process the request
        try:
            # Prepare messages for the chat completion
            system_prompt = """
You are a helpful assistant that manages tasks. When users request to create, update, list, complete, or delete tasks,
use the appropriate functions to perform these actions. Always respond in a helpful manner and explain what you're doing.
"""

            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Add conversation history
            for msg in formatted_history:
                messages.append({"role": msg['role'], "content": msg['content']})
            
            print(f"Prepared {len(messages)} messages for Groq API")
            print(f"First message: {messages[0]['content'][:100]}...")  # First 100 chars of system prompt
            if len(messages) > 1:
                print(f"Last user message: {messages[-1]['content'][:100]}...")  # First 100 chars of last message

            # Log the request for debugging
            print(f"Sending request to Groq with {len(messages)} messages")

            # Call Groq API with function calling
            try:
                print("Making API call to Groq...")
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",  # Free tier eligible model with good performance
                    messages=messages,
                    tools=tools,
                    tool_choice="auto",  # Auto-select tools based on user request
                    max_tokens=4096  # Maximum tokens for the response
                )
                
                print("Groq response received successfully")
                print(f"Response finish reason: {response.choices[0].finish_reason if response.choices else 'No choices'}")
            except Exception as groq_error:
                print(f"ERROR in STEP 6: Groq API call failed - {str(groq_error)}")
                error_msg = str(groq_error)
                
                # Check if it's a rate limit error
                if "rate_limit" in error_msg.lower() or "quota" in error_msg.lower() or "exceeded" in error_msg.lower():
                    print("STEP 6: Detected rate limit error")
                    ai_response = "Sorry, I've reached my usage limit temporarily. Please try again later. This is a limitation of the free API tier."
                elif "authentication" in error_msg.lower() or "invalid" in error_msg.lower():
                    print("STEP 6: Detected authentication error")
                    ai_response = "Sorry, there's an issue with the AI service configuration. Please contact the administrator."
                else:
                    print("STEP 6: General API error")
                    ai_response = f"Sorry, I encountered an error processing your request: {error_msg}. Please try again."
                
                print(f"STEP 6: Saving error response to conversation: {ai_response}")
                # Store the error response in the conversation
                try:
                    ai_message = await create_message(
                        db,
                        conversation_id,
                        user_id,
                        "assistant",
                        ai_response
                    )
                    print("STEP 6: Error response saved to conversation successfully")
                except Exception as save_error:
                    print(f"ERROR in STEP 6: Failed to save error response - {str(save_error)}")
                
                # Return the error response
                response_data = ChatResponseData(
                    conversation_id=conversation_id,
                    response=ai_response,
                    tool_calls=[]
                )
                
                print("STEP 6: Returning error response to frontend")
                return ChatResponse(success=True, data=response_data)

            print("\n=== STEP 7: PROCESSING GROQ RESPONSE ===")
            # Process the response
            ai_response = ""
            tool_calls_results = []
            
            print(f"Response finish reason: {response.choices[0].finish_reason if response.choices else 'No choices'}")
            
            # Check if the response has tool calls
            if response.choices and response.choices[0].finish_reason == "tool_calls":
                # Process tool calls
                print("STEP 7: Processing tool calls from response")
                for tool_call in response.choices[0].message.tool_calls:
                    function_name = tool_call.function.name
                    print(f"Processing tool call: {function_name}")
                    try:
                        function_args = json.loads(tool_call.function.arguments)
                        print(f"Arguments: {function_args}")
                        
                        # Execute the MCP tool
                        tool_result = await execute_mcp_tool(function_name, function_args, user_id)
                        print(f"Tool result success: {tool_result.success}")

                        # Store the tool call and result
                        tool_calls_results.append(ToolCallResult(
                            tool_name=function_name,
                            arguments=function_args,
                            result=tool_result.data if tool_result.success else {"error": tool_result.error}
                        ))

                        # If there was an error, add it to the AI response
                        if not tool_result.success:
                            ai_response += f"\nError executing {function_name}: {tool_result.error}"
                            print(f"Added error to response: {tool_result.error}")
                        else:
                            ai_response += f"\nSuccessfully executed {function_name}."
                            print(f"Successfully executed {function_name}")

                    except json.JSONDecodeError:
                        print(f"ERROR in STEP 7: Could not parse arguments for tool {function_name}: {tool_call.function.arguments}")
                        ai_response += f"\nError: Could not parse arguments for {function_name}."
                        continue
                    except Exception as e:
                        print(f"ERROR in STEP 7: Error executing tool {function_name}: {str(e)}")
                        ai_response += f"\nError executing {function_name}: {str(e)}."
                        continue
            
            # Save AI response to conversation history
            try:
                ai_message = await create_message(
                    db,
                    conversation_id,
                    user_id,
                    "assistant",
                    ai_response
                )
            except Exception as e:
                print(f"Error saving AI response to database: {str(e)}")
                # Still return the response even if saving to DB fails
                # This prevents a bad database operation from breaking the entire chat
                pass

            # Return the response
            response_data = ChatResponseData(
                conversation_id=conversation_id,
                response=ai_response,
                tool_calls=tool_calls_results
            )

            return ChatResponse(success=True, data=response_data)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing AI request: {str(e)}"
            )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )