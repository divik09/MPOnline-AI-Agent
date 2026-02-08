"""FormExpert agent node - handles field mapping and form filling."""
import time
from typing import Any
from src.core.agent_state import AgentState
from src.automation.browser_manager import browser_manager
from src.automation import browser_actions
from src.tools.vision_tool import vision_tool
from src import config
from src.utils.logging_config import logger
from src.services.service_registry import SERVICE_REGISTRY


async def form_expert_node(state: AgentState) -> dict[str, Any]:
    """
    FormExpert agent handles:
    - Mapping user_data to form fields
    - Filling text inputs, dropdowns, radio buttons, checkboxes
    - Handling file uploads
    - Using VisionTool when selectors are ambiguous
    
    Args:
        state: Current agent state
        
    Returns:
        Partial state update
    """
    logger.info("form_expert_node_started", service=state["service_type"])
    
    try:
        # Get page
        page = await browser_manager.get_page()
        
        # Get service template
        service_template = SERVICE_REGISTRY.get(state["service_type"])
        if not service_template:
            return {
                "errors": [f"Unknown service type: {state['service_type']}"],
                "next_action": "error"
            }
        
        # Get field mappings for current step
        field_mappings = service_template.get_field_mappings(state["current_step"])
        
        form_progress = state.get("form_progress", {})
        errors = []
        filled_count = 0
        
        # Fill each field
        for field_name, field_config in field_mappings.items():
            # Skip if already filled
            if form_progress.get(field_name, False):
                logger.info("field_already_filled", field=field_name)
                continue
            
            # Get value from user_data
            value = state["user_data"].get(field_name)
            if value is None:
                logger.warning("field_value_missing", field=field_name)
                errors.append(f"Missing value for field: {field_name}")
                continue
            
            # Get selector
            selector = field_config.get("selector")
            field_type = field_config.get("type", "text")
            
            # If selector not found, use VisionTool
            if not selector or not await browser_actions.wait_for_selector(page, selector, timeout=3000):
                logger.info("using_vision_tool", field=field_name)
                
                # Take screenshot
                screenshot_path = f"{config.SCREENSHOTS_DIR}/vision_{field_name}_{int(time.time())}.png"
                await browser_actions.take_screenshot(page, screenshot_path)
                
                # Use VisionTool
                vision_result = await vision_tool.identify_element(
                    screenshot_path,
                    field_name,
                    field_config.get("description")
                )
                
                if vision_result["confidence"] > 60:
                    selector = vision_result["selector"]
                    logger.info("vision_tool_success", field=field_name, selector=selector)
                else:
                    logger.error("vision_tool_failed", field=field_name)
                    errors.append(f"Could not find selector for: {field_name}")
                    continue
            
            # Fill the field based on type
            success = False
            
            if field_type == "text":
                success = await browser_actions.safe_fill(page, selector, str(value))
            
            elif field_type == "select":
                success = await browser_actions.safe_select(page, selector, str(value))
            
            elif field_type == "radio" or field_type == "checkbox":
                # Find the specific radio/checkbox option
                option_selector = f"{selector}[value='{value}']"
                success = await browser_actions.safe_click(page, option_selector)
            
            elif field_type == "file":
                success = await browser_actions.upload_file(page, selector, str(value))
            
            if success:
                form_progress[field_name] = True
                filled_count += 1
                logger.info("field_filled", field=field_name, type=field_type)
            else:
                errors.append(f"Failed to fill field: {field_name}")
                logger.error("field_fill_failed", field=field_name)
        
        # Take screenshot of filled form
        screenshot_path = f"{config.SCREENSHOTS_DIR}/form_filled_{int(time.time())}.png"
        await browser_actions.take_screenshot(page, screenshot_path)
        
        # Extract DOM
        dom = await browser_actions.extract_dom_snapshot(page)
        
        logger.info(
            "form_expert_completed",
            filled=filled_count,
            total=len(field_mappings),
            errors=len(errors)
        )
        
        # Determine next action
        if errors:
            next_action = "audit"  # Let auditor check errors
        else:
            next_action = "audit"  # Always audit before proceeding
        
        return {
            "form_progress": form_progress,
            "screenshot_path": screenshot_path,
            "dom_snapshot": dom,
            "errors": errors if errors else [],
            "next_action": next_action,
            "last_update_time": time.time()
        }
    
    except Exception as e:
        logger.error("form_expert_node_error", error=str(e))
        return {
            "errors": [f"FormExpert error: {str(e)}"],
            "next_action": "error"
        }
