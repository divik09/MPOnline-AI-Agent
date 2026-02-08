"""Auditor agent node - validates form state and catches errors."""
import time
import re
from typing import Any
from src.core.agent_state import AgentState
from src.automation.browser_manager import browser_manager
from src.automation import browser_actions
from src.utils.logging_config import logger
from src.services.service_registry import SERVICE_REGISTRY


async def auditor_node(state: AgentState) -> dict[str, Any]:
    """
    Auditor agent handles:
    - Validating filled data against user_data
    - Checking for missing required fields
    - Verifying format (email, phone, date)
    - Comparing preview page with requirements
    
    Args:
        state: Current agent state
        
    Returns:
        Partial state update
    """
    logger.info("auditor_node_started", service=state["service_type"])
    
    try:
        # Get page
        page = await browser_manager.get_page()
        
        # Get service template
        service_template = SERVICE_REGISTRY.get(state["service_type"])
        if not service_template:
            return {
                "errors": ["Unknown service type"],
                "next_action": "error"
            }
        
        # Get field mappings for current step
        field_mappings = service_template.get_field_mappings(state["current_step"])
        validation_rules = service_template.get_validation_rules()
        
        errors = []
        form_progress = state.get("form_progress", {})
        
        # Check required fields
        for field_name, field_config in field_mappings.items():
            if field_config.get("required", False):
                if not form_progress.get(field_name, False):
                    errors.append(f"Required field not filled: {field_name}")
                    logger.warning("required_field_missing", field=field_name)
        
        # Validate data formats
        for field_name, value in state["user_data"].items():
            # Email validation
            if "email" in field_name.lower() and value:
                if not _validate_email(value):
                    errors.append(f"Invalid email format: {field_name}")
                    logger.warning("invalid_email", field=field_name, value=value)
            
            # Phone validation (Indian format)
            if "phone" in field_name.lower() or "mobile" in field_name.lower():
                if value and not _validate_phone(value):
                    errors.append(f"Invalid phone format: {field_name}")
                    logger.warning("invalid_phone", field=field_name, value=value)
            
            # Date validation
            if "date" in field_name.lower() or "dob" in field_name.lower():
                if value and not _validate_date(value):
                    errors.append(f"Invalid date format: {field_name}")
                    logger.warning("invalid_date", field=field_name, value=value)
        
        # Check for form-level errors on page
        page_errors = await _check_page_errors(page)
        if page_errors:
            errors.extend(page_errors)
        
        # Take screenshot of validation state
        screenshot_path = f"{config.SCREENSHOTS_DIR}/audit_{int(time.time())}.png"
        await browser_actions.take_screenshot(page, screenshot_path)
        
        logger.info(
            "auditor_completed",
            errors_found=len(errors),
            fields_checked=len(field_mappings)
        )
        
        # Determine next action based on validation
        if errors:
            next_action = "fill_form"  # Go back to FormExpert to fix errors
        else:
            # Move to next step
            if state["current_step"] == "form_fill":
                next_action = "upload_documents"
            elif state["current_step"] == "document_upload":
                next_action = "preview"
            elif state["current_step"] == "preview":
                next_action = "payment"
            else:
                next_action = "complete"
        
        return {
            "errors": errors,
            "screenshot_path": screenshot_path,
            "next_action": next_action,
            "last_update_time": time.time()
        }
    
    except Exception as e:
        logger.error("auditor_node_error", error=str(e))
        return {
            "errors": [f"Auditor error: {str(e)}"],
            "next_action": "error"
        }


def _validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def _validate_phone(phone: str) -> bool:
    """Validate Indian phone number format."""
    # Remove spaces, dashes, etc.
    phone = re.sub(r'[\s\-\(\)]', '', phone)
    # Check for 10 digits or +91 followed by 10 digits
    pattern = r'^(?:\+91)?[6-9]\d{9}$'
    return bool(re.match(pattern, phone))


def _validate_date(date_str: str) -> bool:
    """Validate date format (DD/MM/YYYY or DD-MM-YYYY or YYYY-MM-DD)."""
    patterns = [
        r'^\d{2}/\d{2}/\d{4}$',  # DD/MM/YYYY
        r'^\d{2}-\d{2}-\d{4}$',  # DD-MM-YYYY
        r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
    ]
    return any(re.match(pattern, date_str) for pattern in patterns)


async def _check_page_errors(page) -> list[str]:
    """Check for error messages displayed on the page."""
    errors = []
    
    # Common error selectors
    error_selectors = [
        ".error",
        ".alert-danger",
        ".validation-error",
        "[class*='error']",
        ".field-validation-error"
    ]
    
    for selector in error_selectors:
        try:
            elements = await page.query_selector_all(selector)
            for element in elements:
                text = await element.text_content()
                if text and text.strip():
                    errors.append(f"Page error: {text.strip()}")
                    logger.info("page_error_found", error=text.strip())
        except Exception:
            continue
    
    return errors
