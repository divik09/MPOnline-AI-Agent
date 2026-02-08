"""
Enhanced MPPSC State Service Preliminary Examination 2026 Form Filler
Shows CONTINUOUS, PERSISTENT effort to navigate and fill the form
"""

import asyncio
from playwright.async_api import async_playwright, TimeoutError
from datetime import datetime
import json
import os

class ContinuousMPPSCFiller:
    def __init__(self):
        self.page = None
        self.browser = None
        self.context = None
        self.screenshots_dir = "data/screenshots"
        self.logs_dir = "data/logs"
        self.attempts_log = []
        
        # Ensure directories exist
        os.makedirs(self.screenshots_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
    
    def log_attempt(self, action, status, details=""):
        """Log each attempt for transparency"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = {
            "time": timestamp,
            "action": action,
            "status": status,
            "details": details
        }
        self.attempts_log.append(log_entry)
        
        symbol = "✅" if status == "success" else "🔄" if status == "retry" else "⚠️"
        print(f"{symbol} [{timestamp}] {action}: {status}")
        if details:
            print(f"   └─ {details}")
    
    async def take_screenshot(self, name):
        """Take screenshot and return path"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"{self.screenshots_dir}/{name}_{timestamp}.png"
        await self.page.screenshot(path=path, full_page=True)
        self.log_attempt(f"Screenshot: {name}", "success", f"Saved to {path}")
        return path
    
    async def click_with_retry(self, selectors, description, max_attempts=5):
        """Try multiple selectors with retries"""
        print(f"\n{'='*80}")
        print(f"🎯 TRYING TO: {description}")
        print(f"{'='*80}")
        
        if isinstance(selectors, str):
            selectors = [selectors]
        
        for attempt in range(max_attempts):
            self.log_attempt(f"Attempt {attempt + 1}/{max_attempts}", "retry", f"Trying to {description}")
            
            for idx, selector in enumerate(selectors):
                try:
                    self.log_attempt(f"Testing selector {idx + 1}/{len(selectors)}", "retry", selector)
                    
                    # Wait for selector
                    element = await self.page.wait_for_selector(selector, timeout=5000, state='visible')
                    
                    if element:
                        # Scroll into view
                        await element.scroll_into_view_if_needed()
                        await asyncio.sleep(1)
                        
                        # Get text content for logging
                        text = await element.text_content()
                        self.log_attempt(f"Found element", "success", f"Text: {text.strip()[:50]}")
                        
                        # Click
                        await element.click()
                        await asyncio.sleep(3)
                        
                        self.log_attempt(f"{description}", "success", f"Clicked using selector: {selector}")
                        return True
                        
                except TimeoutError:
                    self.log_attempt(f"Selector timeout", "retry", f"Selector not found: {selector}")
                except Exception as e:
                    self.log_attempt(f"Selector error", "retry", f"{selector}: {str(e)}")
            
            # Wait before retry
            if attempt < max_attempts - 1:
                self.log_attempt("Waiting before retry", "retry", "Pausing 2 seconds")
                await asyncio.sleep(2)
        
        self.log_attempt(f"{description}", "failed", "All attempts exhausted")
        return False
    
    async def fill_form_field(self, field_name, value, selectors, field_type="text"):
        """Fill a form field with multiple selector attempts"""
        print(f"\n📝 Filling field: {field_name}")
        
        if isinstance(selectors, str):
            selectors = [selectors]
        
        for selector in selectors:
            try:
                element = await self.page.wait_for_selector(selector, timeout=3000, state='visible')
                
                if element:
                    if field_type == "select":
                        await element.select_option(value)
                    elif field_type == "radio":
                        await element.click()
                    else:
                        await element.fill(value)
                    
                    self.log_attempt(f"Fill: {field_name}", "success", f"Value: {value}")
                    await asyncio.sleep(0.5)
                    return True
                    
            except Exception as e:
                self.log_attempt(f"Fill attempt: {field_name}", "retry", f"{selector}: {str(e)}")
        
        self.log_attempt(f"Fill: {field_name}", "failed", "Field not found")
        return False
    
    async def navigate_to_form(self):
        """Navigate to the MPPSC form with continuous effort"""
        
        # STEP 1: Open portal
        print(f"\n{'#'*80}")
        print("STEP 1: OPENING MPONLINE PORTAL")
        print(f"{'#'*80}")
        
        await self.page.goto("https://mponline.gov.in/portal/", wait_until="networkidle")
        await asyncio.sleep(3)
        await self.take_screenshot("01_portal_homepage")
        self.log_attempt("Portal navigation", "success", "https://mponline.gov.in/portal/")
        
        # STEP 2: Click MPPSC
        print(f"\n{'#'*80}")
        print("STEP 2: CLICKING ON MPPSC")
        print(f"{'#'*80}")
        
        mppsc_selectors = [
            'a:has-text("MPPSC")',
            'a:has-text("एमपीपीएससी")',
            'a[href*="mppsc"]',
            'div:has-text("MPPSC")',
            'button:has-text("MPPSC")',
            '//a[contains(text(), "MPPSC")]',
            '//a[contains(text(), "एमपीपीएससी")]',
        ]
        
        if await self.click_with_retry(mppsc_selectors, "Click MPPSC", max_attempts=3):
            await asyncio.sleep(3)
            await self.take_screenshot("02_after_mppsc_click")
        else:
            # Try to find any MPPSC related link by inspecting page
            self.log_attempt("Alternative search", "retry", "Looking for MPPSC in page content")
            content = await self.page.content()
            if "MPPSC" in content or "एमपीपीएससी" in content:
                self.log_attempt("MPPSC found in content", "success", "Attempting JavaScript click")
                try:
                    await self.page.evaluate("""
                        () => {
                            const links = Array.from(document.querySelectorAll('a'));
                            const mppscLink = links.find(a => 
                                a.textContent.includes('MPPSC') || 
                                a.textContent.includes('एमपीपीएससी')
                            );
                            if (mppscLink) {
                                mppscLink.click();
                                return true;
                            }
                            return false;
                        }
                    """)
                    await asyncio.sleep(3)
                    await self.take_screenshot("02_after_js_mppsc_click")
                except Exception as e:
                    self.log_attempt("JavaScript click", "failed", str(e))
        
        # STEP 3: Find exam
        print(f"\n{'#'*80}")
        print("STEP 3: FINDING STATE SERVICE PRELIMINARY EXAM 2026")
        print(f"{'#'*80}")
        
        exam_selectors = [
            'a:has-text("State Service Preliminary Examination 2026")',
            'a:has-text("राज्य सेवा प्रारम्भिक परीक्षा 2026")',
            'a:has-text("State Service")',
            'text="State Service Preliminary Examination 2026"',
            '//a[contains(text(), "State Service")]',
            '//a[contains(text(), "राज्य सेवा")]',
            'td:has-text("State Service") a',
            'tr:has-text("State Service") a',
        ]
        
        exam_clicked = await self.click_with_retry(exam_selectors, "Click exam", max_attempts=3)
        
        if not exam_clicked:
            # Try clicking any element with "State Service" text
            self.log_attempt("Alternative exam search", "retry", "Searching page for exam text")
            try:
                # Click on any row/div containing the exam name
                await self.page.click('text="2026"')
                await asyncio.sleep(2)
                await self.take_screenshot("03_after_year_click")
            except:
                pass
        
        await self.take_screenshot("03_exam_page")
        
        # STEP 4: Find and click application link
        print(f"\n{'#'*80}")
        print("STEP 4: FINDING APPLICATION FORM LINK")
        print(f"{'#'*80}")
        
        # First, try to expand any details if needed
        expand_selectors = [
            'a:has-text("Details")',
            'button:has-text("View More")',
            'a:has-text("विवरण")',
            '.accordion-button',
            '.expand-button',
        ]
        
        for selector in expand_selectors:
            try:
                element = await self.page.query_selector(selector)
                if element:
                    await element.click()
                    await asyncio.sleep(2)
                    self.log_attempt("Expanded details", "success", selector)
                    break
            except:
                pass
        
        # Now look for application link
        app_selectors = [
            'a:has-text("Fill Application")',
            'a:has-text("Apply Online")',
            'a:has-text("आवेदन करें")',
            'a:has-text("आवेदन")',
            'a:has-text("फॉर्म भरें")',
            'a:has-text("Application Form")',
            'a:has-text("Registration")',
            'button:has-text("Apply")',
            'a[href*="apply"]',
            'a[href*="application"]',
            'a[href*="form"]',
            '//a[contains(text(), "Application")]',
            '//a[contains(text(), "आवेदन")]',
        ]
        
        if await self.click_with_retry(app_selectors, "Click application link", max_attempts=5):
            await asyncio.sleep(5)
            await self.take_screenshot("04_application_form")
            return True
        
        # Last resort: Find all links and try those with promising text
        self.log_attempt("Last resort search", "retry", "Examining all links on page")
        try:
            links = await self.page.query_selector_all('a')
            for link in links:
                text = await link.text_content()
                href = await link.get_attribute('href')
                
                if text and any(keyword in text.lower() for keyword in ['apply', 'application', 'form', 'आवेदन', 'फॉर्म']):
                    self.log_attempt("Promising link found", "retry", f"Text: {text}, Href: {href}")
                    try:
                        await link.click()
                        await asyncio.sleep(5)
                        await self.take_screenshot("04_clicked_promising_link")
                        return True
                    except:
                        pass
        except Exception as e:
            self.log_attempt("Link examination", "failed", str(e))
        
        await self.take_screenshot("04_stuck_at_exam_page")
        return False
    
    async def fill_application_form(self):
        """Fill the application form with sample data"""
        print(f"\n{'#'*80}")
        print("STEP 5: FILLING APPLICATION FORM")
        print(f"{'#'*80}")
        
        # Wait for form to load
        await asyncio.sleep(3)
        await self.take_screenshot("05_form_loaded")
        
        # Sample form data
        form_data = {
            "Name": ("राज कुमार शर्मा", ['input[name*="name"]', '#name', 'input[placeholder*="Name"]']),
            "Father Name": ("विजय शर्मा", ['input[name*="father"]', 'input[placeholder*="Father"]']),
            "Mother Name": ("सुनीता शर्मा", ['input[name*="mother"]', 'input[placeholder*="Mother"]']),
            "Email": ("raj.sharma.test@example.com", ['input[type="email"]', 'input[name*="email"]']),
            "Mobile": ("9876543210", ['input[type="tel"]', 'input[name*="mobile"]', 'input[name*="phone"]']),
            "DOB": ("15/08/1995", ['input[type="date"]', 'input[name*="dob"]', 'input[name*="birth"]']),
            "Address": ("123, नई सड़क, इंदौर", ['textarea[name*="address"]', 'textarea', 'input[name*="address"]']),
            "Pincode": ("452001", ['input[name*="pin"]', 'input[name*="zip"]']),
        }
        
        filled_count = 0
        for field_name, (value, selectors) in form_data.items():
            if await self.fill_form_field(field_name, value, selectors):
                filled_count += 1
        
        self.log_attempt("Form filling summary", "success", f"Filled {filled_count}/{len(form_data)} fields")
        
        await self.take_screenshot("05_form_filled")
        
        # Look for next/continue/submit button
        next_selectors = [
            'button:has-text("Next")',
            'button:has-text("Continue")',
            'button:has-text("Submit")',
            'button:has-text("आगे")',
            'button:has-text("जमा करें")',
            'input[type="submit"]',
            'button[type="submit"]',
        ]
        
        await self.click_with_retry(next_selectors, "Click Next/Continue", max_attempts=3)
        await asyncio.sleep(3)
        await self.take_screenshot("06_after_continue")
    
    async def run(self):
        """Main execution"""
        print("\n" + "="*80)
        print("🚀 STARTING CONTINUOUS MPPSC FORM FILLING PROCESS")
        print("="*80)
        
        async with async_playwright() as p:
            # Launch browser
            self.browser = await p.chromium.launch(headless=False)
            self.context = await self.browser.new_context(viewport={"width": 1920, "height": 1080})
            self.page = await self.context.new_page()
            
            self.log_attempt("Browser initialization", "success", "Chromium launched")
            
            try:
                # Navigate to form
                form_reached = await self.navigate_to_form()
                
                if form_reached:
                    # Fill form
                    await self.fill_application_form()
                    
                    # Keep browser open for manual verification
                    self.log_attempt("Process complete", "success", "Form filled - browser staying open for review")
                    print("\n" + "="*80)
                    print("✅ PROCESS COMPLETE - REVIEW THE BROWSER")
                    print("="*80)
                    input("Press Enter to close browser...")
                else:
                    self.log_attempt("Navigation incomplete", "failed", "Could not reach application form")
                    print("\n" + "="*80)
                    print("⚠️  COULD NOT REACH APPLICATION FORM")
                    print("="*80)
                    await self.take_screenshot("final_state")
                    input("Press Enter to close browser...")
                
            except Exception as e:
                self.log_attempt("Fatal error", "failed", str(e))
                await self.take_screenshot("error_state")
            finally:
                # Save attempts log
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                log_path = f"{self.logs_dir}/continuous_attempts_{timestamp}.json"
                with open(log_path, 'w', encoding='utf-8') as f:
                    json.dump(self.attempts_log, f, indent=2, ensure_ascii=False)
                
                print(f"\n📝 Attempts log saved to: {log_path}")
                
                await self.browser.close()

if __name__ == "__main__":
    filler = ContinuousMPPSCFiller()
    asyncio.run(filler.run())
