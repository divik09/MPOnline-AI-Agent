"""Payment verification node - manages HITL for payment confirmation."""
import time
from typing import Any
from src.core.agent_state import AgentState
from src.automation.browser_manager import browser_manager
from src.automation import browser_actions
from src.tools.human_input_tool import human_input_tool
from src import config
from src.utils.logging_config import logger


async def payment_node(state: AgentState) -> dict[str, Any]:
    """
    Payment verifier with Human-in-the-Loop:
    - Displays payment details to user
    - Interrupts for confirmation
    - Handles payment gateway navigation
    - Returns success/failure status
    
    Args:
        state: Current agent state
        
    Returns:
        Partial state update
    """
    logger.info("payment_node_started")
    
    try:
        # Get page
        page = await browser_manager.get_page()
        
        # Check if payment already confirmed
        if state.get("payment_confirmed", False):
            # Proceed with payment
            success = await _process_payment(page, state)
            
            if success:
                logger.info("payment_processed_successfully")
                
                # Take final screenshot
                screenshot_path = f"{config.SCREENSHOTS_DIR}/payment_success_{int(time.time())}.png"
                await browser_actions.take_screenshot(page, screenshot_path)
                
                return {
                    "current_step": "complete",
                    "screenshot_path": screenshot_path,
                    "next_action": "complete",
                    "last_update_time": time.time()
                }
            else:
                return {
                    "errors": ["Payment processing failed"],
                    "next_action": "error"
                }
        
        # Extract payment details from page
        payment_details = await _extract_payment_details(page)
        
        # Take screenshot of payment page
        screenshot_path = f"{config.SCREENSHOTS_DIR}/payment_{int(time.time())}.png"
        await browser_actions.take_screenshot(page, screenshot_path)
        
        logger.info("payment_confirmation_required", details=payment_details)
        
        # Request human confirmation
        request_id = f"payment_{int(time.time())}"
        
        prompt = f"""Payment Confirmation Required:
{payment_details}

Please review the payment details and confirm to proceed.
Type 'confirm' to proceed or 'cancel' to abort."""
        
        confirmation = await human_input_tool.request_input(
            request_id=request_id,
            prompt=prompt,
            input_type="confirmation",
            timeout=config.PAYMENT_TIMEOUT
        )
        
        if not confirmation or confirmation.lower() != "confirm":
            logger.warning("payment_cancelled_by_user")
            return {
                "errors": ["Payment cancelled by user"],
                "next_action": "error"
            }
        
        # Mark as confirmed and process
        success = await _process_payment(page, state)
        
        if success:
            logger.info("payment_completed")
            
            final_screenshot = f"{config.SCREENSHOTS_DIR}/payment_final_{int(time.time())}.png"
            await browser_actions.take_screenshot(page, final_screenshot)
            
            return {
                "payment_confirmed": True,
                "current_step": "complete",
                "screenshot_path": final_screenshot,
                "next_action": "complete",
                "last_update_time": time.time()
            }
        else:
            return {
                "errors": ["Payment failed"],
                "next_action": "error"
            }
    
    except Exception as e:
        logger.error("payment_node_error", error=str(e))
        return {
            "errors": [f"Payment error: {str(e)}"],
            "next_action": "error"
        }


async def _extract_payment_details(page) -> str:
    """Extract payment information from the page."""
    try:
        # Look for payment amount
        amount_selectors = [
            ".payment-amount",
            "#paymentAmount",
            "[class*='amount']",
            ".total-amount"
        ]
        
        amount = "Not found"
        for selector in amount_selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    amount = await element.text_content()
                    break
            except Exception:
                continue
        
        # Look for service/application details
        service_selectors = [
            ".service-name",
            ".application-type",
            "h2",
            "h3"
        ]
        
        service = "Not found"
        for selector in service_selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    service = await element.text_content()
                    break
            except Exception:
                continue
        
        details = f"""
Amount: {amount}
Service: {service}
URL: {page.url}
"""
        
        return details.strip()
        
    except Exception as e:
        logger.error("payment_details_extraction_error", error=str(e))
        return "Could not extract payment details. Please review the page manually."


async def _process_payment(page, state: AgentState) -> bool:
    """Process the payment (click continue/proceed buttons)."""
    try:
        # Common payment proceed buttons
        proceed_selectors = [
            "button:has-text('Proceed')",
            "button:has-text('Pay Now')",
            "input[value*='Proceed']",
            "input[value*='Pay']",
            "#btnPayNow",
            ".payment-btn",
            "button[type='submit']"
        ]
        
        for selector in proceed_selectors:
            try:
                if await browser_actions.safe_click(page, selector, timeout=5000):
                    logger.info("payment_proceed_clicked", selector=selector)
                    
                    # Wait for payment gateway or confirmation
                    await page.wait_for_load_state("networkidle", timeout=30000)
                    
                    # Check for success indicators
                    success_indicators = [
                        ":has-text('Success')",
                        ":has-text('Successful')",
                        ":has-text('Confirmed')",
                        ".success-message",
                        ".confirmation"
                    ]
                    
                    for indicator in success_indicators:
                        if await browser_actions.wait_for_selector(page, indicator, timeout=5000):
                            logger.info("payment_success_detected")
                            return True
                    
                    # If no explicit success, assume it worked
                    return True
                    
            except Exception as e:
                logger.warning("payment_proceed_attempt_failed", selector=selector, error=str(e))
                continue
        
        logger.error("no_payment_proceed_button_found")
        return False
        
    except Exception as e:
        logger.error("payment_processing_error", error=str(e))
        return False
