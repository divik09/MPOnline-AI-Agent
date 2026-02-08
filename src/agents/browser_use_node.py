"""Browser-use agent node for AI-driven browser automation."""
import time
import asyncio
from typing import Dict, Any
from browser_use import Agent, Browser
from playwright.async_api import async_playwright, Browser as PlaywrightBrowser, Page

from src.core.agent_state import AgentState
from src.utils.browser_use_helper import (
    get_configured_llm,
    create_form_filling_task,
    extract_browser_use_result
)
from src.utils.logging_config import logger
from src import config


async def browser_use_node(state: AgentState) -> Dict[str, Any]:
    """
    Use browser-use library for AI-driven browser automation.
    
    This node:
    1. Creates a natural language task from user data
    2. Launches browser-use agent with configured LLM
    3. Agent searches Google for MPOnline
    4. Agent navigates to service page
    5. Agent fills form with user data
    6. Returns updated state with progress
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state dictionary
    """
    logger.info("browser_use_node_started", service_type=state.get("service_type"))
    
    start_time = time.time()
    user_data = state.get("user_data", {})
    service_type = state.get("service_type", "mppsc")
    
    try:
        # Create the task in natural language
        task = create_form_filling_task(user_data, service_type)
        logger.info("browser_use_task_created", task_length=len(task))
        
        # Get configured LLM
        llm = get_configured_llm()
        
        browser_instance = None
        playwright = None
        page = None
        
        # Get browser mode from state (allows runtime override)
        use_real_browser = state.get("use_real_browser", config.USE_REAL_BROWSER)
        
        # Choose between real Chrome browser or regular Playwright
        if use_real_browser:
            logger.info("browser_use_real_chrome", 
                       executable=config.CHROME_EXECUTABLE_PATH,
                       user_data_dir=config.CHROME_USER_DATA_DIR,
                       profile=config.CHROME_PROFILE)
            
            # Use real Chrome browser with user data
            browser_instance = Browser(
                executable_path=config.CHROME_EXECUTABLE_PATH,
                user_data_dir=config.CHROME_USER_DATA_DIR,
                profile_directory=config.CHROME_PROFILE,
                headless=False  # Real browser must be visible
            )
            
            # Create agent with Browser instance
            agent = Agent(
                task=task,
                llm=llm,
                browser=browser_instance
            )
        else:
            # Launch regular Playwright browser
            playwright = await async_playwright().start()
            browser = await playwright.chromium.launch(
                headless=config.HEADLESS_MODE,
                slow_mo=config.SLOW_MO
            )
            
            # Create a new page
            context = await browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            page = await context.new_page()
            
            logger.info("browser_use_playwright_launched", headless=config.HEADLESS_MODE)
            
            # Create browser-use agent with the page
            agent = Agent(
                task=task,
                llm=llm,
                browser=browser,
                browser_context=context
            )
        
        logger.info("browser_use_agent_created", task_preview=task[:100])
        
        # Run the agent
        logger.info("browser_use_agent_running", status="started")
        result = await agent.run()
        logger.info("browser_use_agent_completed", duration=time.time() - start_time)
        
        # Extract result information
        result_data = extract_browser_use_result(result)
        
        # Take screenshot of final state
        screenshot_path = None
        current_url = None
        
        try:
            # Get the page from the agent's browser context
            if use_real_browser:
                # For real browser, browser-use manages everything
                logger.info("browser_use_real_chrome_used", note="Browser remains open for user")
                # Extract URL from result if available
                current_url = result_data.get("final_url", "N/A")
            else:
                # For Playwright, we have direct access to page
                if page:
                    screenshot_path = config.DATA_DIR / "screenshots" / f"browser_use_{int(time.time())}.png"
                    screenshot_path.parent.mkdir(parents=True, exist_ok=True)
                    await page.screenshot(path=str(screenshot_path), full_page=True)
                    logger.info("browser_use_screenshot_saved", path=str(screenshot_path))
                    current_url = page.url
        except Exception as e:
            logger.warning("browser_use_screenshot_failed", error=str(e))
        
        # Cleanup (only for Playwright, not real browser)
        if not use_real_browser and playwright:
            await browser.close()
            await playwright.stop()
            logger.info("browser_use_playwright_closed")
        
        # Determine if form was successfully filled
        # In a real scenario, we'd verify fields, but for now we trust the AI
        success = result_data.get("success", False)
        
        # Update state
        return {
            "current_step": "form_filled" if success else "error",
            "current_url": current_url,
            "screenshot_path": str(screenshot_path) if screenshot_path else None,
            "form_progress": {
                field: True for field in user_data.keys()
            } if success else {},
            "errors": result_data.get("errors", []) if not success else [],
            "next_action": "captcha" if success else "error",
            "last_update_time": time.time(),
            "messages": state.get("messages", []) + [{
                "role": "assistant",
                "content": f"AI agent completed form filling. Actions: {len(result_data.get('actions_taken', []))}"
            }]
        }
        
    except Exception as e:
        logger.error("browser_use_node_error", error=str(e), traceback=True)
        
        return {
            "current_step": "error",
            "errors": state.get("errors", []) + [f"Browser-use error: {str(e)}"],
            "next_action": "error",
            "last_update_time": time.time()
        }


async def test_browser_use_simple() -> bool:
    """
    Simple test function for browser-use integration.
    
    Returns:
        True if test passes, False otherwise
    """
    print("\n🧪 Testing Browser-Use Integration\n")
    
    try:
        # Create test state
        test_state: AgentState = {
            "user_data": {
                "full_name": "Test User",
                "email": "test@example.com",
                "mobile": "9876543210"
            },
            "service_type": "mppsc",
            "current_step": "start",
            "form_progress": {},
            "dom_snapshot": None,
            "screenshot_path": None,
            "current_url": None,
            "session_data": {},
            "errors": [],
            "messages": [],
            "next_action": "navigate",
            "captcha_solution": None,
            "payment_confirmed": False,
            "attempt_count": {},
            "start_time": time.time(),
            "last_update_time": time.time()
        }
        
        print("✅ Test state created")
        print(f"   Service: {test_state['service_type']}")
        print(f"   User: {test_state['user_data']['full_name']}")
        
        # Run browser-use node
        print("\n🚀 Running browser-use automation...")
        result = await browser_use_node(test_state)
        
        print(f"\n✅ Browser-use completed!")
        print(f"   Current step: {result.get('current_step')}")
        print(f"   URL: {result.get('current_url','N/A')}")
        print(f"   Errors: {len(result.get('errors', []))}")
        
        if result.get('screenshot_path'):
            print(f"   Screenshot: {result.get('screenshot_path')}")
        
        return result.get("current_step") != "error"
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Run test
    success = asyncio.run(test_browser_use_simple())
    exit(0 if success else 1)
