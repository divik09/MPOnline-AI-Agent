"""Navigator agent node - handles URL routing and login."""
import time
from typing import Any
from src.core.agent_state import AgentState
from src.automation.browser_manager import browser_manager
from src.automation import browser_actions
from src import config
from src.utils.logging_config import logger
from src.services.service_registry import SERVICE_REGISTRY


async def navigator_node(state: AgentState) -> dict[str, Any]:
    """
    Navigator agent handles:
    - Routing to correct service URL
    - Performing login
    - Session management
    - Multi-page navigation
    
    Args:
        state: Current agent state
        
    Returns:
        Partial state update
    """
    logger.info("navigator_node_started", service=state["service_type"], step=state["current_step"])
    
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
        
        # Handle different navigation steps
        current_step = state.get("current_step", "start")
        
        if current_step == "start":
            # Navigate to service URL
            url = service_template.get_url()
            await page.goto(url)
            logger.info("navigated_to_service", url=url)
            
            # Take screenshot
            screenshot_path = f"{config.SCREENSHOTS_DIR}/nav_start_{int(time.time())}.png"
            await browser_actions.take_screenshot(page, screenshot_path)
            
            # Extract DOM
            dom = await browser_actions.extract_dom_snapshot(page)
            
            return {
                "current_step": "login",
                "current_url": url,
                "screenshot_path": screenshot_path,
                "dom_snapshot": dom,
                "next_action": "navigate",
                "last_update_time": time.time()
            }
        
        elif current_step == "login":
            # Perform login if required
            login_success = await _perform_login(page, service_template)
            
            if not login_success:
                return {
                    "errors": ["Login failed"],
                    "next_action": "error"
                }
            
            # Take screenshot after login
            screenshot_path = f"{config.SCREENSHOTS_DIR}/nav_login_{int(time.time())}.png"
            await browser_actions.take_screenshot(page, screenshot_path)
            
            dom = await browser_actions.extract_dom_snapshot(page)
            
            return {
                "current_step": "form_fill",
                "screenshot_path": screenshot_path,
                "dom_snapshot": dom,
                "next_action": "fill_form",
                "last_update_time": time.time()
            }
        
        elif current_step in ["document_upload", "preview", "payment"]:
            # Navigate to specific step if not already there
            nav_success = await _navigate_to_step(page, service_template, current_step)
            
            if not nav_success:
                return {
                    "errors": [f"Failed to navigate to {current_step}"],
                    "next_action": "error"
                }
            
            screenshot_path = f"{config.SCREENSHOTS_DIR}/nav_{current_step}_{int(time.time())}.png"
            await browser_actions.take_screenshot(page, screenshot_path)
            
            dom = await browser_actions.extract_dom_snapshot(page)
            
            return {
                "screenshot_path": screenshot_path,
                "dom_snapshot": dom,
                "current_url": page.url,
                "next_action": state.get("next_action", "continue"),
                "last_update_time": time.time()
            }
        
        else:
            logger.warning("navigator_unknown_step", step=current_step)
            return {
                "next_action": "continue"
            }
    
    except Exception as e:
        logger.error("navigator_node_error", error=str(e))
        return {
            "errors": [f"Navigator error: {str(e)}"],
            "next_action": "error"
        }


async def _perform_login(page, service_template) -> bool:
    """Perform login to MPOnline portal."""
    try:
        # Check if login is needed
        login_selectors = service_template.get_login_selectors()
        if not login_selectors:
            logger.info("login_not_required")
            return True
        
        # Check if already logged in
        if await browser_actions.wait_for_selector(
            page,
            login_selectors.get("logged_in_indicator", ""),
            timeout=3000
        ):
            logger.info("already_logged_in")
            return True
        
        # Fill username
        username_filled = await browser_actions.safe_fill(
            page,
            login_selectors["username"],
            config.MPONLINE_USERNAME
        )
        
        if not username_filled:
            logger.error("login_username_failed")
            return False
        
        # Fill password
        password_filled = await browser_actions.safe_fill(
            page,
            login_selectors["password"],
            config.MPONLINE_PASSWORD
        )
        
        if not password_filled:
            logger.error("login_password_failed")
            return False
        
        # Click login button
        login_clicked = await browser_actions.safe_click(
            page,
            login_selectors["submit"]
        )
        
        if not login_clicked:
            logger.error("login_submit_failed")
            return False
        
        # Wait for successful login
        await page.wait_for_load_state("networkidle")
        
        logger.info("login_successful")
        return True
        
    except Exception as e:
        logger.error("login_error", error=str(e))
        return False


async def _navigate_to_step(page, service_template, step: str) -> bool:
    """Navigate to a specific step in multi-page forms."""
    try:
        # This would be service-specific
        # For now, just verify we're on the right page
        await page.wait_for_load_state("domcontentloaded")
        return True
    except Exception as e:
        logger.error("navigation_error", step=step, error=str(e))
        return False
