"""
Autonomous Browser Agent for MPOnline Portal
Demonstrates autonomous navigation, search, and form interaction
"""
import asyncio
import random
from playwright.async_api import async_playwright, Page
from datetime import datetime
import json


class AutonomousMPOnlineAgent:
    """Autonomous agent that can navigate and interact with MPOnline portal."""
    
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.actions_log = []
        
    async def start_browser(self):
        """Initialize browser with stealth settings."""
        print("🚀 Starting autonomous browser...")
        self.playwright = await async_playwright().start()
        
        # Launch with anti-detection settings
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
            ]
        )
        
        # Create realistic context
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-IN',
            timezone_id='Asia/Kolkata',
        )
        
        # Add stealth script
        await self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        self.page = await self.context.new_page()
        print("✅ Browser ready!")
        
    async def human_delay(self, min_ms: int = 1000, max_ms: int = 3000):
        """Add human-like delay."""
        delay = random.randint(min_ms, max_ms) / 1000
        await asyncio.sleep(delay)
        
    async def log_action(self, action: str, details: dict = None):
        """Log actions for transparency."""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "action": action,
            "details": details or {}
        }
        self.actions_log.append(log_entry)
        print(f"📝 {action}: {json.dumps(details, indent=2) if details else ''}")
        
    async def navigate_to_mponline(self):
        """Navigate to MPOnline homepage autonomously."""
        print("\n🌐 Navigating to MPOnline portal...")
        await self.log_action("navigate", {"url": "https://www.mponline.gov.in"})
        
        try:
            await self.page.goto("https://www.mponline.gov.in", wait_until="domcontentloaded", timeout=30000)
            await self.human_delay(2000, 4000)
            
            # Take screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"data/screenshots/mponline_homepage_{timestamp}.png"
            await self.page.screenshot(path=screenshot_path, full_page=True)
            await self.log_action("screenshot", {"path": screenshot_path})
            
            print(f"✅ Homepage loaded! Screenshot saved: {screenshot_path}")
            return True
            
        except Exception as e:
            await self.log_action("error", {"message": str(e)})
            print(f"❌ Error: {e}")
            return False
            
    async def discover_services(self):
        """Autonomously discover available services on the portal."""
        print("\n🔍 Discovering available services...")
        
        try:
            # Look for common service patterns
            service_selectors = [
                'a[href*="citizen"]',
                'a[href*="service"]',
                'a[href*="online"]',
                '.service-link',
                '.menu-item',
                'nav a',
            ]
            
            discovered_services = []
            
            for selector in service_selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    for element in elements[:10]:  # Limit to first 10
                        text = await element.text_content()
                        href = await element.get_attribute('href')
                        if text and text.strip():
                            discovered_services.append({
                                "text": text.strip(),
                                "href": href,
                                "selector": selector
                            })
                except:
                    continue
            
            # Deduplicate by text
            unique_services = {s['text']: s for s in discovered_services}.values()
            
            await self.log_action("services_discovered", {
                "count": len(unique_services),
                "services": list(unique_services)[:20]  # Log first 20
            })
            
            print(f"✅ Found {len(unique_services)} services!")
            for i, service in enumerate(list(unique_services)[:10], 1):
                print(f"   {i}. {service['text']}")
                
            return list(unique_services)
            
        except Exception as e:
            await self.log_action("error", {"message": str(e)})
            print(f"❌ Error discovering services: {e}")
            return []
            
    async def search_on_portal(self, search_query: str):
        """Autonomously find and use search functionality."""
        print(f"\n🔎 Searching for: '{search_query}'...")
        
        try:
            # Common search input selectors
            search_selectors = [
                'input[type="search"]',
                'input[name*="search"]',
                'input[placeholder*="Search"]',
                'input[placeholder*="search"]',
                '#search',
                '.search-input',
            ]
            
            search_input = None
            for selector in search_selectors:
                try:
                    search_input = await self.page.query_selector(selector)
                    if search_input:
                        print(f"✅ Found search input: {selector}")
                        break
                except:
                    continue
            
            if search_input:
                # Type search query with human-like behavior
                await search_input.click()
                await self.human_delay(500, 1000)
                await search_input.type(search_query, delay=random.randint(50, 150))
                await self.log_action("search_typed", {"query": search_query})
                
                # Try to submit
                await self.page.keyboard.press('Enter')
                await self.human_delay(2000, 3000)
                
                # Screenshot results
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"data/screenshots/search_results_{timestamp}.png"
                await self.page.screenshot(path=screenshot_path, full_page=True)
                await self.log_action("search_results", {"path": screenshot_path})
                
                print(f"✅ Search completed! Screenshot: {screenshot_path}")
                return True
            else:
                print("⚠️  No search input found on this page")
                return False
                
        except Exception as e:
            await self.log_action("error", {"message": str(e)})
            print(f"❌ Search error: {e}")
            return False
            
    async def click_service(self, service_name: str, services: list):
        """Autonomously click on a specific service."""
        print(f"\n🖱️  Attempting to click service: '{service_name}'...")
        
        try:
            # Find matching service
            matching_service = None
            for service in services:
                if service_name.lower() in service['text'].lower():
                    matching_service = service
                    break
            
            if not matching_service:
                print(f"⚠️  Service '{service_name}' not found in discovered services")
                return False
            
            # Click the service link
            await self.page.click(f'text="{matching_service["text"]}"')
            await self.human_delay(2000, 4000)
            
            await self.log_action("service_clicked", {
                "service": matching_service['text'],
                "url": self.page.url
            })
            
            # Screenshot after navigation
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"data/screenshots/service_page_{timestamp}.png"
            await self.page.screenshot(path=screenshot_path, full_page=True)
            
            print(f"✅ Navigated to: {self.page.url}")
            print(f"📸 Screenshot: {screenshot_path}")
            return True
            
        except Exception as e:
            await self.log_action("error", {"message": str(e)})
            print(f"❌ Click error: {e}")
            return False
            
    async def analyze_page(self):
        """Analyze current page for forms and interactive elements."""
        print("\n🔬 Analyzing current page...")
        
        try:
            # Find forms
            forms = await self.page.query_selector_all('form')
            print(f"📋 Found {len(forms)} forms")
            
            # Find input fields
            inputs = await self.page.query_selector_all('input')
            print(f"📝 Found {len(inputs)} input fields")
            
            # Categorize inputs
            input_types = {}
            for input_elem in inputs[:50]:  # Limit analysis
                input_type = await input_elem.get_attribute('type') or 'text'
                input_name = await input_elem.get_attribute('name') or 'unnamed'
                input_id = await input_elem.get_attribute('id') or 'no-id'
                placeholder = await input_elem.get_attribute('placeholder') or ''
                
                if input_type not in input_types:
                    input_types[input_type] = []
                
                input_types[input_type].append({
                    'name': input_name,
                    'id': input_id,
                    'placeholder': placeholder
                })
            
            await self.log_action("page_analyzed", {
                "url": self.page.url,
                "forms_count": len(forms),
                "inputs_count": len(inputs),
                "input_types": {k: len(v) for k, v in input_types.items()}
            })
            
            # Print summary
            print("\n📊 Page Analysis Summary:")
            print(f"   URL: {self.page.url}")
            print(f"   Forms: {len(forms)}")
            print(f"   Input Fields: {len(inputs)}")
            for input_type, fields in input_types.items():
                print(f"   - {input_type}: {len(fields)}")
                for field in fields[:3]:  # Show first 3
                    print(f"      • {field['name']} (ID: {field['id']})")
            
            return {
                'forms': len(forms),
                'inputs': len(inputs),
                'input_types': input_types
            }
            
        except Exception as e:
            await self.log_action("error", {"message": str(e)})
            print(f"❌ Analysis error: {e}")
            return None
            
    async def save_action_log(self):
        """Save all actions to a file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = f"data/logs/autonomous_agent_{timestamp}.json"
        
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(self.actions_log, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Action log saved: {log_path}")
        
    async def close(self):
        """Cleanup resources."""
        print("\n🛑 Closing browser...")
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("✅ Browser closed!")


async def main():
    """Main autonomous workflow."""
    print("=" * 60)
    print("🤖 MPOnline Autonomous Browser Agent")
    print("=" * 60)
    
    # Initialize agent
    agent = AutonomousMPOnlineAgent(headless=False)
    
    try:
        # Start browser
        await agent.start_browser()
        
        # Navigate to MPOnline
        if await agent.navigate_to_mponline():
            
            # Discover available services
            services = await agent.discover_services()
            
            # Optional: Search for something
            # await agent.search_on_portal("MPPSC")
            
            # Optional: Click on a specific service
            # if services:
            #     await agent.click_service("Citizen", services)
            
            # Analyze the current page
            await agent.analyze_page()
            
            # Save action log
            await agent.save_action_log()
            
            print("\n" + "=" * 60)
            print("✅ Autonomous exploration completed!")
            print("=" * 60)
            
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        
    finally:
        # Cleanup
        await agent.close()


if __name__ == "__main__":
    asyncio.run(main())
