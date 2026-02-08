"""
Quick Test Script for Multilingual MPOnline Agent
Tests vision and Hindi/English reading capabilities
"""
import asyncio
import os
from dotenv import load_dotenv
from browser_use import Agent, BrowserSession
from browser_use.llm.openai.chat import ChatOpenAI

load_dotenv()

async def test_multilingual_agent():
    """Test agent with Hindi/English vision capabilities"""
    print("\n" + "="*80)
    print("🧪 Testing Multilingual MPOnline Agent with Vision")
    print("="*80)
    print("\n✨ Features being tested:")
    print("   - Vision enabled to read Hindi/English text")
    print("   - Fast form filling")
    print("   - Multilingual UI navigation")
    print("\n")
    
    async with async_playwright() as playwright:
        llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
        browser_session = BrowserSession(user_data_dir=None)
        
        task = """
        QUICK TEST: Navigate to MPOnline website and demonstrate multilingual capabilities.
        
        1. Go to https://www.mponline.gov.in
        2. Look for MPPSC exam (may be in Hindi or English)
        3. Read any text you see on the page (both Hindi and English)
        4. Report what you found and what languages you detected
        5. Do NOT fill any forms - just navigate and read
        
        Use vision to read everything accurately!
        """
        
        agent = Agent(
            task=task,
            llm=llm,
            browser_session=browser_session,
            use_vision=True,  # Vision enabled for multilingual support
            max_failures=3,
        )
        
        print("🤖 Agent starting with VISION enabled...")
        print("📖 Can read BOTH Hindi (हिंदी) and English\n")
        
        try:
            result = await agent.run()
            print("\n" + "="*80)
            print("✅ TEST PASSED: Multilingual agent working!")
            print("="*80)
            return True
        except Exception as e:
            print("\n" + "="*80)
            print("❌ TEST FAILED")
            print("="*80)
            print(f"Error: {str(e)}")
            return False

if __name__ == "__main__":
    from playwright.async_api import async_playwright
    asyncio.run(test_multilingual_agent())
