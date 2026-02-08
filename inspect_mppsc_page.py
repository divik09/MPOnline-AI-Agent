"""
ADVANCED MPPSC Form Filler - With Page Inspection and Manual Guidance
Shows detailed page structure analysis to help locate the application link
"""

import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import json
import os

async def inspect_page_for_exam():
    """Detailed page inspection to find State Service Preliminary Examination 2026"""
    
    print("\n" + "="*90)
    print("🔍 ADVANCED MPPSC STATE SERVICE PRELIMINARY EXAMINATION 2026 - PAGE INSPECTOR")
    print("="*90 + "\n")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()
        
        screenshots_dir = "data/screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        
        try:
            # Step 1: Navigate to portal
            print("▶ Step 1: Opening MPOnline Portal...")
            await page.goto("https://mponline.gov.in/portal/", wait_until="networkidle")
            await asyncio.sleep(3)
            print("✅ Portal loaded\n")
            
            # Step 2: Click MPPSC
            print("▶ Step 2: Clicking MPPSC...")
            mppsc_result = await page.evaluate("""
                () => {
                    const links = Array.from(document.querySelectorAll('a'));
                    const mppscLink = links.find(a => 
                        a.textContent.includes('MPPSC') || 
                        a.textContent.includes('एमपीपीएससी')
                    );
                    if (mppscLink) {
                        mppscLink.click();
                        return {success: true, text: mppscLink.textContent.trim()};
                    }
                    return {success: false};
                }
            """)
            
            if mppsc_result['success']:
                print(f"✅ Clicked: {mppsc_result['text']}\n")
                await asyncio.sleep(4)
            else:
                print("❌ MPPSC link not found\n")
                await browser.close()
                return
            
            # Step 3: Analyze page structure for State Service exam
            print("▶ Step 3: Analyzing page for State Service Preliminary Examination 2026...\n")
            
            page_analysis = await page.evaluate("""
                () => {
                    const analysis = {
                        examFound: false,
                        examElements: [],
                        links: [],
                        tables: [],
                        buttons: []
                    };
                    
                    // Find all elements containing exam text
                    const allElements = Array.from(document.querySelectorAll('*'));
                    const examElements = allElements.filter(el => {
                        const text = el.textContent;
                        return (
                            (text.includes('State Service') || text.includes('राज्य सेवा')) &&
                            text.includes('2026')
                        );
                    });
                    
                    analysis.examFound = examElements.length > 0;
                    
                    // Analyze each exam element
                    examElements.forEach((el, idx) => {
                        const info = {
                            index: idx,
                            tag: el.tagName,
                            text: el.textContent.trim().substring(0, 200),
                            hasLinks: el.querySelectorAll('a').length,
                            hasButtons: el.querySelectorAll('button').length,
                            className: el.className,
                            id: el.id
                        };
                        
                        // Find links within or near this element
                        const nearbyLinks = [
                            ...Array.from(el.querySelectorAll('a')),
                            ...Array.from(el.parentElement?.querySelectorAll('a') || [])
                        ];
                        
                        info.links = nearbyLinks.map(a => ({
                            text: a.textContent.trim(),
                            href: a.getAttribute('href'),
                            visible: a.offsetParent !== null
                        }));
                        
                        analysis.examElements.push(info);
                    });
                    
                    // Find ALL links on page
                    const allLinks = Array.from(document.querySelectorAll('a'));
                    analysis.links = allLinks
                        .filter(a => {
                            const text = a.textContent.toLowerCase();
                            const href = (a.getAttribute('href') || '').toLowerCase();
                            return (
                                text.includes('apply') ||
                                text.includes('application') ||
                                text.includes('form') ||
                                text.includes('आवेदन') ||
                                text.includes('फॉर्म') ||
                                href.includes('apply') ||
                                href.includes('application')
                            );
                        })
                        .map(a => ({
                            text: a.textContent.trim(),
                            href: a.getAttribute('href'),
                            visible: a.offsetParent !== null,
                            nearStateService: (() => {
                                let parent = a.parentElement;
                                for (let i = 0; i < 5 && parent; i++) {
                                    if (parent.textContent.includes('State Service') || 
                                        parent.textContent.includes('राज्य सेवा')) {
                                        return true;
                                    }
                                    parent = parent.parentElement;
                                }
                                return false;
                            })()
                        }));
                    
                    return analysis;
                }
            """)
            
            # Print analysis results
            print("="*90)
            print("📊 PAGE ANALYSIS RESULTS")
            print("="*90 + "\n")
            
            print(f"🎯 Exam Found on Page: {'YES ✅' if page_analysis['examFound'] else 'NO ❌'}\n")
            
            if page_analysis['examFound']:
                print(f"📍 Found {len(page_analysis['examElements'])} element(s) containing exam text:\n")
                
                for elem in page_analysis['examElements']:
                    print(f"  Element #{elem['index']}:")
                    print(f"    Tag: <{elem['tag']}>")
                    print(f"    Class: {elem['className']}")
                    print(f"    ID: {elem['id']}")
                    print(f"    Text Preview: {elem['text'][:100]}...")
                    print(f"    Contains {elem['hasLinks']} links, {elem['hasButtons']} buttons")
                    
                    if elem['links']:
                        print(f"    📎 Links found:")
                        for link in elem['links']:
                            visible_status = "👁️ VISIBLE" if link['visible'] else "🔒 HIDDEN"
                            print(f"      - [{visible_status}] {link['text']}")
                            print(f"        → {link['href']}")
                    print()
            
            print("="*90)
            print(f"🔗 ALL APPLICATION-RELATED LINKS ON PAGE ({len(page_analysis['links'])} found):")
            print("="*90 + "\n")
            
            if page_analysis['links']:
                for idx, link in enumerate(page_analysis['links'], 1):
                    visible_status = "👁️ VISIBLE" if link['visible'] else "🔒 HIDDEN"
                    near_exam = "⭐ NEAR STATE SERVICE" if link['nearStateService'] else ""
                    print(f"{idx}. [{visible_status}] {near_exam}")
                    print(f"   Text: {link['text']}")
                    print(f"   Href: {link['href']}\n")
            else:
                print(" No application-related links found\n")
            
            # Save analysis to JSON
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            analysis_path = f"data/logs/page_analysis_{timestamp}.json"
            os.makedirs("data/logs", exist_ok=True)
            with open(analysis_path, 'w', encoding='utf-8') as f:
                json.dump(page_analysis, f, indent=2, ensure_ascii=False)
            print(f"📝 Detailed analysis saved to: {analysis_path}\n")
            
            # Take screenshot
            screenshot_path = f"{screenshots_dir}/inspection_{timestamp}.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 Screenshot saved: {screenshot_path}\n")
            
            # Interactive mode - wait for user guidance
            print("="*90)
            print("🎮 INTERACTIVE MODE - MANUAL GUIDANCE")
            print("="*90)
            print("\nThe browser is now open showing the MPPSC page.")
            print("You can see the State Service Preliminary Examination 2026 listing.")
            print("\nOptions:")
            print("1. Press Enter if you want me to try clicking links automatically")
            print("2. Or manually click the 'Application Form' link yourself and then press Enter")
            print("3. The browser will stay open for your inspection\n")
            
            input("Press Enter when ready to continue or after manual click...")
            
            # Check current URL
            current_url = page.url
            print(f"\n📍 Current URL: {current_url}")
            
            if 'application' in current_url.lower() or 'apply' in current_url.lower() or 'form' in current_url.lower():
                print("✅ Looks like we're on an application page!")
                
                # Try to fill basic form fields
                print("\n▶ Step 4: Attempting to fill form fields...")
                
                await asyncio.sleep(2)
                await page.screenshot(path=f"{screenshots_dir}/form_page_{timestamp}.png")
                
                # Get form fields
                form_fields = await page.evaluate("""
                    () => {
                        const inputs = Array.from(document.querySelectorAll('input, select, textarea'));
                        return inputs.map(inp => ({
                            type: inp.type,
                            name: inp.name,
                            id: inp.id,
                            placeholder: inp.placeholder,
                            visible: inp.offsetParent !== null
                        })).filter(f => f.visible);
                    }
                """)
                
                print(f"\n📝 Found {len(form_fields)} visible form fields:")
                for idx, field in enumerate(form_fields[:20], 1):  # Show first 20
                    print(f"  {idx}. Type: {field['type']}, Name: {field['name']}, ID: {field['id']}")
                
                print("\n✅ You can now manually fill the form!")
                print("Press Enter when you want to close the browser...")
                input()
            else:
                print("⚠️ Not on application page yet. You may need to manual click or check the page structure.")
                print("\nPress Enter to close browser...")
                input()
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            await browser.close()
            print("\n✅ Browser closed. Check screenshots and logs for details.")

if __name__ == "__main__":
    asyncio.run(inspect_page_for_exam())
