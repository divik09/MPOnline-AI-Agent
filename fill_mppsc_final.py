"""
FINAL MPPSC Form Filler - Click "Application Form" Action Button
Based on user screenshot showing exact table structure
"""

import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import os

async def fill_mppsc_final():
    """Click Application Form action button based on screenshot"""
    
    print("\n" + "="*90)
    print("🎯 FINAL MPPSC FORM FILLER - CLICKING APPLICATION FORM ACTION BUTTON")
    print("="*90 + "\n")
    
    screenshots_dir = "data/screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # STEP 1: Navigate to MPPSC page
            print("STEP 1: Navigating to MPPSC Attestation page...\n")
            
            target_url = "https://mponline.gov.in/Portal/Examinations/MPPSC/Attestation/Home/Home.aspx"
            await page.goto(target_url, wait_until="networkidle")
            await asyncio.sleep(3)
            
            await page.screenshot(path=f"{screenshots_dir}/final_01_page_{timestamp}.png", full_page=True)
            print(f"✅ Page loaded: {target_url}\n")
            
            # STEP 2: Find and click "Application Form" action button
            print("STEP 2: Finding 'Application Form' row and clicking Action button...\n")
            
            click_result = await page.evaluate("""
                () => {
                    // Find all table rows
                    const rows = Array.from(document.querySelectorAll('tr'));
                    
                    // Find the row containing "Application Form"
                    const appFormRow = rows.find(row => {
                        const text = row.textContent.trim();
                        return text.startsWith('Application Form') || 
                               text.includes('Application Form') && 
                               !text.includes('Pay for Unpaid') &&
                               !text.includes('Edit');
                    });
                    
                    if (!appFormRow) {
                        return {success: false, error: 'Application Form row not found'};
                    }
                    
                    // Find the action column (usually last cell with a link/button)
                    const cells = Array.from(appFormRow.querySelectorAll('td'));
                    const actionCell = cells[cells.length - 1]; // Last cell should be Action column
                    
                    if (!actionCell) {
                        return {success: false, error: 'Action column not found'};
                    }
                    
                    // Find clickable element in action cell
                    const actionButton = actionCell.querySelector('a, button, input[type="button"], input[type="submit"]');
                    
                    if (!actionButton) {
                        return {success: false, error: 'Action button not found in cell'};
                    }
                    
                    // Get button info before clicking
                    const buttonInfo = {
                        tag: actionButton.tagName,
                        text: actionButton.textContent.trim(),
                        href: actionButton.getAttribute('href'),
                        onclick: actionButton.getAttribute('onclick')
                    };
                    
                    // Click it
                    actionButton.click();
                    
                    return {
                        success: true,
                        buttonInfo: buttonInfo
                    };
                }
            """)
            
            if click_result['success']:
                print("✅ Successfully clicked Action button!")
                print(f"   Button: {click_result['buttonInfo']['tag']}")
                print(f"   Text: {click_result['buttonInfo']['text']}")
                print(f"   Href: {click_result['buttonInfo']['href']}\n")
                
                await asyncio.sleep(5)
                
                # Take screenshot after click
                await page.screenshot(path=f"{screenshots_dir}/final_02_after_click_{timestamp}.png", full_page=True)
                
                current_url = page.url
                print(f"📍 Current URL: {current_url}\n")
                
                # Check if we're on a form page
                if any(keyword in current_url.lower() for keyword in ['application', 'form', 'register', 'candidate']):
                    print("="*90)
                    print("✅ SUCCESS - APPLICATION FORM PAGE REACHED!")
                    print("="*90 + "\n")
                    
                    # Wait for form to load
                    await asyncio.sleep(3)
                    
                    # Analyze form
                    form_analysis = await page.evaluate("""
                        () => {
                            const inputs = Array.from(document.querySelectorAll('input:not([type="hidden"]), select, textarea'));
                            const visibleInputs = inputs.filter(inp => {
                                const style = window.getComputedStyle(inp);
                                return style.display !== 'none' && style.visibility !== 'hidden';
                            });
                            
                            return {
                                totalFields: visibleInputs.length,
                                fields: visibleInputs.slice(0, 20).map(inp => ({
                                    type: inp.type || inp.tagName.toLowerCase(),
                                    name: inp.name,
                                    id: inp.id,
                                    placeholder: inp.placeholder,
                                    required: inp.required
                                }))
                            };
                        }
                    """)
                    
                    print(f"📝 Form Fields Found: {form_analysis['totalFields']}\n")
                    print("First 20 fields:")
                    for idx, field in enumerate(form_analysis['fields'], 1):
                        req = " (REQUIRED)" if field['required'] else ""
                        print(f"   {idx}. [{field['type']}] {field['name'] or field['id'] or field['placeholder']}{req}")
                    
                    await page.screenshot(path=f"{screenshots_dir}/final_03_form_page_{timestamp}.png", full_page=True)
                    
                    print("\n" + "="*90)
                    print("🎮 READY FOR FORM FILLING")
                    print("="*90)
                    print("\nThe application form is now open in the browser.")
                    print("You can:")
                    print("1. Manually fill the form")
                    print("2. Or let me know and I'll create an auto-fill script")
                    print("\nPress Enter when done...")
                    input()
                else:
                    print("⚠️ URL changed but doesn't look like a form page")
                    print("Current page title:", await page.title())
                    print("\nPress Enter to close...")
                    input()
            else:
                print(f"❌ Failed to click: {click_result['error']}\n")
                await page.screenshot(path=f"{screenshots_dir}/final_error_{timestamp}.png", full_page=True)
                
                print("="*90)
                print("Manual Intervention Required")
                print("="*90)
                print("\nPlease manually click the 'Click Here' button in the Action column")
                print("for the 'Application Form' row, then press Enter...")
                input()
                
                # Check URL after manual click
                current_url = page.url
                print(f"\n📍 URL after manual click: {current_url}")
                
                if any(keyword in current_url.lower() for keyword in ['application', 'form']):
                    print("✅ Looks like you reached the form!")
                    await page.screenshot(path=f"{screenshots_dir}/final_manual_success_{timestamp}.png", full_page=True)
                
                print("\nPress Enter to close...")
                input()
                
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}\n")
            import traceback
            traceback.print_exc()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            await page.screenshot(path=f"{screenshots_dir}/final_exception_{timestamp}.png", full_page=True)
            
            print("\nPress Enter to close...")
            input()
        finally:
            await browser.close()
            print("\n✅ Browser closed")
            print(f"\n📁 Screenshots saved to: {screenshots_dir}/final_*")

if __name__ == "__main__":
    asyncio.run(fill_mppsc_final())
