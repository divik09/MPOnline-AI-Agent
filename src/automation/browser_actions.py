"""Browser automation actions with retry logic and human-like behavior."""
import asyncio
import random
from typing import Optional
from playwright.async_api import Page, ElementHandle, TimeoutError as PlaywrightTimeout
from src import config
from src.utils.logging_config import logger


async def safe_click(
    page: Page,
    selector: str,
    timeout: int = config.BROWSER_TIMEOUT,
    retries: int = 3
) -> bool:
    """
    Click an element with retry logic and human-like delay.
    
    Args:
        page: Playwright page object
        selector: CSS selector or XPath
        timeout: Maximum wait time in ms
        retries: Number of retry attempts
        
    Returns:
        True if successful, False otherwise
    """
    for attempt in range(retries):
        try:
            # Wait for element to be visible and enabled
            await page.wait_for_selector(selector, state="visible", timeout=timeout)
            
            # Random delay before clicking (mimic human)
            delay = random.randint(config.MIN_DELAY, config.MAX_DELAY) / 1000
            await asyncio.sleep(delay)
            
            # Click the element
            await page.click(selector)
            
            logger.info("safe_click_success", selector=selector, attempt=attempt + 1)
            return True
            
        except PlaywrightTimeout:
            logger.warning(
                "safe_click_timeout",
                selector=selector,
                attempt=attempt + 1,
                retries=retries
            )
            if attempt == retries - 1:
                logger.error("safe_click_failed", selector=selector)
                return False
            await asyncio.sleep(1)  # Wait before retry
            
        except Exception as e:
            logger.error(
                "safe_click_error",
                selector=selector,
                error=str(e),
                attempt=attempt + 1
            )
            if attempt == retries - 1:
                return False
            await asyncio.sleep(1)
    
    return False


async def safe_fill(
    page: Page,
    selector: str,
    text: str,
    timeout: int = config.BROWSER_TIMEOUT,
    retries: int = 3
) -> bool:
    """
    Fill an input field with human-like typing speed.
    
    Args:
        page: Playwright page object
        selector: CSS selector or XPath
        text: Text to fill
        timeout: Maximum wait time in ms
        retries: Number of retry attempts
        
    Returns:
        True if successful, False otherwise
    """
    for attempt in range(retries):
        try:
            # Wait for element
            await page.wait_for_selector(selector, state="visible", timeout=timeout)
            
            # Random delay before typing
            delay = random.randint(config.MIN_DELAY, config.MAX_DELAY) / 1000
            await asyncio.sleep(delay)
            
            # Clear existing text
            await page.fill(selector, "")
            
            # Type with human-like speed
            await page.type(selector, text, delay=config.TYPING_SPEED)
            
            logger.info(
                "safe_fill_success",
                selector=selector,
                text_length=len(text),
                attempt=attempt + 1
            )
            return True
            
        except PlaywrightTimeout:
            logger.warning(
                "safe_fill_timeout",
                selector=selector,
                attempt=attempt + 1,
                retries=retries
            )
            if attempt == retries - 1:
                logger.error("safe_fill_failed", selector=selector)
                return False
            await asyncio.sleep(1)
            
        except Exception as e:
            logger.error(
                "safe_fill_error",
                selector=selector,
                error=str(e),
                attempt=attempt + 1
            )
            if attempt == retries - 1:
                return False
            await asyncio.sleep(1)
    
    return False


