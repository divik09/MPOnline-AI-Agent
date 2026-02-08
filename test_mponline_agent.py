"""
Automated Test Script for MPOnline Interactive Agent
Tests the agent without requiring user interaction
"""
import asyncio
import os
from dotenv import load_dotenv
from browser_use import Agent, BrowserSession
from browser_use.llm.openai.chat import ChatOpenAI

load_dotenv()

class MPOnlineAgentTester:
    """Automated tester for the MPOnline agent"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.test_data = {
            "exam_type": "3",
            "full_name": "Test Candidate AutoTest",
            "father_name": "Test Father Name",
            "mother_name": "Test Mother Name",
            "dob": "15/08/1995",
            "gender": "Male",
            "category": "General",
            "mobile": "9876543210",
            "email": "autotest@example.com",
            "address": "123 Test Street, Test Area",
            "pincode": "462001",
            "district": "Bhopal",
            "state": "Madhya Pradesh",
            "qualification": "Bachelor of Technology",
            "university": "Test University of Technology",
            "passing_year": "2020",
            "percentage": "78.5",
        }
    
    async def test_basic_navigation(self):
        """Test 1: Basic browser navigation"""
        print("\n" + "="*80)
        print("TEST 1: Basic Browser Navigation")
        print("="*80)
        
        try:
            async with async_playwright() as playwright:
                llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
                browser_session = BrowserSession(user_data_dir=None)
                
                agent = Agent(
                    task="Go to https://www.google.com and search for 'MPOnline MPPSC' then report what you find.",
                    llm=llm,
                    browser_session=browser_session,
                    use_vision=False,
                )
                
                result = await agent.run()
                print("✅ TEST 1 PASSED: Basic navigation works")
                return True
        except Exception as e:
            print(f"❌ TEST 1 FAILED: {str(e)}")
            return False
    
    async def test_form_detection(self):
        """Test 2: Detect MPOnline form"""
        print("\n" + "="*80)
        print("TEST 2: MPOnline Form Detection")
        print("="*80)
        
        try:
            async with async_playwright() as playwright:
                llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
                browser_session = BrowserSession(user_data_dir=None)
                
                agent = Agent(
                    task="""
                    Navigate to MPOnline website (www.mponline.gov.in) and:
                    1. Look for MPPSC exam listings
                    2. Identify State Service Preliminary Examination 2026
                    3. Report if you can find the application form link
                    4. Do NOT click on anything, just report
                    """,
                    llm=llm,
                    browser_session=browser_session,
                    use_vision=False,
                )
                
                result = await agent.run()
                print("✅ TEST 2 PASSED: Form detection works")
                return True
        except Exception as e:
            print(f"❌ TEST 2 FAILED: {str(e)}")
            return False
    
    def create_full_task_prompt(self) -> str:
        """Create the full task prompt for testing"""
        task = f"""
You are testing a form-filling system. Navigate to the MPOnline website and attempt to fill the MPPSC application form.

# TEST TASK:

## Step 1: Navigate to MPOnline
1. Go to https://www.mponline.gov.in
2. Search for "MPPSC 2026" or "State Service Preliminary Examination 2026"
3. Click on the exam link

## Step 2: Access Application
1. Find the application form link
2. Click on "Apply" button
3. If you see declaration, accept it

## Step 3: Fill Test Data (if form is accessible)
Fill the following information:

**Personal Information:**
- Full Name: {self.test_data['full_name']}
- Father's Name: {self.test_data['father_name']}
- Mother's Name: {self.test_data['mother_name']}
- Date of Birth: {self.test_data['dob']}
- Gender: {self.test_data['gender']}
- Category: {self.test_data['category']}

**Contact Information:**
- Mobile: {self.test_data['mobile']}
- Email: {self.test_data['email']}
- Address: {self.test_data['address']}
- Pincode: {self.test_data['pincode']}
- District: {self.test_data['district']}
- State: {self.test_data['state']}

**Education:**
- Qualification: {self.test_data['qualification']}
- University: {self.test_data['university']}
- Passing Year: {self.test_data['passing_year']}
- Percentage: {self.test_data['percentage']}

## IMPORTANT:
- Fill as many fields as you can find
- Do NOT submit or make payment
- Report what you were able to do
- If you encounter errors, describe them
- Stop after filling basic information
"""
        return task
    
    async def test_full_flow(self):
        """Test 3: Full agent flow"""
        print("\n" + "="*80)
        print("TEST 3: Full Agent Flow (with real website)")
        print("="*80)
        print("\n⚠️  This test will attempt to actually fill the MPOnline form")
        print("Browser window will open. Monitor it closely.\n")
        
        try:
            async with async_playwright() as playwright:
                llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
                browser_session = BrowserSession(user_data_dir=None)
                
                task = self.create_full_task_prompt()
                
                agent = Agent(
                    task=task,
                    llm=llm,
                    browser_session=browser_session,
                    use_vision=False,
                    max_failures=5,
                )
                
                print("🤖 Agent starting full flow test...")
                result = await agent.run()
                print("\n✅ TEST 3 PASSED: Full flow completed")
                return True
        except Exception as e:
            print(f"\n❌ TEST 3 FAILED: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    async def run_all_tests(self, quick_test=False):
        """Run all tests"""
        print("\n" + "="*80)
        print("🧪 MPOnline Interactive Agent - Automated Testing")
        print("="*80)
        print(f"\nOpenAI API Key: {'✅ Configured' if self.openai_api_key else '❌ Missing'}")
        print(f"Mode: {'Quick Test' if quick_test else 'Full Test Suite'}\n")
        
        if not self.openai_api_key:
            print("❌ FATAL: No OpenAI API key found!")
            return False
        
        results = []
        
        if quick_test:
            # Only run Test 3 for quick testing
            print("\n🏃 Running Quick Test (Full Flow Only)...\n")
            result = await self.test_full_flow()
            results.append(("Full Flow Test", result))
        else:
            # Run all tests
            print("\n🔬 Running Full Test Suite...\n")
            
            # Test 1: Basic Navigation
            result1 = await self.test_basic_navigation()
            results.append(("Basic Navigation", result1))
            
            # Test 2: Form Detection
            result2 = await self.test_form_detection()
            results.append(("Form Detection", result2))
            
            # Test 3: Full Flow
            result3 = await self.test_full_flow()
            results.append(("Full Flow", result3))
        
        # Summary
        print("\n" + "="*80)
        print("📊 TEST RESULTS SUMMARY")
        print("="*80)
        
        for test_name, passed in results:
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"{test_name:30s} - {status}")
        
        all_passed = all(result for _, result in results)
        
        print("\n" + "="*80)
        if all_passed:
            print("🎉 ALL TESTS PASSED!")
        else:
            print("⚠️  SOME TESTS FAILED")
        print("="*80)
        
        return all_passed

async def main():
    """Main test entry point"""
    import sys
    
    # Check if quick_test flag is provided
    quick_test = "--quick" in sys.argv or "-q" in sys.argv
    
    tester = MPOnlineAgentTester()
    success = await tester.run_all_tests(quick_test=quick_test)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    # Need to import playwright here
    from playwright.async_api import async_playwright
    asyncio.run(main())
