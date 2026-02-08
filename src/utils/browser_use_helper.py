"""Helper utilities for browser-use integration."""
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from src import config
from src.utils.logging_config import logger


def get_configured_llm():
    """
    Get configured LLM instance for browser-use.
    
    Returns:
        Configured LLM (ChatOpenAI or ChatAnthropic)
    """
    if config.LLM_PROVIDER == "openai":
        logger.info("browser_use_llm", provider="openai", model="gpt-4o")
        return ChatOpenAI(
            model="gpt-4o",
            api_key=config.OPENAI_API_KEY,
            temperature=0.1
        )
    elif config.LLM_PROVIDER == "anthropic":
        logger.info("browser_use_llm", provider="anthropic", model="claude-3-5-sonnet-20241022")
        return ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            api_key=config.ANTHROPIC_API_KEY,
            temperature=0.1
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {config.LLM_PROVIDER}")


def format_user_data_for_ai(user_data: Dict[str, Any], service_type: str) -> str:
    """
    Convert structured user data into natural language instructions for AI.
    
    Args:
        user_data: Dictionary of user-provided data
        service_type: Type of service (mppsc, electricity, general, etc.)
        
    Returns:
        Natural language instructions for form filling or general task
    """
    instructions = []
    
    # Handle general assistant queries
    if service_type == "general":
        query = user_data.get("query", "")
        if query:
            return f"Please help with the following task: {query}"
        else:
            return "Please help navigate MPOnline portal."
    
    # Service-specific instructions
    if service_type == "mppsc":
        instructions.append("You are filling out an MPPSC application form on the MPOnline portal.")
        instructions.append("\nPlease fill the following information into the application form:\n")
    elif service_type == "electricity":
        instructions.append("You are paying an electricity bill on the MPOnline portal.")
        instructions.append("\nPlease enter the following information:\n")
    else:
        instructions.append(f"You are filling out a form for {service_type} on MPOnline.")
        instructions.append("\nPlease fill the following information:\n")
    
    # Convert each field to readable format
    for field, value in user_data.items():
        if value:  # Only include non-empty fields
            # Convert snake_case to Title Case
            readable_field = field.replace("_", " ").title()
            
            # Handle file paths
            if isinstance(value, str) and ("/" in value or "\\" in value):
                instructions.append(f"- {readable_field}: [File at {value}]")
            else:
                instructions.append(f"- {readable_field}: {value}")
    
    instructions.append("\nIMPORTANT INSTRUCTIONS:")
    instructions.append("- Take your time to carefully locate each field")
    instructions.append("- For dropdown menus, select the exact option that matches the value")
    instructions.append("- For date fields, use the format DD/MM/YYYY if not specified")
    instructions.append("- Skip any fields that are optional or not present in the form")
    instructions.append("- Do NOT submit the form - stop before clicking the final submit button")
    instructions.append("- The form may have multiple pages/sections - fill all of them")
    
    return "\n".join(instructions)


def create_google_search_task(service_type: str) -> str:
    """
    Create a task for searching Google and navigating to MPOnline.
    
    Args:
        service_type: Type of service to search for
        
    Returns:
        Task description for browser-use agent
    """
    # For general queries, don't force MPOnline navigation
    if service_type == "general":
        return ""
    
    search_queries = {
        "mppsc": "MPOnline MPPSC application form",
        "electricity": "MPOnline electricity bill payment",
        "barkatullah": "MPOnline Barkatullah University admission",
        "jiwaji": "MPOnline Jiwaji University admission"
    }
    
    query = search_queries.get(service_type, f"MPOnline {service_type}")
    
    task = f"""
    Perform the following steps:
    
    1. Go to google.com
    2. Search for "{query}"
    3. Look for results from mponline.gov.in domain
    4. Click on the official MPOnline portal link (mponline.gov.in)
    5. Wait for the page to fully load
    6. If you see a home page, look for navigation to {service_type.upper()} section
    7. Navigate to the application or service page
    8. Stop when you see a form or application page
    
    Be patient and make sure each step completes before moving to the next.
    """
    
    return task.strip()


def create_form_filling_task(user_data: Dict[str, Any], service_type: str) -> str:
    """
    Create a complete task for finding and filling the form.
    
    Args:
        user_data: User-provided data
        service_type: Type of service
        
    Returns:
        Complete task description
    """
    # Combine search and form filling
    search_task = create_google_search_task(service_type)
    form_instructions = format_user_data_for_ai(user_data, service_type)
    
    complete_task = f"""
{search_task}

Once you reach the application form page:

{form_instructions}

Remember: Complete all fields carefully, but DO NOT submit the form.
We will handle CAPTCHA and final submission separately.
"""
    
    return complete_task.strip()


def extract_browser_use_result(result: Any) -> Dict[str, Any]:
    """
    Extract useful information from browser-use agent result.
    
    Args:
        result: Result from browser-use agent.run()
        
    Returns:
        Dictionary with extracted information
    """
    try:
        # Browser-use returns various result formats
        # Extract what we can
        extracted = {
            "success": True,
            "final_url": None,
            "actions_taken": [],
            "errors": []
        }
        
        # Try to get final state information
        if hasattr(result, 'final_result'):
            extracted["final_url"] = getattr(result.final_result, 'url', None)
        
        if hasattr(result, 'history'):
            extracted["actions_taken"] = [
                str(action) for action in result.history
            ]
        
        logger.info("browser_use_result_extracted", result=extracted)
        return extracted
        
    except Exception as e:
        logger.error("browser_use_result_extraction_failed", error=str(e))
        return {
            "success": False,
            "final_url": None,
            "actions_taken": [],
            "errors": [str(e)]
        }


def estimate_ai_automation_cost(service_type: str, llm_provider: str) -> Dict[str, float]:
    """
    Estimate the cost of AI-driven automation.
    
    Args:
        service_type: Type of service
        llm_provider: LLM provider (openai/anthropic)
        
    Returns:
        Cost estimates
    """
    # Rough estimates based on typical usage
    estimates = {
        "mppsc": {
            "openai": {"min": 0.15, "max": 0.40},
            "anthropic": {"min": 0.20, "max": 0.50}
        },
        "electricity": {
            "openai": {"min": 0.05, "max": 0.15},
            "anthropic": {"min": 0.08, "max": 0.20}
        }
    }
    
    service_estimate = estimates.get(service_type, estimates["mppsc"])
    provider_estimate = service_estimate.get(llm_provider, service_estimate["openai"])
    
    return {
        "estimated_min_cost": provider_estimate["min"],
        "estimated_max_cost": provider_estimate["max"],
        "currency": "USD",
        "note": "Actual cost depends on form complexity and LLM API pricing"
    }
