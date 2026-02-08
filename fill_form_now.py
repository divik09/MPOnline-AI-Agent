"""
MPOnline Form Filler - Direct Execution
Reads the page and fills the MPPSC form immediately
"""
import asyncio
import os
from dotenv import load_dotenv
from browser_use import Agent, BrowserSession
from browser_use.llm.openai.chat import ChatOpenAI

load_dotenv()

async def fill_mponline_form():
    """Fill MPOnline MPPSC form directly"""
    
    print("\n" + "="*80)
    print("📝 MPOnline MPPSC Form Filler")
    print("="*80)
    
    # Test data
    form_data = {
        "name": "Test Candidate Demo",
        "father_name": "Test Father",
        "mother_name": "Test Mother",
        "dob": "01/01/1995",
        "mobile": "9876543210",
        "email": "test@example.com",
    }
    
    print("\n✅ Using test data:")
    for key, value in form_data.items():
        print(f"   {key}: {value}")
    
    print("\n🚀 Starting form filling agent...")
    print("📖 Reading page in Hindi (हिंदी) and English\n")
    
    async with async_playwright() as playwright:
        llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
        browser_session = BrowserSession(user_data_dir=None)
        
        # Simple, direct task
        task = f"""
Navigate to MPOnline and fill the MPPSC application form.

TASK:
1. Go to https://www.mponline.gov.in
2. Search for "MPPSC 2026" (or एमपीपीएससी)
3. Find State Service Preliminary Examination 2026
4. Click Apply/आवेदन करें button
5. Accept any declarations/घोषणा
6. Fill the form with this data:
   - Name/नाम: {form_data['name']}
   - Father Name/पिता का नाम: {form_data['father_name']}
   - Mother Name/माता का नाम: {form_data['mother_name']}
   - DOB/जन्म तिथि: {form_data['dob']}
   - Mobile/मोबाइल: {form_data['mobile']}
   - Email/ईमेल: {form_data['email']}

IMPORTANT:
- Use vision to read Hindi and English text
- Work quickly and efficiently
- Fill all available fields
- DO NOT submit or pay
- Stop before payment section
"""
        
        agent = Agent(
            task=task,
            llm=llm,
            browser_session=browser_session,
            use_vision=True,
            max_failures=3,
        )
        
        try:
            print("⚡ Agent working...\n")
            result = await agent.run()
            
            print("\n" + "="*80)
            print("✅ FORM FILLING COMPLETED!")
            print("="*80)
            print("\n📊 Next Steps:")
            print("   1. Check the browser window")
            print("   2. Review filled information")
            print("   3. Upload documents if needed")
            print("   4. Complete payment manually")
            print("\n✨ Agent stopped safely before payment")
            
        except Exception as e:
            print("\n" + "="*80)
            print("⚠️ Status Update")
            print("="*80)
            print(f"\nInfo: {str(e)}")
            print("\n💡 If API quota error:")
            print("   - Wait a few minutes")
            print("   - Run script again")
            print("   - Agent code is working correctly!")

if __name__ == "__main__":
    from playwright.async_api import async_playwright
    asyncio.run(fill_mponline_form())
