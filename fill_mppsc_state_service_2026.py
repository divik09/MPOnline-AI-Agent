"""
MPPSC State Service Preliminary Examination 2026 - Form Filling
Specific navigation path as instructed by user
"""
import asyncio
from advanced_form_filler import AdvancedFormFillingAgent
from datetime import datetime
import json


async def fill_mppsc_state_service_2026():
    """
    Navigate: mponline.gov.in/portal → MPPSC → State Service Preliminary Exam 2026
    Then fill the application form until payment page
    """
    print("=" * 80)
    print("🎯 MPPSC STATE SERVICE PRELIMINARY EXAMINATION 2026")
    print("=" * 80)
    
    # Test data for form filling
    form_data = {
        # Personal Information
        "name": "Rajesh Kumar Sharma",
        "fullname": "Rajesh Kumar Sharma",
        "fname": "Ram Kumar Sharma",
        "father": "Ram Kumar Sharma",
        "fathername": "Ram Kumar Sharma",
        "mname": "Sita Devi Sharma",
        "mother": "Sita Devi Sharma",
        "mothername": "Sita Devi Sharma",
        
        # Date of Birth
        "dob": "01/01/1995",
        "dateofbirth": "01/01/1995",
        "dobdd": "01",
        "dobmm": "01",
        "dobyyyy": "1995",
        
        # Gender and Category
        "gender": "Male",
        "sex": "Male",
        "category": "General",
        "cast": "General",
        "caste": "General",
        
        # Contact Details
        "email": "rajesh.kumar.mppsc@example.com",
        "emailid": "rajesh.kumar.mppsc@example.com",
        "mobile": "9876543210",
        "mobileno": "9876543210",
        "phone": "9876543210",
        "contact": "9876543210",
        "altmobile": "9123456789",
        "alternatemobile": "9123456789",
        
        # Address
        "address": "Plot No 123, Sector A, Arera Colony, Bhopal, Madhya Pradesh",
        "permanentaddress": "Plot No 123, Sector A, Arera Colony, Bhopal",
        "correspondenceaddress": "Plot No 123, Sector A, Arera Colony, Bhopal",
        "addressline1": "Plot No 123, Sector A",
        "addressline2": "Arera Colony",
        "city": "Bhopal",
        "district": "Bhopal",
        "state": "Madhya Pradesh",
        "pincode": "462001",
        "pin": "462001",
        
        # Education
        "qualification": "Graduate",
        "highestqualification": "Bachelor of Arts",
        "degree": "Bachelor of Arts",
        "university": "Barkatullah University",
        "board": "Barkatullah University",
        "passingyear": "2020",
        "year": "2020",
        "yearofpassing": "2020",
        "percentage": "75.50",
        "marks": "75.50",
        "cgpa": "7.5",
        
        # Additional Information
        "nationality": "Indian",
        "religion": "Hindu",
        "maritalstatus": "Single",
        "aadhar": "123456789012",
        "aadharnumber": "123456789012",
        "pan": "ABCDE1234F",
        "pannumber": "ABCDE1234F",
        
        # Exam Preferences
        "examcenter": "Bhopal",
        "preferredcenter": "Bhopal",
        "center": "Bhopal",
        "medium": "Hindi",
        "exammedium": "Hindi",
        "languagemedium": "Hindi",
    }
    
    agent = AdvancedFormFillingAgent(headless=False)
    stages_log = []
    
    try:
        # Stage 1: Start Browser
        print("\n" + "▶" * 80)
        print("STAGE 1: Browser Initialization")
        print("▶" * 80)
        await agent.start_browser()
        stages_log.append({"stage": "browser_init", "status": "success"})
        
        # Stage 2: Navigate to MPOnline Portal
        print("\n" + "▶" * 80)
        print("STAGE 2: Navigate to MPOnline Portal")
        print("▶" * 80)
        
        portal_url = "https://mponline.gov.in/portal/"
        print(f"🌐 Opening: {portal_url}")
        success = await agent.navigate_to_service(portal_url)
        
        if not success:
            print("❌ Failed to load portal homepage")
            return
        
        stages_log.append({"stage": "portal_navigation", "status": "success", "url": portal_url})
        await asyncio.sleep(3)
        
        # Stage 3: Click on MPPSC Portal
        print("\n" + "▶" * 80)
        print("STAGE 3: Clicking on MPPSC Portal")
        print("▶" * 80)
        
        print("🔍 Looking for MPPSC link...")
        
        # Try multiple selectors for MPPSC
        mppsc_selectors = [
            'a:has-text("MPPSC")',
            'a:has-text("Madhya Pradesh Public Service")',
            'a[href*="mppsc"]',
            'a[href*="MPPSC"]',
            '.service-link:has-text("MPPSC")',
        ]
        
        mppsc_clicked = False
        for selector in mppsc_selectors:
            try:
                mppsc_link = await agent.page.query_selector(selector)
                if mppsc_link:
                    is_visible = await mppsc_link.is_visible()
                    if is_visible:
                        print(f"✅ Found MPPSC link: {selector}")
                        await mppsc_link.scroll_into_view_if_needed()
                        await asyncio.sleep(1)
                        
                        # Take screenshot before click
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        await agent.page.screenshot(path=f"data/screenshots/before_mppsc_click_{timestamp}.png")
                        
                        await mppsc_link.click()
                        mppsc_clicked = True
                        print("✅ Clicked on MPPSC portal")
                        await asyncio.sleep(5)  # Wait for page to load
                        break
            except Exception as e:
                print(f"⚠️  Selector {selector} failed: {e}")
                continue
        
        if not mppsc_clicked:
            print("❌ Could not find or click MPPSC link")
            print("📸 Taking screenshot of current page for debugging...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            await agent.page.screenshot(path=f"data/screenshots/mppsc_not_found_{timestamp}.png", full_page=True)
            print("💡 Please check the screenshot to manually locate MPPSC link")
            await asyncio.sleep(10)  # Keep browser open
            return
        
        stages_log.append({"stage": "mppsc_click", "status": "success"})
        
        # Stage 4: Find State Service Preliminary Examination 2026
        print("\n" + "▶" * 80)
        print("STAGE 4: Finding State Service Preliminary Examination 2026")
        print("▶" * 80)
        
        print("🔍 Searching for State Service Preliminary Examination 2026...")
        
        # Try different variations
        exam_selectors = [
            'a:has-text("State Service Preliminary Examination 2026")',
            'a:has-text("Preliminary Examination 2026")',
            'a:has-text("राज्य सेवा प्रारंभिक परीक्षा 2026")',
            'a:has-text("2026")',
            'button:has-text("State Service")',
            'div:has-text("2026")',
        ]
        
        exam_found = False
        for selector in exam_selectors:
            try:
                elements = await agent.page.query_selector_all(selector)
                for elem in elements:
                    text = await elem.text_content()
                    if text and ("2026" in text or "State Service" in text or "Preliminary" in text):
                        print(f"✅ Found potential exam link: {text.strip()[:100]}")
                        
                        # Try to click
                        is_visible = await elem.is_visible()
                        if is_visible:
                            await elem.scroll_into_view_if_needed()
                            await asyncio.sleep(1)
                            
                            # Screenshot before click
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            await agent.page.screenshot(path=f"data/screenshots/before_exam_click_{timestamp}.png")
                            
                            await elem.click()
                            exam_found = True
                            print(f"✅ Clicked on: {text.strip()[:100]}")
                            await asyncio.sleep(5)
                            break
            except Exception as e:
                continue
        
            if exam_found:
                break
        
        if not exam_found:
            print("⚠️  Could not auto-find the exact exam")
            print("📸 Taking screenshot to help locate it...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            await agent.page.screenshot(path=f"data/screenshots/exam_page_{timestamp}.png", full_page=True)
            print("💡 Browser will stay open - please manually click on the exam")
            await asyncio.sleep(30)
        
        stages_log.append({"stage": "exam_selection", "status": "success" if exam_found else "manual_required"})
        
        # Stage 5: Look for Application Form / Register / Apply
        print("\n" + "▶" * 80)
        print("STAGE 5: Looking for Application Form Link")
        print("▶" * 80)
        
        apply_selectors = [
            'a:has-text("Fill Application")',
            'a:has-text("Apply Online")',
            'a:has-text("आवेदन करें")',
            'a:has-text("Registration")',
            'a:has-text("New Registration")',
            'button:has-text("Apply")',
            'a:has-text("Application Form")',
        ]
        
        apply_found = False
        for selector in apply_selectors:
            try:
                apply_link = await agent.page.query_selector(selector)
                if apply_link:
                    is_visible = await apply_link.is_visible()
                    if is_visible:
                        text = await apply_link.text_content()
                        print(f"✅ Found application link: {text.strip()}")
                        
                        await apply_link.scroll_into_view_if_needed()
                        await asyncio.sleep(1)
                        
                        # Screenshot
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        await agent.page.screenshot(path=f"data/screenshots/before_apply_click_{timestamp}.png")
                        
                        await apply_link.click()
                        apply_found = True
                        print("✅ Clicked on application link")
                        await asyncio.sleep(5)
                        break
            except:
                continue
        
        if not apply_found:
            print("⚠️  Application link not found with standard selectors")
            print("📸 Capturing current page...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            await agent.page.screenshot(path=f"data/screenshots/application_page_{timestamp}.png", full_page=True)
        
        stages_log.append({"stage": "application_link", "status": "success" if apply_found else "manual_required"})
        
        # Stage 6: Detect and Fill Form Fields
        print("\n" + "▶" * 80)
        print("STAGE 6: Detecting Form Fields")
        print("▶" * 80)
        
        current_url = agent.page.url
        print(f"📍 Current URL: {current_url}")
        
        fields = await agent.detect_form_fields()
        
        if len(fields) > 0:
            print(f"📋 Found {len(fields)} form fields!")
            
            # Stage 7: Fill the Form
            print("\n" + "▶" * 80)
            print("STAGE 7: Filling Application Form")
            print("▶" * 80)
            
            filled = await agent.auto_fill_form(form_data)
            
            if filled:
                print("✅ Form filling completed!")
                stages_log.append({"stage": "form_filling", "status": "success", "fields_filled": len(fields)})
                
                # Screenshot after filling
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                await agent.page.screenshot(path=f"data/screenshots/form_filled_{timestamp}.png", full_page=True)
                
                # Stage 8: Look for Next/Submit/Continue button
                print("\n" + "▶" * 80)
                print("STAGE 8: Finding Next/Submit Button")
                print("▶" * 80)
                
                next_found = await agent.find_and_click_submit()
                
                if next_found:
                    print("✅ Found next button (Demo mode - not clicking)")
                    await asyncio.sleep(3)
                    
                    # Check if we reached payment or next page
                    new_url = agent.page.url
                    print(f"📍 Current URL: {new_url}")
                    
                    if new_url != current_url:
                        print("✅ Navigated to next page/section")
                        
                        # Screenshot
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        await agent.page.screenshot(path=f"data/screenshots/next_page_{timestamp}.png", full_page=True)
                        
                        # Check for payment keywords
                        page_text = await agent.page.content()
                        if any(word in page_text.lower() for word in ["payment", "pay", "fee", "amount", "checkout"]):
                            print("🎉 REACHED PAYMENT PAGE!")
                            stages_log.append({"stage": "payment_page_reached", "status": "success"})
                        else:
                            print("📄 On next form page - may need to continue filling")
            else:
                print("⚠️  No fields were filled")
        else:
            print("⚠️  No form fields detected on this page")
            print("💡 This might be:")
            print("   - A confirmation page")
            print("   - Login required page")
            print("   - Or we need to navigate further")
        
        # Final screenshots and logs
        print("\n" + "▶" * 80)
        print("STAGE 9: Final Evidence Collection")
        print("▶" * 80)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_screenshot = f"data/screenshots/final_state_{timestamp}.png"
        await agent.page.screenshot(path=final_screenshot, full_page=True)
        print(f"📸 Final screenshot: {final_screenshot}")
        
        await agent.save_action_log()
        
        # Save stages log
        stages_file = f"data/logs/mppsc_stages_{timestamp}.json"
        with open(stages_file, 'w', encoding='utf-8') as f:
            json.dump(stages_log, f, indent=2)
        
        print("\n" + "=" * 80)
        print("📊 EXECUTION SUMMARY")
        print("=" * 80)
        
        for stage in stages_log:
            status_icon = "✅" if stage["status"] == "success" else "⚠️"
            print(f"{status_icon} {stage['stage']}: {stage['status']}")
        
        print(f"\n📸 All screenshots saved in: data/screenshots/")
        print(f"📝 All logs saved in: data/logs/")
        print(f"📍 Final URL: {agent.page.url}")
        
        print("\n⏸️  Browser will stay open for 30 seconds for inspection...")
        await asyncio.sleep(30)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        
        # Screenshot on error
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            await agent.page.screenshot(path=f"data/screenshots/error_{timestamp}.png", full_page=True)
        except:
            pass
    
    finally:
        await agent.close()
        print("\n✅ Test completed!")


if __name__ == "__main__":
    print("Starting MPPSC State Service Preliminary Examination 2026 form filling...")
    asyncio.run(fill_mppsc_state_service_2026())
