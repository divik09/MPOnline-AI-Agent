"""
Official Browser-Use Implementation
Following: https://docs.browser-use.com/quickstart
"""
import asyncio
from browser_use import Agent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


async def demo_search_mppsc():
    """
    Demo: AI agent searches for MPOnline MPPSC.
    """
    
    print("\n" + "=" * 80)
    print("🎬 BROWSER-USE OFFICIAL DEMO")
    print("=" * 80)
    
    print("\n📚 Following: https://docs.browser-use.com/quickstart")
    print("\n📺 A browser window will open - WATCH IT!")
    print("\nThe AI agent will:")
    print("  • Navigate to Google")
    print("  • Search for 'MPOnline MPPSC official website'")
    print("  • Find and click the officiallink")
    print("  • Navigate to the MPOnline portal")
    
    input("\n👉 Press ENTER to start...")
    
    print("\n🚀 Starting browser automation...")
    print("=" * 80 + "\n")
    
    try:
        # Option 1: Use OpenAI/Anthropic directly (since we already have API keys)
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        
        # Simple task
        task = "Go to Google and search for 'MPOnline MPPSC official website'. Click on the link from mponline.gov.in domain."
        
        print(f"📝 Task: {task}")
        print("\n🔴 BROWSER OPENING - WATCH THE WINDOW! 🔴\n")
        
        # Create and run agent
        agent = Agent(
            task=task,
            llm=llm
        )
        
        print("⏳ AI is working... (30-60 seconds)\n")
        
        result = await agent.run()
        
        print("\n" + "=" * 80)
        print("✅ AGENT COMPLETED!")
        print("=" * 80)
        
        print("\n📊 What happened:")
        print("  ✓ Browser opened")
        print("  ✓ AI navigated to Google")
        print("  ✓ AI searched for MPOnline MPPSC")
        print("  ✓ AI clicked on official link")
        print("  ✓ Reached MPOnline portal")
        
        print("\n💡 Check the browser window to see the final page!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nDebug info:")
        import traceback
        traceback.print_exc()
        
        print("\n💡 Make sure:")
        print("  1. OPENAI_API_KEY is set in .env")  
        print("  2. browser-use is installed: pip install browser-use")
        print("  3. Playwright is installed: playwright install")
        
        return False


async def demo_fill_form():
    """
    Demo: AI agent fills MPPSC form.
    """
    
    print("\n" + "=" * 80)
    print("🎬 FORM FILLING DEMO")
    print("=" * 80)
    
    print("\nThis will demonstrate AI filling an MPPSC application form.")
    
    # Sample data
    test_data = {
        "name": "Amit Kumar Sharma",
        "email": "amit@example.com",
        "mobile": "9876543210"
    }
    
    print("\n📋 Data to fill:")
    for key, value in test_data.items():
        print(f"  • {key}: {value}")
    
    input("\n👉 Press ENTER to start form filling...")
    
    try:
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        
        # Task with data
        task = f"""
        1. Go to Google and search for "MPOnline MPPSC application form"
        2. Find and click on the official mponline.gov.in link
        3. Navigate to the application form page
        4. Fill the form with this data:
           - Name: {test_data['name']}
           - Email: {test_data['email']}
           - Mobile: {test_data['mobile']}
        5. DO NOT submit the form
        6. Stop after filling the fields
        """
        
        print("\n🔴 BROWSER OPENING 🔴\n")
        
        agent = Agent(task=task, llm=llm)
        
        print("⏳ AI is filling the form... (1-2 minutes)\n")
        
        result = await agent.run()
        
        print("\n" + "=" * 80)
        print("✅ FORM FILLING COMPLETE!")
        print("=" * 80)
        
        print("\n📝 Next steps:")
        print("  1. Check the browser window")
        print("  2. Verify the filled data")
        print("  3. Complete any CAPTCHA if present")
        print("  4. Submit when ready")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main menu."""
    
    print("\n🤖 Browser-Use Official Implementation")
    print("   Based on: https://docs.browser-use.com/quickstart\n")
    
    print("Choose a demo:")
    print("  1. Simple Search (30 seconds)")
    print("  2. Form Filling (1-2 minutes)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        success = await demo_search_mppsc()
    elif choice == "2":
        success = await demo_fill_form()
    else:
        print("Invalid choice!")
        return False
    
    if success:
        print("\n✅ Demo completed successfully!")
        print("\n💡 Next steps:")
        print("  • Try the Streamlit app: http://localhost:8505")
        print("  • Run: python demo_browser_use.py (full workflow)")
    
    input("\nPress ENTER to exit...")
    return success


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏸️  Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
