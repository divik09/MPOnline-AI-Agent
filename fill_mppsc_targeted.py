"""
TARGETED MPPSC State Service Preliminary Examination 2026 Form Filler
Specifically validates we're on the correct exam before proceeding
"""

import asyncio
from playwright.async_api import async_playwright, TimeoutError
from datetime import datetime
import json
import os

class TargetedMPPSCFiller:
    def __init__(self):
        self.page = None
        self.browser = None
        self.context = None
        self.screenshots_dir = "data/screenshots"
        self.logs_dir = "data/logs"
        self.log_entries = []
        
        os.makedirs(self.screenshots_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
    
    def log(self, message, level="INFO"):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {level}: {message}"
        self.log_entries.append(entry)
        
        emoji = "✅" if level == "SUCCESS" else "🔄" if level == "PROGRESS" else "⚠️" if level == "WARNING" else "ℹ️"
        print(f"{emoji} {entry}")
    
    async def screenshot(self, name):
        """Take screenshot"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"{self.screenshots_dir}/targeted_{name}_{timestamp}.png"
        await self.page.screenshot(path=path, full_page=True)
        self.log(f"Screenshot saved: {name}", "SUCCESS")
        return path
    
    async def verify_exam_on_page(self):
        """Verify State Service Preliminary Examination 2026 is on the page"""
        self.log("Verifying exam name on page...", "PROGRESS")
        
        content = await self.page.content()
        
        # Check for exam keywords
        keywords = [
            "State Service Preliminary Examination 2026",
            "राज्य सेवा प्रारम्भिक परीक्षा 2026",
            "State Service",
            "राज्य सेवा",
            "Preliminary Examination 2026",
            "प्रारम्भिक परीक्षा 2026"
        ]
        
        found_keywords = [kw for kw in keywords if kw in content]
        
        if found_keywords:
            self.log(f"✓ Found exam keywords: {', '.join(found_keywords)}", "SUCCESS")
            return True
        else:
            self.log("✗ Exam keywords NOT found on page", "WARNING")
            return False
    
    async def find_and_click_exam_row(self):
        """Find the specific exam row and click it to reveal application link"""
        self.log("Looking for State Service Preliminary Examination 2026 row...", "PROGRESS")
        
        # Try to find the exam in a table row
        strategies = [
            # Strategy 1: Find row containing both "State Service" and "2026"
            {
                "name": "Table row with exam text",
                "script": """
                    () => {
                        const rows = Array.from(document.querySelectorAll('tr, div.row, div.exam-row'));
                        const targetRow = rows.find(row => {
                            const text = row.textContent;
                            return (
                                (text.includes('State Service') || text.includes('राज्य सेवा')) &&
                                (text.includes('2026') || text.includes('Preliminary') || text.includes('प्रारम्भिक'))
                            );
                        });
                        if (targetRow) {
                            targetRow.scrollIntoView({behavior: 'smooth', block: 'center'});
                            return true;
                        }
                        return false;
                    }
                """
            },
            # Strategy 2: Find and click any link with exam text
            {
                "name": "Link with exam text",
                "script": """
                    () => {
                        const links = Array.from(document.querySelectorAll('a'));
                        const targetLink = links.find(link => {
                            const text = link.textContent;
                            return (
                                (text.includes('State Service') || text.includes('राज्य सेवा')) &&
                                text.includes('2026')
                            );
                        });
                        if (targetLink) {
                            targetLink.click();
                            return true;
                        }
                        return false;
                    }
                """
            }
        ]
        
        for strategy in strategies:
            self.log(f"Trying strategy: {strategy['name']}", "PROGRESS")
            try:
                result = await self.page.evaluate(strategy['script'])
                if result:
                    self.log(f"✓ Strategy succeeded: {strategy['name']}", "SUCCESS")
                    await asyncio.sleep(3)
                    return True
            except Exception as e:
                self.log(f"Strategy failed: {str(e)}", "WARNING")
        
        return False
    
    async def find_application_link_in_context(self):
        """Find application link specifically in the context of State Service exam"""
        self.log("Searching for application link in exam context...", "PROGRESS")
        
        # First verify we can see the exam
        if not await self.verify_exam_on_page():
            self.log("Cannot proceed - exam not found on page", "WARNING")
            return None
        
        # Strategy 1: Find link near "State Service" text
        try:
            result = await self.page.evaluate("""
                () => {
                    // Find elements containing State Service text
                    const allElements = Array.from(document.querySelectorAll('*'));
                    const examElements = allElements.filter(el => {
                        const text = el.textContent;
                        return (
                            (text.includes('State Service') || text.includes('राज्य सेवा')) &&
                            text.includes('2026')
                        );
                    });
                    
                    // For each exam element, look for nearby application links
                    for (const examEl of examElements) {
                        // Check children and siblings
                        const nearby = [
                            ...Array.from(examEl.querySelectorAll('a')),
                            ...Array.from(examEl.parentElement.querySelectorAll('a'))
                        ];
                        
                        const appLink = nearby.find(a => {
                            const text = a.textContent.toLowerCase();
                            const href = (a.getAttribute('href') || '').toLowerCase();
                            return (
                                text.includes('apply') ||
                                text.includes('application') ||
                                text.includes('form') ||
                                text.includes('आवेदन') ||
                                text.includes('फॉर्म') ||
                                href.includes('apply') ||
                                href.includes('application') ||
                                href.includes('form')
                            );
                        });
                        
                        if (appLink) {
                            appLink.scrollIntoView({behavior: 'smooth', block: 'center'});
                            return {
                                found: true,
                                text: appLink.textContent.trim(),
                                href: appLink.getAttribute('href')
                            };
                        }
                    }
                    
                    return {found: false};
                }
            """)
            
            if result['found']:
                self.log(f"✓ Found application link: {result['text']}", "SUCCESS")
                self.log(f"  Link URL: {result['href']}", "INFO")
                return result
        
        except Exception as e:
            self.log(f"Link search error: {str(e)}", "WARNING")
        
        return None
    
    async def click_application_link(self):
        """Click the application link for State Service exam"""
        self.log("Attempting to click application link...", "PROGRESS")
        
        # Find the link
        link_info = await self.find_application_link_in_context()
        
        if not link_info or not link_info.get('found'):
            self.log("Application link not found", "WARNING")
            return False
        
        # Click it using JavaScript
        try:
            clicked = await self.page.evaluate("""
                () => {
                    const allElements = Array.from(document.querySelectorAll('*'));
                    const examElements = allElements.filter(el => {
                        const text = el.textContent;
                        return (
                            (text.includes('State Service') || text.includes('राज्य सेवा')) &&
                            text.includes('2026')
                        );
                    });
                    
                    for (const examEl of examElements) {
                        const nearby = [
                            ...Array.from(examEl.querySelectorAll('a')),
                            ...Array.from(examEl.parentElement.querySelectorAll('a'))
                        ];
                        
                        const appLink = nearby.find(a => {
                            const text = a.textContent.toLowerCase();
                            const href = (a.getAttribute('href') || '').toLowerCase();
                            return (
                                text.includes('apply') ||
                                text.includes('application') ||
                                text.includes('form') ||
                                text.includes('आवेदन') ||
                                text.includes('फॉर्म') ||
                                href.includes('apply') ||
                                href.includes('application') ||
                                href.includes('form')
                            );
                        });
                        
                        if (appLink) {
                            appLink.click();
                            return true;
                        }
                    }
                    return false;
                }
            """)
            
            if clicked:
                self.log("✓ Successfully clicked application link", "SUCCESS")
                await asyncio.sleep(5)
                return True
        
        except Exception as e:
            self.log(f"Click error: {str(e)}", "WARNING")
        
        return False
    
    async def run(self):
        """Main execution with specific focus on State Service Preliminary Examination 2026"""
        print("\n" + "="*80)
        print("🎯 TARGETED MPPSC STATE SERVICE PRELIMINARY EXAMINATION 2026 FILLER")
        print("="*80 + "\n")
        
        async with async_playwright() as p:
            self.browser = await p.chromium.launch(headless=False)
            self.context = await self.browser.new_context(viewport={"width": 1920, "height": 1080})
            self.page = await self.context.new_page()
            
            try:
                # Step 1: Go to portal
                print("\n" + "="*80)
                print("STEP 1: OPENING MPONLINE PORTAL")
                print("="*80)
                self.log("Navigating to MPOnline portal", "PROGRESS")
                await self.page.goto("https://mponline.gov.in/portal/", wait_until="networkidle")
                await asyncio.sleep(3)
                await self.screenshot("01_portal")
                
                # Step 2: Click MPPSC
                print("\n" + "="*80)
                print("STEP 2: CLICKING MPPSC")
                print("="*80)
                self.log("Looking for MPPSC link", "PROGRESS")
                
                mppsc_clicked = await self.page.evaluate("""
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
                
                if mppsc_clicked:
                    self.log("✓ Clicked MPPSC", "SUCCESS")
                    await asyncio.sleep(4)
                    await self.screenshot("02_mppsc_page")
                else:
                    self.log("MPPSC link not found", "WARNING")
                    await self.screenshot("02_no_mppsc")
                
                # Step 3: Verify and find State Service Exam
                print("\n" + "="*80)
                print("STEP 3: FINDING STATE SERVICE PRELIMINARY EXAMINATION 2026")
                print("="*80)
                
                # First, check if exam is visible
                exam_visible = await self.verify_exam_on_page()
                await self.screenshot("03_exam_search")
                
                if not exam_visible:
                    self.log("Exam not immediately visible, trying to find and click row", "PROGRESS")
                    await self.find_and_click_exam_row()
                    await asyncio.sleep(3)
                    await self.screenshot("03_after_row_click")
                    exam_visible = await self.verify_exam_on_page()
                
                if exam_visible:
                    # Step 4: Find and click application link
                    print("\n" + "="*80)
                    print("STEP 4: CLICKING APPLICATION FORM LINK")
                    print("="*80)
                    
                    await self.screenshot("04_before_app_link")
                    
                    if await self.click_application_link():
                        await self.screenshot("05_application_form")
                        self.log("✓ Successfully reached application form!", "SUCCESS")
                        
                        # Keep browser open for inspection
                        print("\n" + "="*80)
                        print("✅ SUCCESS - APPLICATION FORM REACHED")
                        print("="*80)
                        print("\nBrowser is open for you to inspect and manually fill the form")
                        print("Press Enter when done...")
                        input()
                    else:
                        self.log("Could not click application link", "WARNING")
                        await self.screenshot("04_stuck")
                        print("\nPress Enter to close...")
                        input()
                else:
                    self.log("Could not verify exam on page", "WARNING")
                    await self.screenshot("03_exam_not_found")
                    print("\nPress Enter to close...")
                    input()
                
            except Exception as e:
                self.log(f"Fatal error: {str(e)}", "WARNING")
                await self.screenshot("error")
            finally:
                # Save log
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                log_path = f"{self.logs_dir}/targeted_log_{timestamp}.txt"
                with open(log_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(self.log_entries))
                print(f"\n📝 Log saved: {log_path}")
                
                await self.browser.close()

if __name__ == "__main__":
    filler = TargetedMPPSCFiller()
    asyncio.run(filler.run())
