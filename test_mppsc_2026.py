"""
End-to-End Test: MPPSC 2026 Form Filling
Tests the autonomous form filling application with real MPPSC 2026 form
"""
import asyncio
from advanced_form_filler import AdvancedFormFillingAgent
from datetime import datetime
import json

async def test_mppsc_2026_form():
    """
    Complete test of MPPSC 2026 form filling until payment option.
    """
    print("=" * 70)
    print("🧪 TESTING: MPPSC 2026 Form Filling - End-to-End")
    print("=" * 70)
    
    # Sample test data for MPPSC 2026
    test_data = {
        # Personal Information
        "name": "Rajesh Kumar Sharma",
        "fullname": "Rajesh Kumar Sharma",
        "fname": "Ram Kumar Sharma",
        "father": "Ram Kumar Sharma",
        "fathername": "Ram Kumar Sharma",
        "mname": "Sita Devi",
        "mother": "Sita Devi",
        "mothername": "Sita Devi",
        
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
        "email": "rajesh.kumar.test@example.com",
        "emailid": "rajesh.kumar.test@example.com",
        "email_id": "rajesh.kumar.test@example.com",
        "mobile": "9876543210",
        "mobileno": "9876543210",
        "phone": "9876543210",
        "contact": "9876543210",
        "altmobile": "9876543211",
        
        # Address
        "address": "Plot No 123, Sector A, Arera Colony",
        "permanentaddress": "Plot No 123, Sector A, Arera Colony",
        "addressline1": "Plot No 123, Sector A",
        "addressline2": "Arera Colony",
        "city": "Bhopal",
        "district": "Bhopal",
        "state": "Madhya Pradesh",
        "pincode": "462001",
        "pin": "462001",
        
        # Education
        "qualification": "Graduate",
        "highestqualification": "Graduate",
        "degree": "Bachelor of Arts",
        "university": "Barkatullah University",
        "board": "Barkatullah University",
        "passingyear": "2020",
        "year": "2020",
        "percentage": "75.5",
        "marks": "75.5",
        "cgpa": "7.5",
        
        # Other common fields
        "nationality": "Indian",
        "religion": "Hindu",
        "maritalstatus": "Single",
        "occupation": "Student",
        
        # Exam specific
        "examcenter": "Bhopal",
        "preferredcenter": "Bhopal",
        "medium": "Hindi",
        "exammedium": "Hindi",
    }
    
    agent = AdvancedFormFillingAgent(headless=False)
    test_results = {
        "test_name": "MPPSC 2026 Form Filling",
        "timestamp": datetime.now().isoformat(),
        "stages": []
    }
    
    try:
        # Stage 1: Initialize Browser
        print("\n" + "▶" * 70)
        print("STAGE 1: Browser Initialization")
        print("▶" * 70)
        
        await agent.start_browser()
        test_results["stages"].append({
            "stage": "browser_init",
            "status": "success",
            "message": "Browser started successfully"
        })
        
        # Stage 2: Navigate to MPPSC Portal
        print("\n" + "▶" * 70)
        print("STAGE 2: Navigation to MPPSC Portal")
        print("▶" * 70)
        
        mppsc_url = "https://mppsc.mponline.gov.in"
        success = await agent.navigate_to_service(mppsc_url)
        
        if not success:
            test_results["stages"].append({
                "stage": "navigation",
                "status": "failed",
                "message": "Failed to navigate to MPPSC portal"
            })
            print("❌ Navigation failed!")
            return test_results
        
        test_results["stages"].append({
            "stage": "navigation", 
            "status": "success",
            "url": mppsc_url
        })
        
        # Stage 3: Analyze Homepage
        print("\n" + "▶" * 70)
        print("STAGE 3: Homepage Analysis")
        print("▶" * 70)
        
        await asyncio.sleep(3)  # Wait for page to settle
        
        # Look for application links
        print("🔍 Searching for 2026 application links...")
        
        try:
            # Check for common application link patterns
            link_selectors = [
                'a:has-text("2026")',
                'a:has-text("Online Application")',
                'a:has-text("Apply Online")',
                'a:has-text("New Registration")',
                'a:has-text("Registration")',
                'a:has-text("Application")',
            ]
            
            found_links = []
            for selector in link_selectors:
                try:
                    links = await agent.page.query_selector_all(selector)
                    for link in links[:5]:  # Check first 5 of each type
                        text = await link.text_content()
                        href = await link.get_attribute('href')
                        if text and href:
                            found_links.append({
                                "text": text.strip(),
                                "href": href,
                                "selector": selector
                            })
                except:
                    continue
            
            print(f"✅ Found {len(found_links)} potential application links")
            for i, link in enumerate(found_links[:10], 1):
                print(f"   {i}. {link['text']}")
            
            test_results["stages"].append({
                "stage": "homepage_analysis",
                "status": "success",
                "links_found": len(found_links),
                "sample_links": found_links[:5]
            })
            
        except Exception as e:
            print(f"⚠️  Error analyzing homepage: {e}")
        
        # Stage 4: Detect Form Fields on Current Page
        print("\n" + "▶" * 70)
        print("STAGE 4: Form Field Detection")
        print("▶" * 70)
        
        fields = await agent.detect_form_fields()
        
        test_results["stages"].append({
            "stage": "field_detection",
            "status": "success",
            "fields_count": len(fields),
            "field_types": {}
        })
        
        # Categorize fields
        field_types = {}
        for field in fields:
            ftype = field.get('type', 'unknown')
            if ftype not in field_types:
                field_types[ftype] = 0
            field_types[ftype] += 1
        
        test_results["stages"][-1]["field_types"] = field_types
        
        # Stage 5: Auto-Fill Available Forms
        print("\n" + "▶" * 70)
        print("STAGE 5: Form Filling")
        print("▶" * 70)
        
        if len(fields) > 0:
            print(f"📝 Attempting to fill {len(fields)} detected fields...")
            filled = await agent.auto_fill_form(test_data)
            
            test_results["stages"].append({
                "stage": "form_filling",
                "status": "success" if filled else "no_fields_filled",
                "fields_available": len(fields)
            })
        else:
            print("⚠️  No fillable fields detected on this page")
            print("💡 This might be because:")
            print("   - The homepage doesn't have a form")
            print("   - Need to click on application link first")
            print("   - Registration/Login required")
            
            test_results["stages"].append({
                "stage": "form_filling",
                "status": "skipped",
                "reason": "no_fields_on_homepage"
            })
        
        # Stage 6: Look for Submit/Next/Apply buttons
        print("\n" + "▶" * 70)
        print("STAGE 6: Finding Action Buttons")
        print("▶" * 70)
        
        button_selectors = [
            'button:has-text("Apply")',
            'a:has-text("Apply Online")',
            'button:has-text("Register")',
            'a:has-text("New Registration")',
            'button:has-text("Submit")',
            'button:has-text("Next")',
            'a:has-text("Click Here")',
        ]
        
        found_buttons = []
        for selector in button_selectors:
            try:
                buttons = await agent.page.query_selector_all(selector)
                for btn in buttons:
                    text = await btn.text_content()
                    is_visible = await btn.is_visible()
                    if text and is_visible:
                        found_buttons.append({
                            "text": text.strip(),
                            "selector": selector,
                            "visible": is_visible
                        })
            except:
                continue
        
        print(f"🔍 Found {len(found_buttons)} action buttons:")
        for i, btn in enumerate(found_buttons[:10], 1):
            print(f"   {i}. {btn['text']} ({btn['selector']})")
        
        test_results["stages"].append({
            "stage": "button_detection",
            "status": "success",
            "buttons_found": len(found_buttons),
            "sample_buttons": found_buttons[:5]
        })
        
        # Stage 7: Take Final Screenshots
        print("\n" + "▶" * 70)
        print("STAGE 7: Evidence Collection")
        print("▶" * 70)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Full page screenshot
        full_screenshot = f"data/screenshots/mppsc_2026_test_full_{timestamp}.png"
        await agent.page.screenshot(path=full_screenshot, full_page=True)
        print(f"📸 Full page screenshot: {full_screenshot}")
        
        # Current viewport screenshot
        viewport_screenshot = f"data/screenshots/mppsc_2026_test_viewport_{timestamp}.png"
        await agent.page.screenshot(path=viewport_screenshot)
        print(f"📸 Viewport screenshot: {viewport_screenshot}")
        
        test_results["stages"].append({
            "stage": "evidence_collection",
            "status": "success",
            "screenshots": [full_screenshot, viewport_screenshot]
        })
        
        # Save action log
        await agent.save_action_log()
        
        # Stage 8: Summary
        print("\n" + "=" * 70)
        print("📊 TEST SUMMARY")
        print("=" * 70)
        
        print(f"\n✅ Stages Completed: {len(test_results['stages'])}")
        for stage in test_results["stages"]:
            status_icon = "✅" if stage["status"] == "success" else "⚠️"
            print(f"   {status_icon} {stage['stage']}: {stage['status']}")
        
        print(f"\n📸 Screenshots saved:")
        print(f"   - {full_screenshot}")
        print(f"   - {viewport_screenshot}")
        
        print(f"\n📝 Action logs saved in: data/logs/")
        
        print("\n💡 NEXT STEPS:")
        print("   1. Review the screenshots to see the current page")
        print("   2. If application link is visible, we can click it")
        print("   3. Then proceed with full form filling")
        print("   4. Continue until payment page is reached")
        
        # Save test results
        results_file = f"data/logs/mppsc_2026_test_results_{timestamp}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(test_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Test results saved: {results_file}")
        
        # Keep browser open for inspection
        print("\n⏸️  Browser will stay open for 30 seconds for inspection...")
        await asyncio.sleep(30)
        
        return test_results
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        test_results["error"] = str(e)
        return test_results
        
    finally:
        await agent.close()
        print("\n✅ Test completed!")


if __name__ == "__main__":
    results = asyncio.run(test_mppsc_2026_form())
    print("\n" + "=" * 70)
    print("Test execution finished. Check screenshots and logs for details.")
    print("=" * 70)