async def safe_select(
    page: Page,
    selector: str,
    value: str,
    timeout: int = config.BROWSER_TIMEOUT,
    retries: int = 3
) -> bool:
    """
    Select an option from a dropdown.
    
    Args:
        page: Playwright page object
        selector: CSS selector for dropdown
        value: Option value to select
        timeout: Maximum wait time in ms
        retries: Number of retry attempts
        
    Returns:
        True if successful, False otherwise
    """
    for attempt in range(retries):
        try:
            await page.wait_for_selector(selector, state="visible", timeout=timeout)
            
            delay = random.randint(config.MIN_DELAY, config.MAX_DELAY) / 1000
            await asyncio.sleep(delay)
            
            await page.select_option(selector, value)
            
            logger.info(
                "safe_select_success",
                selector=selector,
                value=value,
                attempt=attempt + 1
            )
            return True
            
        except PlaywrightTimeout:
            logger.warning(
                "safe_select_timeout",
                selector=selector,
                attempt=attempt + 1
            )
            if attempt == retries - 1:
                return False
            await asyncio.sleep(1)
            
        except Exception as e:
            logger.error("safe_select_error", selector=selector, error=str(e))
            if attempt == retries - 1:
                return False
            await asyncio.sleep(1)
    
    return False


async def wait_for_selector(
    page: Page,
    selector: str,
    state: str = "visible",
    timeout: int = config.BROWSER_TIMEOUT
) -> bool:
    """
    Wait for a selector with timeout handling.
    
    Args:
        page: Playwright page object
        selector: CSS selector or XPath
        state: Element state to wait for
        timeout: Maximum wait time in ms
        
    Returns:
        True if found, False otherwise
    """
    try:
        await page.wait_for_selector(selector, state=state, timeout=timeout)
        logger.info("wait_for_selector_success", selector=selector, state=state)
        return True
    except PlaywrightTimeout:
        logger.warning("wait_for_selector_timeout", selector=selector, state=state)
        return False
    except Exception as e:
        logger.error("wait_for_selector_error", selector=selector, error=str(e))
        return False


async def extract_dom_snapshot(page: Page) -> str:
    """
    Extract page accessibility tree for LLM consumption.
    
    Args:
        page: Playwright page object
        
    Returns:
        Accessibility tree as string
    """
    try:
        # Get accessibility snapshot
        snapshot = await page.accessibility.snapshot()
        
        # Convert to simplified string format
        def format_node(node, indent=0):
            if not node:
                return ""
            
            lines = []
            role = node.get("role", "")
            name = node.get("name", "")
            value = node.get("value", "")
            
            if role:
                line = "  " * indent + f"{role}"
                if name:
                    line += f': "{name}"'
                if value:
                    line += f' = "{value}"'
                lines.append(line)
            
            for child in node.get("children", []):
                lines.append(format_node(child, indent + 1))
            
            return "\n".join(filter(None, lines))
        
        result = format_node(snapshot)
        logger.info("dom_snapshot_extracted", length=len(result))
        return result
        
    except Exception as e:
        logger.error("dom_snapshot_error", error=str(e))
        return ""


async def take_screenshot(page: Page, path: str) -> bool:
    """
    Take screenshot of current page.
    
    Args:
        page: Playwright page object
        path: File path to save screenshot
        
    Returns:
        True if successful, False otherwise
    """
    try:
        await page.screenshot(path=path, full_page=True)
        logger.info("screenshot_taken", path=path)
        return True
    except Exception as e:
        logger.error("screenshot_error", path=path, error=str(e))
        return False


async def upload_file(
    page: Page,
    selector: str,
    file_path: str,
    timeout: int = config.BROWSER_TIMEOUT
) -> bool:
    """
    Upload a file to an input element.
    
    Args:
        page: Playwright page object
        selector: CSS selector for file input
        file_path: Path to file to upload
        timeout: Maximum wait time in ms
        
    Returns:
        True if successful, False otherwise
    """
    try:
        await page.wait_for_selector(selector, state="attached", timeout=timeout)
        
        delay = random.randint(config.MIN_DELAY, config.MAX_DELAY) / 1000
        await asyncio.sleep(delay)
        
        await page.set_input_files(selector, file_path)
        
        logger.info("file_upload_success", selector=selector, file=file_path)
        return True
        
    except Exception as e:
        logger.error("file_upload_error", selector=selector, error=str(e))
        return False
