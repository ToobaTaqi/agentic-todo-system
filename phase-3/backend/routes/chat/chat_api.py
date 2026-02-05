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

# Import Google Generative AI optionally
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Google Generative AI library not found. Install with: pip install google-generativeai")


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

    # Verify that the user_id in the URL matches the authenticated user's ID
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id does not match authenticated user"
        )

    # Validate UUID format if conversation_id is provided
    if chat_request.conversation_id and not validate_uuid(chat_request.conversation_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid conversation_id format"
        )

    # Validate message content
    if not chat_request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Message cannot be empty"
        )

    try:
        # Get or create conversation
        conversation = None
        if chat_request.conversation_id:
            # Verify that the conversation belongs to the authenticated user
            conversation = await get_conversation_by_id(db, chat_request.conversation_id, user_id)
            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied: Conversation does not belong to authenticated user"
                )
        else:
            # Create a new conversation
            conversation = await create_conversation(db, user_id)

        conversation_id = str(conversation.id)

        # Save user message to conversation history
        try:
            user_message = await create_message(
                db,
                conversation_id,
                user_id,
                "user",
                chat_request.message
            )
        except Exception as e:
            print(f"Error saving user message to database: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error saving message to conversation: {str(e)}"
            )

        # Prepare conversation history for the AI agent
        conversation_history = await get_messages_for_conversation(db, conversation_id, user_id)
        formatted_history = []
        for msg in conversation_history:
            formatted_history.append({
                "role": msg.role,
                "content": msg.content or ""  # Ensure content is not None
            })

        # Check if Gemini is available
        if not GEMINI_AVAILABLE:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Google Generative AI library not installed. Run: pip install google-generativeai"
            )

        # Get Gemini API key from environment
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Gemini API key not configured"
            )

        # Configure Gemini API
        genai.configure(api_key=gemini_api_key)

        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-pro')

        # Create the AI agent and process the request
        try:
            # Construct a prompt that encourages structured responses for tool usage
            system_prompt = """
You are a helpful assistant that manages tasks. When users request to create, update, list, complete, or delete tasks,
respond with a structured format indicating which tool to use and its parameters.
Use this format: [TOOL_CALL:tool_name:{"param1":"value1","param2":"value2"}]
For example:
- To add a task: [TOOL_CALL:add_task:{"title":"Buy groceries","priority":"medium"}]
- To list tasks: [TOOL_CALL:list_tasks:{"priority":"high"}]
- To complete a task: [TOOL_CALL:complete_task:{"task_id":"123"}]
- To update a task: [TOOL_CALL:update_task:{"task_id":"123","title":"Updated title"}]
- To delete a task: [TOOL_CALL:delete_task:{"task_id":"123"}]

Always respond in a helpful manner and explain what you're doing.
"""

            # Build the conversation with system instructions
            full_prompt = f"{system_prompt}\n\n"
            for msg in formatted_history:
                full_prompt += f"{msg['role'].upper()}: {msg['content']}\n"

            full_prompt += "\nASSISTANT:"

            # Log the request for debugging
            print(f"Sending request to Gemini with prompt length: {len(full_prompt)}")

            # Generate content using Gemini
            response = model.generate_content(full_prompt)

            print("Gemini response received successfully")

            # Process the response
            ai_response = ""
            tool_calls_results = []

            if response.text:
                ai_response = response.text
            else:
                ai_response = "I couldn't process your request. Please try again."

            # Parse for tool calls in the response
            import re
            tool_call_pattern = r'\[TOOL_CALL:(\w+):({.*?})\]'
            matches = re.findall(tool_call_pattern, response.text)

            for match in matches:
                function_name = match[0]
                try:
                    function_args = json.loads(match[1])

                    # Execute the MCP tool
                    tool_result = await execute_mcp_tool(function_name, function_args, user_id)

                    # Store the tool call and result
                    tool_calls_results.append(ToolCallResult(
                        tool_name=function_name,
                        arguments=function_args,
                        result=tool_result.data if tool_result.success else {"error": tool_result.error}
                    ))

                    # If there was an error, add it to the AI response
                    if not tool_result.success:
                        ai_response += f"\nError executing {function_name}: {tool_result.error}"
                    else:
                        ai_response += f"\nSuccessfully executed {function_name}."

                except json.JSONDecodeError:
                    print(f"Could not parse arguments for tool {function_name}: {match[1]}")
                    continue
                except Exception as e:
                    print(f"Error executing tool {function_name}: {str(e)}")
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