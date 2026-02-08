"""Agent state definition for the MPOnline automation system."""
from typing import TypedDict, Optional, Any, Annotated
from langchain_core.messages import BaseMessage
import operator


class AgentState(TypedDict):
    """
    Shared state for the multi-agent system.
    
    This state is passed between all agent nodes and tracks the entire
    automation workflow from login to form submission.
    """
    
    # User-provided data
    user_data: dict[str, Any]  # Structured applicant details
    service_type: str  # e.g., 'mppsc', 'electricity', 'university'
    
    # Workflow tracking
    current_step: str  # e.g., 'login', 'form_fill', 'document_upload', 'preview', 'payment'
    form_progress: dict[str, bool]  # Track which fields have been filled
    
    # Browser state
    dom_snapshot: Optional[str]  # Current page accessibility tree or HTML
    screenshot_path: Optional[str]  # Path to latest screenshot for VisionTool
    current_url: Optional[str]  # Current page URL
    
    # Session management
    session_data: dict[str, Any]  # Browser cookies, session info, form tokens
    
    # Validation and errors
    errors: Annotated[list[str], operator.add]  # Validation errors from Auditor
    
    # LLM conversation
    messages: Annotated[list[BaseMessage], operator.add]  # Conversation history
    
    # Routing
    next_action: str  # Supervisor's routing decision
    
    # HITL data
    captcha_solution: Optional[str]  # User-provided CAPTCHA solution
    payment_confirmed: bool  # Whether user confirmed payment
    
    # Metadata
    attempt_count: dict[str, int]  # Track retry attempts per step
    start_time: Optional[float]  # Workflow start timestamp
    last_update_time: Optional[float]  # Last state update timestamp
