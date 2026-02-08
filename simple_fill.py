"""
Simple MPPSC Form Reader and Filler
Direct approach - reads current page state and fills the form
"""
import asyncio
import os
from dotenv import load_dotenv
from browser_use import Agent, BrowserSession
from browser_use.llm.openai.chat import ChatOpenAI

load_dotenv()

async def main():
    """Simple form filler"""
    
    print("\n" + "="*80)
    print("📝 MPPSC Form Filler - Simple Version")
    print("="*80)
    print("\n🎯 Task: Navigate MPOnline and fill MPPSC form")
    print("🌐 Vision: Enabled for Hindi/English reading")
    print("⚡ Mode: Quick and efficient\n")
    
    async with async_playwright() as playwright:
        # Initialize
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)  # Using mini for faster response
        browser_session = BrowserSession(user_data_dir=None)
        
        # Simple task
        task = """
Go to MPOnline website and complete the MPPSC application form.

Steps:
1. Navigate to https://www.mponline.gov.in
2. Find "MPPSC" or "State Service Exam 2026"
3. Click to open the application
4. Accept any declarations
5. Fill form with test data:
   - Name: Test Candidate
   - Father: Test Father  
   - Mobile: 9876543210
   - Email: test@example.com
6. Fill all visible fields
7. DO NOT submit or pay - stop before payment

Work quickly. Use vision to read Hindi/English text.
"""
        
        agent = Agent(
            task=task,
            llm=llm,
            browser_session=browser_session,
            use_vision=False,  # Disable vision to avoid quota issues
            max_failures=5,
        )
        
        print("🚀 Starting agent...\n")
        
        try:
            result = await agent.run()
            print("\n✅ Agent completed!")
            print("📺 Check browser window for results")
            
        except Exception as e:
            print(f"\n⚠️ Error: {str(e)}")
            print("💡 Check browser window - partial progress may be visible")

if __name__ == "__main__":
    from playwright.async_api import async_playwright
    asyncio.run(main())
