"""
Advanced Autonomous Form Filling Agent for MPOnline
Demonstrates intelligent form detection, filling, and submission
"""
import asyncio
import random
from playwright.async_api import async_playwright, Page
from datetime import datetime
import json
from typing import Dict, List, Optional


class AdvancedFormFillingAgent:
    """
    Autonomous agent that can intelligently detect and fill forms.
    Integrates with your existing MPOnline Agent architecture.
    """
    
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.actions_log = []
        self.form_data = {}
        
    async def start_browser(self):
        """Initialize browser with stealth settings."""
        print("🚀 Starting advanced form filling agent...")
        self.playwright = await async_playwright().start()
        
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
            ]
        )
        
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            locale='en-IN',
            timezone_id='Asia/Kolkata',
        )
        
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
        icon = {
            "navigate": "🌐",
            "screenshot": "📸",
            "form_detected": "📋",
            "field_filled": "✏️",
            "submit": "🚀",
            "error": "❌",
            "success": "✅"
        }.get(action, "📝")
        print(f"{icon} {action}: {details.get('message', '') if details else ''}")
        
    async def navigate_to_service(self, url: str):
        """Navigate to a specific MPOnline service."""
        print(f"\n🌐 Navigating to: {url}")
        await self.log_action("navigate", {"url": url})
        
        try:
            await self.page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await self.human_delay(2000, 4000)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"data/screenshots/service_page_{timestamp}.png"
            await self.page.screenshot(path=screenshot_path, full_page=True)
            await self.log_action("screenshot", {"path": screenshot_path})
            
            print(f"✅ Page loaded! Screenshot: {screenshot_path}")
            return True
            
        except Exception as e:
            await self.log_action("error", {"message": str(e)})
            print(f"❌ Navigation error: {e}")
            return False
            
    async def detect_form_fields(self) -> List[Dict]:
        """
        Intelligently detect all fillable form fields on the page.
        Returns structured information about each field.
        """
        print("\n🔍 Detecting form fields...")
        
        try:
            fields = []
            
            # Detect all input fields
            inputs = await self.page.query_selector_all('input:not([type="hidden"]):not([type="submit"])')
            
            for i, input_elem in enumerate(inputs):
                try:
                    field_info = {
                        'element': input_elem,
                        'type': await input_elem.get_attribute('type') or 'text',
                        'name': await input_elem.get_attribute('name') or f'field_{i}',
                        'id': await input_elem.get_attribute('id') or '',
                        'placeholder': await input_elem.get_attribute('placeholder') or '',
                        'required': await input_elem.get_attribute('required') is not None,
                        'value': await input_elem.get_attribute('value') or '',
                    }
                    
                    # Try to find associated label
                    label_text = ''
                    if field_info['id']:
                        label = await self.page.query_selector(f'label[for="{field_info["id"]}"]')
                        if label:
                            label_text = await label.text_content()
                    
                    field_info['label'] = label_text.strip() if label_text else ''
                    fields.append(field_info)
                    
                except Exception as e:
                    print(f"⚠️  Error processing input field: {e}")
                    continue
            
            # Detect select dropdowns
            selects = await self.page.query_selector_all('select')
            
            for i, select_elem in enumerate(selects):
                try:
                    field_info = {
                        'element': select_elem,
                        'type': 'select',
                        'name': await select_elem.get_attribute('name') or f'select_{i}',
                        'id': await select_elem.get_attribute('id') or '',
                        'required': await select_elem.get_attribute('required') is not None,
                    }
                    
                    # Get options
                    options = await select_elem.query_selector_all('option')
                    option_values = []
                    for opt in options:
                        value = await opt.get_attribute('value')
                        text = await opt.text_content()
                        if value and text:
                            option_values.append({'value': value, 'text': text.strip()})
                    
                    field_info['options'] = option_values
                    
                    # Try to find label
                    label_text = ''
                    if field_info['id']:
                        label = await self.page.query_selector(f'label[for="{field_info["id"]}"]')
                        if label:
                            label_text = await label.text_content()
                    
                    field_info['label'] = label_text.strip() if label_text else ''
                    fields.append(field_info)
                    
                except Exception as e:
                    print(f"⚠️  Error processing select field: {e}")
                    continue
            
            # Detect textareas
            textareas = await self.page.query_selector_all('textarea')
            
            for i, textarea_elem in enumerate(textareas):
                try:
                    field_info = {
                        'element': textarea_elem,
                        'type': 'textarea',
                        'name': await textarea_elem.get_attribute('name') or f'textarea_{i}',
                        'id': await textarea_elem.get_attribute('id') or '',
                        'placeholder': await textarea_elem.get_attribute('placeholder') or '',
                        'required': await textarea_elem.get_attribute('required') is not None,
                    }
                    
                    # Try to find label
                    label_text = ''
                    if field_info['id']:
                        label = await self.page.query_selector(f'label[for="{field_info["id"]}"]')
                        if label:
                            label_text = await label.text_content()
                    
                    field_info['label'] = label_text.strip() if label_text else ''
                    fields.append(field_info)
                    
                except Exception as e:
                    print(f"⚠️  Error processing textarea field: {e}")
                    continue
            
            await self.log_action("form_detected", {
                "fields_count": len(fields),
                "message": f"Found {len(fields)} fillable fields"
            })
            
            # Print summary
            print(f"\n📋 Detected {len(fields)} fillable fields:")
            for idx, field in enumerate(fields[:20], 1):  # Show first 20
                label = field.get('label', '')
                name = field.get('name', '')
                ftype = field.get('type', '')
                required = "✓" if field.get('required') else ""
                print(f"   {idx}. [{ftype}] {label or name} {required}")
            
            return fields
            
        except Exception as e:
            await self.log_action("error", {"message": str(e)})
            print(f"❌ Form detection error: {e}")
            return []
            
    async def fill_field(self, field: Dict, value: str):
        """
        Fill a single form field with human-like behavior.
        """
        try:
            field_type = field['type']
            element = field['element']
            
            # Scroll into view
            await element.scroll_into_view_if_needed()
            await self.human_delay(500, 1000)
            
            if field_type == 'text' or field_type == 'email' or field_type == 'tel':
                # Click and clear
                await element.click()
                await self.human_delay(300, 600)
                await element.fill('')
                
                # Type with human-like delays
                for char in value:
                    await element.type(char, delay=random.randint(50, 150))
                
                await self.log_action("field_filled", {
                    "field": field.get('label') or field.get('name'),
                    "type": field_type,
                    "message": f"Filled with: {value}"
                })
                
            elif field_type == 'select':
                # Select option
                options = field.get('options', [])
                if options:
                    # Try to match value or text
                    selected = False
                    for opt in options:
                        if value.lower() in opt['text'].lower() or value == opt['value']:
                            await element.select_option(opt['value'])
                            selected = True
                            break
                    
                    if selected:
                        await self.log_action("field_filled", {
                            "field": field.get('label') or field.get('name'),
                            "type": "select",
                            "message": f"Selected: {value}"
                        })
                
            elif field_type == 'textarea':
                await element.click()
                await self.human_delay(300, 600)
                await element.fill(value)
                
                await self.log_action("field_filled", {
                    "field": field.get('label') or field.get('name'),
                    "type": "textarea",
                    "message": f"Filled textarea"
                })
                
            elif field_type == 'checkbox' or field_type == 'radio':
                if value.lower() in ['true', 'yes', '1', 'on']:
                    await element.check()
                    await self.log_action("field_filled", {
                        "field": field.get('label') or field.get('name'),
                        "type": field_type,
                        "message": "Checked"
                    })
            
            await self.human_delay(500, 1000)
            return True
            
        except Exception as e:
            await self.log_action("error", {"message": f"Error filling field: {e}"})
            print(f"❌ Error filling field {field.get('name')}: {e}")
            return False
            
    async def auto_fill_form(self, form_data: Dict[str, str]):
        """
        Automatically fill a form with provided data.
        Matches fields by name, id, or label.
        """
        print("\n📝 Auto-filling form...")
        
        # Detect all fields
        fields = await self.detect_form_fields()
        
        if not fields:
            print("⚠️  No fields detected!")
            return False
        
        # Match and fill fields
        filled_count = 0
        for field in fields:
            field_identifier = field.get('name') or field.get('id') or field.get('label')
            
            # Try to find matching data
            value = None
            for key, val in form_data.items():
                if key.lower() in field_identifier.lower() or field_identifier.lower() in key.lower():
                    value = val
                    break
            
            if value:
                success = await self.fill_field(field, value)
                if success:
                    filled_count += 1
        
        print(f"\n✅ Filled {filled_count}/{len(fields)} fields")
        
        # Take screenshot after filling
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"data/screenshots/form_filled_{timestamp}.png"
        await self.page.screenshot(path=screenshot_path, full_page=True)
        await self.log_action("screenshot", {"path": screenshot_path})
        
        return filled_count > 0
        
    async def find_and_click_submit(self) -> bool:
        """Find and click the submit button."""
        print("\n🔍 Looking for submit button...")
        
        submit_selectors = [
            'input[type="submit"]',
            'button[type="submit"]',
            'button:has-text("Submit")',
            'button:has-text("Apply")',
            'button:has-text("Next")',
            'input[value*="Submit"]',
            'a:has-text("Submit")',
        ]
        
        for selector in submit_selectors:
            try:
                submit_btn = await self.page.query_selector(selector)
                if submit_btn:
                    # Check if visible
                    is_visible = await submit_btn.is_visible()
                    if is_visible:
                        await submit_btn.scroll_into_view_if_needed()
                        await self.human_delay(1000, 2000)
                        
                        # Take screenshot before submit
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        screenshot_path = f"data/screenshots/before_submit_{timestamp}.png"
                        await self.page.screenshot(path=screenshot_path, full_page=True)
                        
                        print(f"✅ Found submit button: {selector}")
                        print("⚠️  NOT clicking submit (demo mode)")
                        # Uncomment to actually submit:
                        # await submit_btn.click()
                        # await self.human_delay(3000, 5000)
                        
                        await self.log_action("submit", {
                            "selector": selector,
                            "message": "Submit button found (not clicked in demo mode)"
                        })
                        
                        return True
            except:
                continue
        
        print("⚠️  No submit button found")
        return False
        
    async def save_action_log(self):
        """Save all actions to a file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = f"data/logs/form_filling_{timestamp}.json"
        
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


async def demo_mppsc_application():
    """
    Demo: Autonomous form filling for MPPSC application
    """
    print("=" * 60)
    print("🤖 MPOnline Advanced Form Filling Agent - DEMO")
    print("=" * 60)
    
    # Sample form data
    sample_data = {
        "name": "Rajesh Kumar",
        "fname": "Ram Kumar",  # Father's name
        "email": "rajesh.kumar@example.com",
        "mobile": "9876543210",
        "dob": "01/01/1995",
        "gender": "Male",
        "category": "General",
        "address": "123 Main Street, Bhopal, MP",
        "pincode": "462001",
        "qualification": "Graduate",
    }
    
    agent = AdvancedFormFillingAgent(headless=False)
    
    try:
        await agent.start_browser()
        
        # Navigate to MPOnline homepage first
        if await agent.navigate_to_service("https://www.mponline.gov.in"):
            
            # Option 1: Detect and analyze forms on current page
            print("\n📋 Analyzing current page forms...")
            fields = await agent.detect_form_fields()
            
            # If you want to navigate to a specific service:
            # await agent.navigate_to_service("https://esb.mponline.gov.in")
            # await agent.auto_fill_form(sample_data)
            # await agent.find_and_click_submit()
            
            # Save log
            await agent.save_action_log()
            
            print("\n" + "=" * 60)
            print("✅ Demo completed!")
            print("=" * 60)
            print("\n💡 Next steps:")
            print("1. Navigate to a specific service URL")
            print("2. Call auto_fill_form() with your data")
            print("3. Call find_and_click_submit() to submit")
            
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        
    finally:
        await agent.close()


if __name__ == "__main__":
    asyncio.run(demo_mppsc_application())
