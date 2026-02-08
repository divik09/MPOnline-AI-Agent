"""CAPTCHA handler node - manages HITL for CAPTCHA solving."""
import time
from typing import Any
from src.core.agent_state import AgentState
from src.automation.browser_manager import browser_manager
from src.automation import browser_actions
from src.tools.human_input_tool import human_input_tool
from src import config
from src.utils.logging_config import logger


async def captcha_node(state: AgentState) -> dict[str, Any]:
    """
    CAPTCHA handler with Human-in-the-Loop:
    - Detects CAPTCHA presence
    - Takes screenshot
    - Interrupts graph execution
    - Waits for human input
    - Submits CAPTCHA solution
    
    Args:
        state: Current agent state
        
    Returns:
        Partial state update
    """
    logger.info("captcha_node_started")
    
    try:
        # Get page
        page = await browser_manager.get_page()
        
        # Check if CAPTCHA solution already provided
        if state.get("captcha_solution"):
            # Submit the solution
            success = await _submit_captcha(page, state["captcha_solution"])
            
            if success:
                logger.info("captcha_submitted_successfully")
                return {
                    "captcha_solution": None,  # Clear solution
                    "next_action": "continue",
                    "last_update_time": time.time()
                }
            else:
                return {
                    "errors": ["Failed to submit CAPTCHA solution"],
                    "captcha_solution": None,
                    "next_action": "error"
                }
        
        # Detect CAPTCHA
        captcha_present = await _detect_captcha(page)
        
        if not captcha_present:
            logger.info("no_captcha_detected")
            return {
                "next_action": "continue",
                "last_update_time": time.time()
            }
        
        # Take screenshot of CAPTCHA
        screenshot_path = f"{config.SCREENSHOTS_DIR}/captcha_{int(time.time())}.png"
        await browser_actions.take_screenshot(page, screenshot_path)
        
        logger.info("captcha_detected", screenshot=screenshot_path)
        
        # Request human input
        request_id = f"captcha_{int(time.time())}"
        
        solution = await human_input_tool.request_input(
            request_id=request_id,
            prompt="Please solve the CAPTCHA visible in the screenshot",
            input_type="text",
            timeout=config.CAPTCHA_TIMEOUT
        )
        
        if not solution:
            logger.warning("captcha_timeout")
            return {
                "errors": ["CAPTCHA solving timed out"],
                "next_action": "error"
            }
        
        # Submit CAPTCHA
        success = await _submit_captcha(page, solution)
        
        if success:
            logger.info("captcha_solved")
            return {
                "screenshot_path": screenshot_path,
                "next_action": "continue",
                "last_update_time": time.time()
            }
        else:
            logger.error("captcha_submission_failed")
            return {
                "errors": ["Failed to submit CAPTCHA"],
                "next_action": "error"
            }
    
    except Exception as e:
        logger.error("captcha_node_error", error=str(e))
        return {
            "errors": [f"CAPTCHA error: {str(e)}"],
            "next_action": "error"
        }


async def _detect_captcha(page) -> bool:
    """Detect if CAPTCHA is present on page."""
    # Common CAPTCHA selectors
    captcha_selectors = [
        "#captcha",
        ".captcha",
        "[name='captcha']",
        "img[alt*='captcha' i]",
        "img[src*='captcha' i]",
        "#ctl00_ContentPlaceHolder1_CaptchaImage",  # Common MPOnline selector
        ".captcha-image"
    ]
    
    for selector in captcha_selectors:
        try:
            if await browser_actions.wait_for_selector(page, selector, timeout=2000):
                logger.info("captcha_found", selector=selector)
                return True
        except Exception:
            continue
    
    return False


async def _submit_captcha(page, solution: str) -> bool:
    """Submit CAPTCHA solution."""
    # Common CAPTCHA input selectors
    input_selectors = [
        "#captchaInput",
        "[name='captcha']",
        "[placeholder*='captcha' i]",
        "#ctl00_ContentPlaceHolder1_txtCaptcha",
        ".captcha-input"
    ]
    
    for selector in input_selectors:
        try:
            if await browser_actions.safe_fill(page, selector, solution, timeout=3000):
                logger.info("captcha_filled", selector=selector)
                
                # Try to find and click submit button
                submit_selectors = [
                    "button[type='submit']",
                    "input[type='submit']",
                    "#btnSubmit",
                    ".submit-btn"
                ]
                
                for submit_selector in submit_selectors:
                    if await browser_actions.safe_click(page, submit_selector, timeout=3000):
                        logger.info("captcha_submitted", selector=submit_selector)
                        await page.wait_for_load_state("networkidle", timeout=10000)
                        return True
                
                # If no submit button found, just return success
                return True
        except Exception as e:
            logger.warning("captcha_submit_attempt_failed", selector=selector, error=str(e))
            continue
    
    return False
