"""
PRECISE MPPSC Form Filler - With User-Provided URL and Steps
Direct navigation to: https://mponline.gov.in/Portal/Examinations/MPPSC/Attestation/Home/Home.aspx
Steps: Find State Service Preliminary Examination 2026 → Check Application Form → Click Action button
"""

import asyncio
from playwright.async_api import async_playwright, TimeoutError
from datetime import datetime
import os

async def fill_mppsc_precise():
    """Fill MPPSC form using exact user-provided steps"""
    
    print("\n" + "="*90)
    print("🎯 PRECISE MPPSC STATE SERVICE PRELIMINARY EXAMINATION 2026 FORM FILLER")
    print("="*90 + "\n")
    
    screenshots_dir = "data/screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # STEP 1: Navigate directly to the MPPSC Attestation page
            print("="*90)
            print("STEP 1: NAVIGATING TO MPPSC ATTESTATION PAGE")
            print("="*90)
            
            target_url = "https://mponline.gov.in/Portal/Examinations/MPPSC/Attestation/Home/Home.aspx"
            print(f"\n📍 Going to: {target_url}\n")
            
            await page.goto(target_url, wait_until="networkidle")
            await asyncio.sleep(3)
            
            screenshot1 = f"{screenshots_dir}/precise_01_attestation_page_{timestamp}.png"
            await page.screenshot(path=screenshot1, full_page=True)
            print(f"✅ Page loaded")
            print(f"📸 Screenshot: {screenshot1}\n")
            
            # STEP 2: Find State Service Preliminary Examination 2026 in the table
            print("="*90)
            print("STEP 2: FINDING STATE SERVICE PRELIMINARY EXAMINATION 2026")
            print("="*90 + "\n")
            
            # Analyze table structure
            print("🔍 Analyzing table structure...\n")
            
            table_analysis = await page.evaluate("""
                () => {
                    const tables = Array.from(document.querySelectorAll('table'));
                    const rows = Array.from(document.querySelectorAll('tr'));
                    
                    const analysis = {
                        totalTables: tables.length,
                        totalRows: rows.length,
                        examRows: []
                    };
                    
                    // Find rows containing State Service 2026
                    rows.forEach((row, idx) => {
                        const text = row.textContent;
                        if ((text.includes('State Service') || text.includes('राज्य सेवा')) && 
                            text.includes('2026')) {
                            
                            const cells = Array.from(row.querySelectorAll('td, th'));
                            const checkboxes = Array.from(row.querySelectorAll('input[type="checkbox"], input[type="radio"]'));
                            const buttons = Array.from(row.querySelectorAll('button, input[type="button"], input[type="submit"], a.btn'));
                            const links = Array.from(row.querySelectorAll('a'));
                            
                            analysis.examRows.push({
                                index: idx,
                                text: text.trim().substring(0, 300),
                                cellCount: cells.length,
                                cellTexts: cells.map(c => c.textContent.trim()),
                                hasCheckboxes: checkboxes.length,
                                checkboxes: checkboxes.map(cb => ({
                                    type: cb.type,
                                    name: cb.name,
                                    id: cb.id,
                                    value: cb.value,
                                    checked: cb.checked
                                })),
                                hasButtons: buttons.length,
                                buttons: buttons.map(b => ({
                                    tag: b.tagName,
                                    type: b.type,
                                    text: b.textContent.trim(),
                                    id: b.id,
                                    className: b.className
                                })),
                                hasLinks: links.length,
                                links: links.map(l => ({
                                    text: l.textContent.trim(),
                                    href: l.getAttribute('href')
                                }))
                            });
                        }
                    });
                    
                    return analysis;
                }
            """)
            
            print(f"📊 Table Analysis:")
            print(f"   Total Tables: {table_analysis['totalTables']}")
            print(f"   Total Rows: {table_analysis['totalRows']}")
            print(f"   Exam Rows Found: {len(table_analysis['examRows'])}\n")
            
            if not table_analysis['examRows']:
                print("⚠️ STATE SERVICE PRELIMINARY EXAMINATION 2026 NOT FOUND")
                print("\nAsking user for guidance...\n")
                print("="*90)
                print("❓ QUESTION FOR USER:")
                print("="*90)
                print("\nI cannot find 'State Service Preliminary Examination 2026' on this page.")
                print("\nOptions:")
                print("1. Is the exam name different? (Please provide exact text)")
                print("2. Do I need to click something first to show the exam list?")
                print("3. Should I try the alternative: 'State Forest Service Preliminary Examination 2026'?\n")
                
                await page.screenshot(path=f"{screenshots_dir}/precise_exam_not_found_{timestamp}.png", full_page=True)
                
                print("The browser will stay open for your inspection.")
                print("Press Enter to close...")
                input()
                await browser.close()
                return
            
            # Display found exam rows
            print("✅ FOUND EXAM ROW(S):\n")
            for idx, exam_row in enumerate(table_analysis['examRows'], 1):
                print(f"  Row #{idx}:")
                print(f"    Text Preview: {exam_row['text'][:150]}...")
                print(f"    Cells: {exam_row['cellCount']}")
                print(f"    Cell Texts: {exam_row['cellTexts']}")
                print(f"    Checkboxes: {exam_row['hasCheckboxes']}")
                if exam_row['checkboxes']:
                    for cb in exam_row['checkboxes']:
                        print(f"      - Type: {cb['type']}, Name: {cb['name']}, ID: {cb['id']}, Value: {cb['value']}")
                print(f"    Buttons: {exam_row['hasButtons']}")
                if exam_row['buttons']:
                    for btn in exam_row['buttons']:
                        print(f"      - {btn['tag']}: '{btn['text']}' (ID: {btn['id']})")
                print(f"    Links: {exam_row['hasLinks']}")
                if exam_row['links']:
                    for link in exam_row['links']:
                        print(f"      - '{link['text']}' → {link['href']}")
                print()
            
            await page.screenshot(path=f"{screenshots_dir}/precise_02_exam_found_{timestamp}.png", full_page=True)
            
            # STEP 3: Check "Application Form" checkbox/option
            print("="*90)
            print("STEP 3: CHECKING APPLICATION FORM OPTION")
            print("="*90 + "\n")
            
            checkbox_checked = await page.evaluate("""
                () => {
                    // Find the exam row
                    const rows = Array.from(document.querySelectorAll('tr'));
                    const examRow = rows.find(row => {
                        const text = row.textContent;
                        return (text.includes('State Service') || text.includes('राज्य सेवा')) && 
                               text.includes('2026');
                    });
                    
                    if (!examRow) return {success: false, message: 'Exam row not found'};
                    
                    // Look for checkbox related to "Application Form"
                    // Try multiple strategies:
                    
                    // Strategy 1: Find checkbox with "application" in name/id/value
                    const checkboxes = Array.from(examRow.querySelectorAll('input[type="checkbox"], input[type="radio"]'));
                    let targetCheckbox = checkboxes.find(cb => 
                        (cb.name && cb.name.toLowerCase().includes('application')) ||
                        (cb.id && cb.id.toLowerCase().includes('application')) ||
                        (cb.value && cb.value.toLowerCase().includes('application')) ||
                        (cb.value && cb.value.toLowerCase().includes('form'))
                    );
                    
                    // Strategy 2: If there's a label with "Application Form", find associated checkbox
                    if (!targetCheckbox) {
                        const labels = Array.from(examRow.querySelectorAll('label, span, td'));
                        const appFormLabel = labels.find(l => 
                            l.textContent.includes('Application Form') ||
                            l.textContent.includes('Application') ||
                            l.textContent.includes('आवेदन')
                        );
                        
                        if (appFormLabel) {
                            // Look for checkbox near this label
                            targetCheckbox = appFormLabel.querySelector('input[type="checkbox"], input[type="radio"]');
                            if (!targetCheckbox && appFormLabel.parentElement) {
                                targetCheckbox = appFormLabel.parentElement.querySelector('input[type="checkbox"], input[type="radio"]');
                            }
                        }
                    }
                    
                    // Strategy 3: Just check the first checkbox if only one exists
                    if (!targetCheckbox && checkboxes.length === 1) {
                        targetCheckbox = checkboxes[0];
                    }
                    
                    if (targetCheckbox) {
                        targetCheckbox.checked = true;
                        // Trigger change event
                        targetCheckbox.dispatchEvent(new Event('change', { bubbles: true }));
                        targetCheckbox.dispatchEvent(new Event('click', { bubbles: true }));
                        
                        return {
                            success: true,
                            message: 'Checkbox checked',
                            checkboxInfo: {
                                type: targetCheckbox.type,
                                name: targetCheckbox.name,
                                id: targetCheckbox.id,
                                value: targetCheckbox.value
                            }
                        };
                    }
                    
                    return {success: false, message: 'No suitable checkbox found'};
                }
            """)
            
            if checkbox_checked['success']:
                print(f"✅ {checkbox_checked['message']}")
                print(f"   Checkbox: Type={checkbox_checked['checkboxInfo']['type']}, " +
                      f"Name={checkbox_checked['checkboxInfo']['name']}, " +
                      f"ID={checkbox_checked['checkboxInfo']['id']}\n")
                await asyncio.sleep(2)
            else:
                print(f"⚠️ {checkbox_checked['message']}\n")
                print("Asking user for guidance...\n")
                print("="*90)
                print("❓ QUESTION FOR USER:")
                print("="*90)
                print("\nI found the exam row but cannot locate the 'Application Form' checkbox/option.")
                print("Please check the browser and let me know:")
                print("1. Is there a specific checkbox I should click?")
                print("2. Or is the 'Application Form' a dropdown/select option?")
                print("3. Or should I directly click the Action button?\n")
                
                await page.screenshot(path=f"{screenshots_dir}/precise_checkbox_issue_{timestamp}.png", full_page=True)
                print("Press Enter after checking...")
                input()
            
            await page.screenshot(path=f"{screenshots_dir}/precise_03_after_checkbox_{timestamp}.png", full_page=True)
            
            # STEP 4: Click Action column button
            print("="*90)
            print("STEP 4: CLICKING ACTION COLUMN BUTTON")
            print("="*90 + "\n")
            
            action_clicked = await page.evaluate("""
                () => {
                    // Find the exam row
                    const rows = Array.from(document.querySelectorAll('tr'));
                    const examRow = rows.find(row => {
                        const text = row.textContent;
                        return (text.includes('State Service') || text.includes('राज्य सेवा')) && 
                               text.includes('2026');
                    });
                    
                    if (!examRow) return {success: false, message: 'Exam row not found'};
                    
                    // Find Action column (usually last column or labeled "Action")
                    const cells = Array.from(examRow.querySelectorAll('td'));
                    
                    // Strategy 1: Find cell containing "Action" or button-like elements
                    let actionCell = null;
                    
                    for (const cell of cells) {
                        const hasButton = cell.querySelector('button, input[type="button"], input[type="submit"], a.btn, a[onclick]');
                        if (hasButton) {
                            actionCell = cell;
                            break;
                        }
                    }
                    
                    // Strategy 2: Try last cell
                    if (!actionCell && cells.length > 0) {
                        actionCell = cells[cells.length - 1];
                    }
                    
                    if (actionCell) {
                        // Find clickable element in action cell
                        const button = actionCell.querySelector('button, input[type="button"], input[type="submit"], a.btn, a[onclick], a[href]');
                        
                        if (button) {
                            button.click();
                            return {
                                success: true,
                                message: 'Action button clicked',
                                buttonInfo: {
                                    tag: button.tagName,
                                    text: button.textContent.trim(),
                                    type: button.type,
                                    href: button.getAttribute('href')
                                }
                            };
                        }
                        
                        return {success: false, message: 'Action cell found but no clickable button'};
                    }
                    
                    return {success: false, message: 'Action column not found'};
                }
            """)
            
            if action_clicked['success']:
                print(f"✅ {action_clicked['message']}")
                print(f"   Button: {action_clicked['buttonInfo']['tag']} - '{action_clicked['buttonInfo']['text']}'\n")
                await asyncio.sleep(5)
                
                screenshot4 = f"{screenshots_dir}/precise_04_after_action_click_{timestamp}.png"
                await page.screenshot(path=screenshot4, full_page=True)
                print(f"📸 Screenshot: {screenshot4}\n")
                
                # Check if we reached application form page
                current_url = page.url
                print(f"📍 Current URL: {current_url}\n")
                
                if 'application' in current_url.lower() or 'form' in current_url.lower():
                    print("="*90)
                    print("✅ SUCCESS - APPLICATION FORM PAGE REACHED!")
                    print("="*90 + "\n")
                    
                    # Analyze form fields
                    await asyncio.sleep(2)
                    
                    form_info = await page.evaluate("""
                        () => {
                            const inputs = Array.from(document.querySelectorAll('input:not([type="hidden"]), select, textarea'));
                            return {
                                totalFields: inputs.length,
                                fields: inputs.slice(0, 30).map(inp => ({
                                    type: inp.type || inp.tagName,
                                    name: inp.name,
                                    id: inp.id,
                                    placeholder: inp.placeholder,
                                    label: inp.labels ? inp.labels[0]?.textContent : ''
                                }))
                            };
                        }
                    """)
                    
                    print(f"📝 Form Analysis:")
                    print(f"   Total Fields: {form_info['totalFields']}\n")
                    print("   Fields (first 30):")
                    for idx, field in enumerate(form_info['fields'], 1):
                        print(f"   {idx}. {field['type']}: {field['label'] or field['placeholder'] or field['name'] or field['id']}")
                    
                    print("\n" + "="*90)
                    print("🎮 READY FOR FORM FILLING")
                    print("="*90)
                    print("\nThe browser is open on the application form page.")
                    print("You can now:")
                    print("1. Manually fill the form")
                    print("2. Or I can attempt to auto-fill with sample data")
                    print("\nPress Enter when done or ready to close...")
                    input()
                else:
                    print("⚠️ Current URL doesn't look like an application form page")
                    print("Press Enter to close and review screenshots...")
                    input()
            else:
                print(f"⚠️ {action_clicked['message']}\n")
                print("="*90)
                print("❓ QUESTION FOR USER:")
                print("="*90)
                print("\nCould not click the Action button automatically.")
                print("Please manually click the action button in the browser")
                print("and then press Enter...\n")
                
                await page.screenshot(path=f"{screenshots_dir}/precise_action_issue_{timestamp}.png", full_page=True)
                input()
                
                # Check URL after manual click
                current_url = page.url
                print(f"\n📍 Current URL after manual interaction: {current_url}")
                
                if 'application' in current_url.lower() or 'form' in current_url.lower():
                    print("✅ Looks like you successfully reached the application form!")
                    await page.screenshot(path=f"{screenshots_dir}/precise_form_after_manual_{timestamp}.png", full_page=True)
                print("\nPress Enter to close...")
                input()
            
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}\n")
            import traceback
            traceback.print_exc()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            await page.screenshot(path=f"{screenshots_dir}/precise_error_{timestamp}.png", full_page=True)
            
            print("\nPress Enter to close...")
            input()
        finally:
            await browser.close()
            print("\n✅ Browser closed\n")
            print("="*90)
            print("📁 Check the following for evidence:")
            print(f"   Screenshots: {screenshots_dir}/precise_*")
            print("="*90)

if __name__ == "__main__":
    asyncio.run(fill_mppsc_precise())
