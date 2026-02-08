"""
Interactive Browser Agent - Human-like Form Filling Assistant
Takes user queries, searches, navigates, and asks for help when stuck
"""

import asyncio
from playwright.async_api import async_playwright, TimeoutError
from datetime import datetime
import json
import os
import random

class InteractiveBrowserAgent:
    def __init__(self):
        self.page = None
        self.browser = None
        self.context = None
        self.screenshots_dir = "data/screenshots/interactive"
        self.logs_dir = "data/logs/interactive"
        self.conversation_history = []
        
        os.makedirs(self.screenshots_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
    
    def log_message(self, message, level="INFO"):
        """Log conversation and actions"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = {
            "time": timestamp,
            "level": level,
            "message": message
        }
        self.conversation_history.append(entry)
        
        emoji_map = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "QUESTION": "❓",
            "THINKING": "🤔",
            "ACTION": "🔄",
            "ERROR": "❌",
            "SPEAK": "💬"
        }
        
        emoji = emoji_map.get(level, "ℹ️")
        print(f"\n{emoji} [{timestamp}] {message}")
    
    async def human_delay(self, min_sec=0.5, max_sec=2):
        """Add human-like random delays"""
        delay = random.uniform(min_sec, max_sec)
        await asyncio.sleep(delay)
    
    async def take_screenshot(self, name):
        """Take screenshot for evidence"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"{self.screenshots_dir}/{name}_{timestamp}.png"
        await self.page.screenshot(path=path, full_page=True)
        self.log_message(f"📸 Screenshot saved: {name}", "INFO")
        return path
    
    def ask_user(self, question, options=None):
        """Ask user for input"""
        self.log_message(question, "QUESTION")
        
        if options:
            print("\nOptions:")
            for idx, option in enumerate(options, 1):
                print(f"  {idx}. {option}")
            print()
        
        response = input("👤 Your answer: ").strip()
        self.log_message(f"User answered: {response}", "INFO")
        return response
    
    async def search_on_google(self, query):
        """Search on Google like a human"""
        self.log_message(f"Searching Google for: {query}", "THINKING")
        
        await self.page.goto("https://www.google.com", wait_until="networkidle")
        await self.human_delay(1, 2)
        
        # Type search query with human-like speed
        search_box = await self.page.wait_for_selector('textarea[name="q"], input[name="q"]')
        await search_box.click()
        await self.human_delay(0.3, 0.8)
        
        # Type character by character
        for char in query:
            await search_box.type(char)
            await asyncio.sleep(random.uniform(0.05, 0.15))
        
        await self.human_delay(0.5, 1)
        await search_box.press("Enter")
        
        await self.page.wait_for_load_state("networkidle")
        await self.human_delay(2, 3)
        
        await self.take_screenshot("google_search_results")
        self.log_message("✓ Google search completed", "SUCCESS")
    
    async def click_search_result(self, expected_domain=None):
        """Click on the most relevant search result"""
        self.log_message("Looking for the right link in search results...", "THINKING")
        
        # Get search results
        results = await self.page.evaluate("""
            () => {
                const links = Array.from(document.querySelectorAll('a'));
                return links
                    .filter(a => a.href && !a.href.includes('google.com'))
                    .slice(0, 10)
                    .map(a => ({
                        text: a.textContent.trim().substring(0, 100),
                        href: a.href
                    }));
            }
        """)
        
        if results:
            print("\n🔍 Found these search results:")
            for idx, result in enumerate(results[:5], 1):
                print(f"  {idx}. {result['text']}")
                print(f"     → {result['href']}")
            
            if expected_domain:
                # Try to find result with expected domain
                matching = [r for r in results if expected_domain.lower() in r['href'].lower()]
                if matching:
                    self.log_message(f"Found matching domain: {expected_domain}", "SUCCESS")
                    target_url = matching[0]['href']
                else:
                    choice = self.ask_user(f"Which result looks correct? (1-{len(results[:5])} or enter URL)")
                    try:
                        idx = int(choice) - 1
                        target_url = results[idx]['href']
                    except:
                        target_url = choice
            else:
                choice = self.ask_user(f"Which result should I click? (1-{len(results[:5])} or enter URL)")
                try:
                    idx = int(choice) - 1
                    target_url = results[idx]['href']
                except:
                    target_url = choice
            
            self.log_message(f"Navigating to: {target_url}", "ACTION")
            await self.page.goto(target_url, wait_until="networkidle")
            await self.human_delay(2, 3)
            await self.take_screenshot("clicked_search_result")
            return True
        
        return False
    
    async def find_and_click_element(self, description, selectors, ask_if_not_found=True):
        """Find and click an element, ask user if not found"""
        self.log_message(f"Looking for: {description}", "THINKING")
        
        if isinstance(selectors, str):
            selectors = [selectors]
        
        for selector in selectors:
            try:
                element = await self.page.wait_for_selector(selector, timeout=5000, state='visible')
                if element:
                    # Scroll into view
                    await element.scroll_into_view_if_needed()
                    await self.human_delay(0.5, 1)
                    
                    # Highlight before clicking (human-like)
                    await self.page.evaluate("""
                        (selector) => {
                            const el = document.querySelector(selector);
                            if (el) {
                                el.style.outline = '3px solid red';
                                setTimeout(() => el.style.outline = '', 1000);
                            }
                        }
                    """, selector)
                    
                    await self.human_delay(0.5, 1)
                    text = await element.text_content()
                    self.log_message(f"Found: {text.strip()[:50]}", "SUCCESS")
                    
                    await element.click()
                    await self.human_delay(2, 3)
                    self.log_message(f"✓ Clicked: {description}", "SUCCESS")
                    return True
            except TimeoutError:
                continue
        
        # Not found - ask user
        if ask_if_not_found:
            await self.take_screenshot("element_not_found")
            
            response = self.ask_user(
                f"❌ I couldn't find '{description}' automatically.\n" +
                "What should I do?",
                [
                    "I'll click it manually - wait",
                    "Try a different search",
                    "It's already visible - describe it",
                    "Skip this step"
                ]
            )
            
            if "manual" in response.lower() or response == "1":
                self.log_message("Waiting for manual click...", "INFO")
                input("Press Enter after you've clicked it manually...")
                await self.human_delay(1, 2)
                return True
            elif "visible" in response.lower() or response == "3":
                guidance = self.ask_user("Please describe what I should look for (text, color, position etc.):")
                self.log_message(f"User guidance: {guidance}", "INFO")
                # Try to use the guidance
                return await self.try_with_guidance(guidance)
        
        return False
    
    async def try_with_guidance(self, guidance):
        """Try to find element based on user guidance"""
        # Try to click based on text in guidance
        try:
            clicked = await self.page.evaluate(f"""
                (guidance) => {{
                    const allElements = Array.from(document.querySelectorAll('a, button, input[type="button"], input[type="submit"]'));
                    const matching = allElements.find(el => 
                        el.textContent.toLowerCase().includes(guidance.toLowerCase())
                    );
                    if (matching) {{
                        matching.click();
                        return true;
                    }}
                    return false;
                }}
            """, guidance.lower())
            
            if clicked:
                self.log_message("✓ Found and clicked based on your guidance!", "SUCCESS")
                await self.human_delay(2, 3)
                return True
        except:
            pass
        
        return False
    
    async def fill_form_interactive(self, form_data=None):
        """Fill form with user interaction"""
        self.log_message("Analyzing form on current page...", "THINKING")
        
        form_fields = await self.page.evaluate("""
            () => {
                const inputs = Array.from(document.querySelectorAll('input:not([type="hidden"]), select, textarea'));
                const visible = inputs.filter(inp => {
                    const style = window.getComputedStyle(inp);
                    return style.display !== 'none' && style.visibility !== 'hidden' && inp.offsetParent !== null;
                });
                
                return visible.map(inp => ({
                    type: inp.type || inp.tagName.toLowerCase(),
                    name: inp.name,
                    id: inp.id,
                    placeholder: inp.placeholder,
                    required: inp.required,
                    label: inp.labels && inp.labels[0] ? inp.labels[0].textContent.trim() : ''
                }));
            }
        """)
        
        if not form_fields:
            self.log_message("No form fields found on this page", "INFO")
            return
        
        self.log_message(f"Found {len(form_fields)} form fields", "SUCCESS")
        print("\n📝 Form Fields:")
        for idx, field in enumerate(form_fields, 1):
            req = " *REQUIRED*" if field['required'] else ""
            label = field['label'] or field['placeholder'] or field['name'] or field['id']
            print(f"  {idx}. [{field['type']}] {label}{req}")
        
        response = self.ask_user(
            "\nHow would you like to proceed?",
            [
                "Fill with sample data automatically",
                "I'll fill manually",
                "Ask me for each field value",
                "Skip form filling for now"
            ]
        )
        
        if "sample" in response.lower() or response == "1":
            await self.fill_with_sample_data(form_fields)
        elif "manual" in response.lower() or response == "2":
            self.log_message("Please fill the form manually", "INFO")
            input("Press Enter when done filling...")
        elif "ask" in response.lower() or response == "3":
            await self.fill_with_user_input(form_fields)
    
    async def fill_with_sample_data(self, fields):
        """Fill form with sample data"""
        sample_data = {
            "name": "राज कुमार शर्मा",
            "email": "test.user@example.com",
            "mobile": "9876543210",
            "phone": "9876543210",
            "dob": "15/08/1995",
            "address": "123, Test Address, Indore",
            "pincode": "452001",
            "city": "Indore",
            "state": "Madhya Pradesh"
        }
        
        filled_count = 0
        for field in fields:
            field_name = (field['label'] or field['name'] or field['id'] or '').lower()
            
            # Match field to sample data
            value = None
            for key, val in sample_data.items():
                if key in field_name:
                    value = val
                    break
            
            if value and field['id']:
                try:
                    await self.page.fill(f"#{field['id']}", value)
                    await self.human_delay(0.3, 0.8)
                    filled_count += 1
                    self.log_message(f"✓ Filled: {field['label'] or field['id']}", "SUCCESS")
                except:
                    pass
        
        self.log_message(f"Filled {filled_count}/{len(fields)} fields", "SUCCESS")
    
    async def fill_with_user_input(self, fields):
        """Ask user for each field value"""
        for field in fields[:10]:  # Limit to first 10
            label = field['label'] or field['placeholder'] or field['name'] or field['id']
            value = self.ask_user(f"Value for '{label}':")
            
            if value and field['id']:
                try:
                    await self.page.fill(f"#{field['id']}", value)
                    await self.human_delay(0.3, 0.8)
                except:
                    pass
    
    async def run_interactive_session(self):
        """Main interactive session"""
        print("\n" + "="*90)
        print("🤖 INTERACTIVE BROWSER AGENT - Your Human-like Form Filling Assistant")
        print("="*90)
        
        async with async_playwright() as p:
            self.browser = await p.chromium.launch(headless=False)
            self.context = await self.browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            self.page = await self.context.new_page()
            
            try:
                self.log_message("Hello! I'm your interactive browser agent.", "SPEAK")
                self.log_message("I'll help you navigate and fill forms like a real human.", "SPEAK")
                
                # Get initial query
                query = self.ask_user("What portal or website would you like me to visit? (e.g., 'MPOnline')")
                
                if query:
                    # Search on Google
                    await self.search_on_google(query)
                    
                    # Click search result
                    expected_domain = "mponline" if "mponline" in query.lower() else None
                    await self.click_search_result(expected_domain)
                    
                    # Main interaction loop
                    while True:
                        await self.take_screenshot("current_state")
                        
                        action = self.ask_user(
                            "\nWhat would you like me to do next?",
                            [
                                "Click on something (I'll search for it)",
                                "Fill a form on this page",
                                "Take screenshot and describe page",
                                "Go to a specific URL",
                                "I'm done - close browser"
                            ]
                        )
                        
                        if "click" in action.lower() or action == "1":
                            target = self.ask_user("What should I click? (describe it)")
                            
                            # Create selector variations
                            selectors = [
                                f'text="{target}"',
                                f'a:has-text("{target}")',
                                f'button:has-text("{target}")',
                                f'//*[contains(text(), "{target}")]'
                            ]
                            
                            clicked = await self.find_and_click_element(target, selectors)
                            
                            if clicked:
                                await self.take_screenshot("after_click")
                        
                        elif "form" in action.lower() or action == "2":
                            await self.fill_form_interactive()
                        
                        elif "screenshot" in action.lower() or action == "3":
                            await self.take_screenshot("user_requested")
                            
                            # Describe page
                            page_info = await self.page.evaluate("""
                                () => {
                                    return {
                                        title: document.title,
                                        url: window.location.href,
                                        headings: Array.from(document.querySelectorAll('h1, h2, h3')).map(h => h.textContent.trim()).slice(0, 5),
                                        buttons: Array.from(document.querySelectorAll('button, a.btn')).map(b => b.textContent.trim()).slice(0, 10),
                                        inputs: document.querySelectorAll('input, select, textarea').length
                                    };
                                }
                            """)
                            
                            print("\n📄 Page Information:")
                            print(f"  Title: {page_info['title']}")
                            print(f"  URL: {page_info['url']}")
                            print(f"  Headings: {', '.join(page_info['headings'])}")
                            print(f"  Form Inputs: {page_info['inputs']}")
                            print(f"  Buttons: {', '.join(page_info['buttons'][:5])}")
                        
                        elif "url" in action.lower() or action == "4":
                            url = self.ask_user("Enter the URL:")
                            self.log_message(f"Navigating to {url}", "ACTION")
                            await self.page.goto(url, wait_until="networkidle")
                            await self.human_delay(2, 3)
                        
                        elif "done" in action.lower() or action == "5":
                            self.log_message("Closing browser...", "INFO")
                            break
                        
                        else:
                            self.log_message("I didn't understand. Let me show you the options again.", "SPEAK")
                
            except Exception as e:
                self.log_message(f"Error: {str(e)}", "ERROR")
                import traceback
                traceback.print_exc()
            finally:
                # Save conversation log
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                log_path = f"{self.logs_dir}/conversation_{timestamp}.json"
                with open(log_path, 'w', encoding='utf-8') as f:
                    json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
                
                print(f"\n📝 Conversation log saved: {log_path}")
                print(f"📁 Screenshots saved in: {self.screenshots_dir}")
                
                await self.browser.close()
                print("\n✅ Session ended. Thank you!")

if __name__ == "__main__":
    agent = InteractiveBrowserAgent()
    asyncio.run(agent.run_interactive_session())
