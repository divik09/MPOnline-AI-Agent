"""Browser manager for Playwright context and session management."""
import asyncio
from typing import Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Playwright
from src import config
from src.utils.logging_config import logger


class BrowserManager:
    """
    Manages Playwright browser lifecycle and session persistence.
    """
    
    def __init__(self):
        """Initialize browser manager."""
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self._lock = asyncio.Lock()
    
    async def start(self) -> Page:
        """
        Start browser and return page instance.
        
        Returns:
            Playwright page object
        """
        async with self._lock:
            if self.page:
                return self.page
            
            logger.info("browser_starting", headless=config.HEADLESS_MODE)
            
            # Launch Playwright
            self.playwright = await async_playwright().start()
            
            # Launch browser with stealth settings
            self.browser = await self.playwright.chromium.launch(
                headless=config.HEADLESS_MODE,
                slow_mo=config.SLOW_MO,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                ]
            )
            
            # Create context with realistic settings
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                locale='en-IN',
                timezone_id='Asia/Kolkata',
                permissions=['geolocation'],
                color_scheme='light',
            )
            
            # Add stealth scripts
            await self.context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)
            
            # Create page
            self.page = await self.context.new_page()
            
            # Set default timeout
            self.page.set_default_timeout(config.BROWSER_TIMEOUT)
            
            logger.info("browser_started")
            return self.page
    
    async def save_session(self, state_path: str):
        """
        Save browser session state (cookies, storage).
        
        Args:
            state_path: Path to save state file
        """
        if self.context:
            try:
                await self.context.storage_state(path=state_path)
                logger.info("session_saved", path=state_path)
            except Exception as e:
                logger.error("session_save_error", error=str(e))
    
    async def load_session(self, state_path: str):
        """
        Load browser session state.
        
        Args:
            state_path: Path to saved state file
        """
        try:
            if self.playwright and not self.context:
                self.context = await self.playwright.chromium.new_context(
                    storage_state=state_path
                )
                self.page = await self.context.new_page()
                logger.info("session_loaded", path=state_path)
        except Exception as e:
            logger.error("session_load_error", error=str(e))
    
    async def get_page(self) -> Page:
        """
        Get current page or create new one.
        
        Returns:
            Playwright page object
        """
        if not self.page:
            return await self.start()
        return self.page
    
    async def close(self):
        """Close browser and cleanup resources."""
        async with self._lock:
            try:
                if self.page:
                    await self.page.close()
                    self.page = None
                
                if self.context:
                    await self.context.close()
                    self.context = None
                
                if self.browser:
                    await self.browser.close()
                    self.browser = None
                
                if self.playwright:
                    await self.playwright.stop()
                    self.playwright = None
                
                logger.info("browser_closed")
                
            except Exception as e:
                logger.error("browser_close_error", error=str(e))
    
    async def __aenter__(self):
        """Async context manager entry."""
        return await self.start()
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()


# Global browser manager instance
browser_manager = BrowserManager()
