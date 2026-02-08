"""
Automated Browser Agent - Fully Automated with Smart Decision Making
Only asks for help when genuinely stuck
"""

import asyncio
from playwright.async_api import async_playwright, TimeoutError
from datetime import datetime
import json
import os
import random

class AutomatedBrowserAgent:
    def __init__(self):
        self.page = None
        self.browser = None
        self.context = None
        self.screenshots_dir = "data/screenshots/automated"
        self.logs_dir = "data/logs/automated"
        self.action_log = []
        
        os.makedirs(self.screenshots_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
    
    def log(self, message, level="INFO"):
        """Log actions"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = {
            "time": timestamp,
            "level": level,
            "message": message
        }
        self.action_log.append(entry)
        
        emoji_map = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "QUESTION": "❓",
            "THINKING": "🤔",
            "ACTION": "🔄",
            "ERROR": "❌",
            "STUCK": "🆘"
        }
        
        emoji = emoji_map.get(level, "ℹ️")
        print(f"{emoji} [{timestamp}] {message}")
    
    async def delay(self, min_sec=0.5, max_sec=2):
        """Human-like delay"""
        await asyncio.sleep(random.uniform(min_sec, max_sec))
    
    async def screenshot(self, name):
        """Take screenshot"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"{self.screenshots_dir}/{name}_{timestamp}.png"
        await self.page.screenshot(path=path, full_page=True)
        self.log(f"Screenshot: {name}", "INFO")
        return path
    
    def ask_when_stuck(self, question, context=""):
        """Only called when truly stuck"""
        self.log(f"STUCK: {question}", "STUCK")
        if context:
            print(f"\n📋 Context: {context}")
        
        print("\n" + "="*90)
        print("🆘 I'M STUCK - NEED YOUR HELP")
        print("="*90)
        print(f"\n{question}\n")
        
        response = input("👤 Your guidance: ").strip()
        self.log(f"User helped: {response}", "SUCCESS")
        return response
    
    async def auto_search(self, query):
        """Automatically search on Google"""
        self.log(f"Auto-searching: {query}", "THINKING")
        
        await self.page.goto("https://www.google.com", wait_until="networkidle")
        await self.delay(1, 2)
        
        search_box = await self.page.wait_for_selector('textarea[name="q"], input[name="q"]')
        await search_box.click()
        await self.delay(0.3, 0.5)
        
        # Type naturally
        for char in query:
            await search_box.type(char)
            await asyncio.sleep(random.uniform(0.05, 0.12))
        
        await self.delay(0.5, 1)
        await search_box.press("Enter")
        await self.page.wait_for_load_state("networkidle")
        await self.delay(2, 3)
        
        await self.screenshot("search_results")
        self.log("Search completed", "SUCCESS")
    
    async def auto_select_result(self, expected_domain):
        """Automatically select best search result"""
        self.log(f"Auto-selecting result with: {expected_domain}", "THINKING")
        
        results = await self.page.evaluate("""
            () => {
                const links = Array.from(document.querySelectorAll('a'));
                return links
                    .filter(a => a.href && !a.href.includes('google.com'))
                    .slice(0, 10)
                    .map(a => ({
                        text: a.textContent.trim(),
                        href: a.href
                    }));
            }
        """)
        
        if not results:
            guidance = self.ask_when_stuck(
                "No search results found. What should I do?",
                "Expected to find links but page appears empty"
            )
            if "http" in guidance:
                await self.page.goto(guidance, wait_until="networkidle")
                return True
            return False
        
        # Auto-select matching domain
        matching = [r for r in results if expected_domain.lower() in r['href'].lower()]
        
        if matching:
            target_url = matching[0]['href']
            self.log(f"Found matching: {target_url}", "SUCCESS")
        else:
            # Show results and ask
            print("\n🔍 Search Results:")
            for idx, r in enumerate(results[:5], 1):
                print(f"  {idx}. {r['text'][:80]}")
                print(f"     {r['href']}")
            
            choice = self.ask_when_stuck(
                f"Couldn't auto-find '{expected_domain}'. Which result? (1-5 or URL)",
                f"Looking for domain containing: {expected_domain}"
            )
            
            try:
                idx = int(choice) - 1
                target_url = results[idx]['href']
            except:
                target_url = choice
        
        self.log(f"Navigating to: {target_url}", "ACTION")
        await self.page.goto(target_url, wait_until="networkidle")
        await self.delay(2, 3)
        await self.screenshot("portal_home")
        return True
    
    async def auto_click(self, description, search_texts):
        """Automatically click element"""
        self.log(f"Auto-clicking: {description}", "THINKING")
        
        if isinstance(search_texts, str):
            search_texts = [search_texts]
        
        # Try JavaScript click with multiple text variations
        for text in search_texts:
            try:
                clicked = await self.page.evaluate("""
                    (searchText) => {
                        const elements = Array.from(document.querySelectorAll('a, button'));
                        const match = elements.find(el => 
                            el.textContent.trim().includes(searchText) ||
                            el.textContent.trim().toLowerCase().includes(searchText.toLowerCase())
                        );
                        
                        if (match) {
                            match.scrollIntoView({behavior: 'smooth', block: 'center'});
                            setTimeout(() => match.click(), 500);
                            return {success: true, text: match.textContent.trim()};
                        }
                        return {success: false};
                    }
                """, text)
                
                if clicked['success']:
                    self.log(f"Clicked: {clicked['text']}", "SUCCESS")
                    await self.delay(3, 4)
                    await self.screenshot(f"after_{description.replace(' ', '_')}")
                    return True
            except:
                continue
        
        # If not found, ask user
        await self.screenshot("element_not_found")
        
        guidance = self.ask_when_stuck(
            f"Cannot find '{description}' to click. What should I do?",
            f"Tried searching for: {', '.join(search_texts)}"
        )
        
        if "manual" in guidance.lower():
            self.log("Waiting for manual click...", "INFO")
            input("Press Enter after clicking manually...")
            await self.delay(2, 3)
            return True
        elif "skip" in guidance.lower():
            return False
        else:
            # Try with user's guidance
            return await self.auto_click(description, [guidance])
    
    async def auto_click_specific_exam_action(self):
        """Find State Service/Forest Service Preliminary Examination 2026 and click Action button"""
        self.log("Searching for State Service Preliminary Examination 2026...", "THINKING")
        
        clicked = await self.page.evaluate("""
            () => {
                // Search for the specific exam row
                const examVariations = [
                    'State Service Preliminary Examination 2026',
                    'State Forest Service Preliminary Examination 2026',
                    'राज्य सेवा प्रारंभिक परीक्षा 2026'
                ];
                
                const rows = Array.from(document.querySelectorAll('tr'));
                let targetRow = null;
                
                // Find row containing any of the exam variations
                for (const examText of examVariations) {
                    targetRow = rows.find(row => 
                        row.textContent.includes(examText)
                    );
                    if (targetRow) {
                        console.log('Found exam row:', examText);
                        break;
                    }
                }
                
                if (!targetRow) {
                    return {success: false, error: 'Exam row not found', exams: examVariations};
                }
                
                // Get all cells in the row
                const cells = Array.from(targetRow.querySelectorAll('td'));
                
                // Find the Action column cell (usually last cell with a link/button)
                let actionCell = null;
                
                // Try to find cell with "Click Here" or similar text
                actionCell = cells.find(cell => {
                    const text = cell.textContent.trim().toLowerCase();
                    return text.includes('click here') || 
                           text.includes('क्लिक') || 
                           cell.querySelector('a[href*="Application"], a[href*="Form"], input[type="button"]');
                });
                
                // If not found, try last cell
                if (!actionCell && cells.length > 0) {
                    actionCell = cells[cells.length - 1];
                }
                
                if (actionCell) {
                    // Find clickable element in action cell
                    const clickable = actionCell.querySelector('a, button, input[type="button"], input[type="submit"]');
                    if (clickable) {
                        const buttonText = clickable.textContent.trim() || clickable.value || 'Action Button';
                        clickable.scrollIntoView({behavior: 'smooth', block: 'center'});
                        setTimeout(() => clickable.click(), 500);
                        return {
                            success: true,
                            buttonText: buttonText,
                            examFound: targetRow.textContent.substring(0, 100)
                        };
                    }
                }
                
                return {success: false, error: 'Action button not found in row'};
            }
        """)
        
        if clicked['success']:
            self.log(f"Found exam: {clicked.get('examFound', 'N/A')[:50]}...", "SUCCESS")
            self.log(f"Clicked: {clicked['buttonText']}", "SUCCESS")
            await self.delay(3, 5)
            await self.screenshot("after_exam_action_click")
            return True
        else:
            error_msg = clicked.get('error', 'Unknown')
            if 'not found' in error_msg.lower():
                await self.screenshot("exam_not_found")
                
                guidance = self.ask_when_stuck(
                    "Cannot find 'State Service Preliminary Examination 2026' in the table",
                    f"Error: {error_msg}\nSearched for: {', '.join(clicked.get('exams', []))}"
                )
            else:
                guidance = self.ask_when_stuck(
                    "Found exam row but cannot click Action button",
                    f"Error: {error_msg}"
                )
            
            if "manual" in guidance.lower():
                input("Please click the Action 'Click Here' button manually, then press Enter...")
                await self.delay(2, 3)
                return True
            
            return False
    
    async def auto_fill_form(self):
        """Automatically detect and fill form"""
        self.log("Auto-detecting form...", "THINKING")
        
        form_fields = await self.page.evaluate("""
            () => {
                const inputs = Array.from(document.querySelectorAll('input:not([type="hidden"]), select, textarea'));
                const visible = inputs.filter(inp => {
                    const style = window.getComputedStyle(inp);
                    return style.display !== 'none' && inp.offsetParent !== null;
                });
                
                return visible.map(inp => ({
                    type: inp.type || inp.tagName.toLowerCase(),
                    name: inp.name,
                    id: inp.id,
                    placeholder: inp.placeholder,
                    required: inp.required,
                    label: inp.labels?.[0]?.textContent.trim() || ''
                }));
            }
        """)
        
        if not form_fields:
            self.log("No form detected", "INFO")
            return False
        
        self.log(f"Found {len(form_fields)} form fields", "SUCCESS")
        
        # Auto sample data
        sample_data = {
            "name": "राज कुमार शर्मा",
            "email": "test.mppsc@example.com",
            "mobile": "9876543210",
            "phone": "9876543210",
            "dob": "1995-08-15",
            "address": "123 Test Street, Indore, MP",
            "pincode": "452001",
            "pin": "452001",
            "city": "Indore",
            "state": "Madhya Pradesh"
        }
        
        filled = 0
        for field in form_fields:
            field_name = (field['label'] or field['name'] or field['id'] or '').lower()
            
            value = None
            for key, val in sample_data.items():
                if key in field_name:
                    value = val
                    break
            
            if value and field['id']:
                try:
                    await self.page.fill(f"#{field['id']}", str(value))
                    await self.delay(0.2, 0.5)
                    filled += 1
                    self.log(f"Filled: {field['label'] or field['id']}", "SUCCESS")
                except:
                    pass
        
        self.log(f"Auto-filled {filled}/{len(form_fields)} fields", "SUCCESS")
        await self.screenshot("form_filled")
        return True
    
    async def run_mppsc_flow(self):
        """Fully automated MPPSC form filling flow"""
        
        print("\n" + "="*90)
        print("🤖 AUTOMATED BROWSER AGENT - MPPSC Form Filling")
        print("="*90)
        print("\nℹ️  I'll work automatically and only ask when I'm stuck!\n")
        
        async with async_playwright() as p:
            self.browser = await p.chromium.launch(headless=False)
            self.context = await self.browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            self.page = await self.context.new_page()
            
            try:
                # Step 1: Navigate directly to MPOnline (skip Google search)
                self.log("Navigating to MPOnline Portal", "ACTION")
                await self.page.goto("https://mponline.gov.in/portal/", wait_until="networkidle")
                await self.delay(3, 4)
                await self.screenshot("mponline_home")
                self.log("MPOnline portal loaded", "SUCCESS")
                
                # Step 2: Click MPPSC
                if await self.auto_click("MPPSC", ["MPPSC", "एमपीपीएससी"]):
                    
                    # Step 3: Navigate to MPPSC Attestation page directly
                    self.log("Going to MPPSC Attestation page directly", "ACTION")
                    await self.page.goto(
                        "https://mponline.gov.in/Portal/Examinations/MPPSC/Attestation/Home/Home.aspx",
                        wait_until="networkidle"
                    )
                    await self.delay(3, 4)
                    await self.screenshot("mppsc_attestation")
                    self.log("MPPSC Attestation page loaded", "SUCCESS")
                    
                    # Step 4: Click Application Form action button for specific exam
                    if await self.auto_click_specific_exam_action():
                        
                        # Step 5: Check if we're on application form
                        await self.delay(3, 4)
                        
                        current_url = self.page.url
                        page_title = await self.page.title()
                        
                        self.log(f"Current URL: {current_url}", "INFO")
                        self.log(f"Page Title: {page_title}", "INFO")
                        
                        await self.screenshot("current_page_after_action")
                        
                        # Check if form page or "coming soon"
                        if "coming soon" in page_title.lower():
                            print("\n" + "="*90)
                            print("ℹ️  NOTICE: Application Form Shows 'Coming Soon'")
                            print("="*90)
                            print(f"\nPage Title: {page_title}")
                            print(f"URL: {current_url}")
                            print("\nThe application period may not be active yet.")
                            print("Browser will stay open for you to verify.")
                            print("\nPress Enter to close...")
                            input()
                            
                        elif "application" in current_url.lower() or "form" in current_url.lower() or "candidate" in current_url.lower():
                            self.log("Reached application form!", "SUCCESS")
                            
                            # Try to fill form
                            form_filled = await self.auto_fill_form()
                            
                            if form_filled:
                                print("\n" + "="*90)
                                print("✅ FORM FILLING COMPLETED")
                                print("="*90)
                                print("\nForm filled automatically. Review in browser.")
                                print("You may need to:")
                                print("  - Upload documents")
                                print("  - Complete CAPTCHA")
                                print("  - Submit the form")
                                print("\nPress Enter when done reviewing...")
                                input()
                            else:
                                self.log("No form fields detected on this page", "INFO")
                                print("\nBrowser staying open for review. Press Enter to close...")
                                input()
                        else:
                            self.log("Unexpected page after clicking action", "INFO")
                            guidance = self.ask_when_stuck(
                                "Clicked action button but not sure what page this is. What should I do?",
                                f"URL: {current_url}\nTitle: {page_title}"
                            )
                            
                            if "fill" in guidance.lower():
                                await self.auto_fill_form()
                                input("\nPress Enter to close...")
                
            except Exception as e:
                self.log(f"Error: {str(e)}", "ERROR")
                import traceback
                traceback.print_exc()
                
                await self.screenshot("error_state")
                
                print("\n" + "="*90)
                print("❌ ERROR OCCURRED")
                print("="*90)
                print(f"\n{str(e)}\n")
                print("Browser will stay open for debugging.")
                input("Press Enter to close...")
                
            finally:
                # Save log
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                log_path = f"{self.logs_dir}/automated_run_{timestamp}.json"
                with open(log_path, 'w', encoding='utf-8') as f:
                    json.dump(self.action_log, f, indent=2, ensure_ascii=False)
                
                print(f"\n📝 Log saved: {log_path}")
                print(f"📁 Screenshots: {self.screenshots_dir}/")
                
                await self.browser.close()
                print("\n✅ Session complete!")

if __name__ == "__main__":
    agent = AutomatedBrowserAgent()
    asyncio.run(agent.run_mppsc_flow())
