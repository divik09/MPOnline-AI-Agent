"""
Visual Demo: Watch the AI Agent Search in Browser!

This will open a browser window where you can SEE the agent working.
"""
import asyncio
from browser_use import Agent
from src.utils.browser_use_helper import get_configured_llm
import time


async def visual_search_demo():
    """
    Opens browser and shows AI searching for MPPSC.
    You'll see every action the AI takes!
    """
    
    print("\n" + "=" * 80)
    print("🎬 VISUAL BROWSER DEMO - Watch the AI Agent Work!")
    print("=" * 80)
    
    print("\n📋 What you'll see:")
    print("   1. Browser window opens (you can watch!)")
    print("   2. AI navigates to Google")
    print("   3. AI types search query")
    print("   4. AI clicks search")
    print("   5. AI finds and clicks MPOnline link")
    print("\n" + "-" * 80)
    
    input("\n👉 Press ENTER to watch the AI agent in action...")
    
    print("\n🤖 Initializing AI Agent...")
    llm = get_configured_llm()
    print(f"✅ LLM Ready: {llm.__class__.__name__}")
    
    print("\n🌐 Opening browser window...")
    print("   (A Chrome window should appear - watch it!)\n")
    
    # Task for the AI agent
    task = """
    I want you to search for MPOnline MPPSC on Google.
    
    Steps:
    1. Go to google.com
    2. Find the search box
    3. Type "MPOnline MPPSC official website"
    4. Click the search button or press enter
    5. Look at the search results
    6. Find the link from mponline.gov.in
    7. Click on it
    8. Stop when you reach the MPOnline website
    
    Take your time and do each step carefully.
    """
    
    print("🎯 Task assigned to AI:")
    print("   'Search Google for MPOnline MPPSC and open official site'\n")
    
    print("⏳ AI is now working... (watch the browser window!)")
    print("   You'll see the AI:")
    print("   • Navigate to pages")
    print("   • Click on elements")
    print("   • Type in search boxes")
    print("   • Make intelligent decisions")
    
    print("\n" + "=" * 80)
    print("🔴 BROWSER WINDOW IS NOW ACTIVE - WATCH IT!")
    print("=" * 80 + "\n")
    
    start_time = time.time()
    
    try:
        # Create and run the agent
        agent = Agent(
            task=task,
            llm=llm,
        )
        
        result = await agent.run()
        
        duration = time.time() - start_time
        
        print("\n" + "=" * 80)
        print("✅ AI AGENT COMPLETED!")
        print("=" * 80)
        
        print(f"\n⏱️  Time Taken: {duration:.1f} seconds")
        print(f"🎯 Task: Successfully searched and navigated to MPOnline")
        
        print("\n📊 What the AI did:")
        print("   ✓ Opened Google")
        print("   ✓ Searched for 'MPOnline MPPSC'")
        print("   ✓ Identified official link")
        print("   ✓ Clicked and navigated to site")
        
        print("\n💡 The browser window is still open!")
        print("   You can see where the AI navigated to.")
        
        print("\n" + "=" * 80)
        
        input("\nPress ENTER to close the browser and finish...")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print("\nPossible issues:")
        print("  1. API key not configured in .env")
        print("  2. browser-use not installed correctly")
        print("  3. Chrome browser not available")
        
        import traceback
        print("\nFull error:")
        traceback.print_exc()
        
        return False


def main():
    """Main entry point."""
    print("\n🎬 Visual Browser Agent Demo")
    print("   Watch the AI search and navigate in real-time!\n")
    
    success = asyncio.run(visual_search_demo())
    
    if success:
        print("\n✅ Demo completed successfully!")
        print("\n💡 Next Steps:")
        print("   • Try the Streamlit app at http://localhost:8505")
        print("   • Say 'I want to apply for MPPSC'")
        print("   • Watch the agentic multi-strategy automation!")
    else:
        print("\n⚠️  Demo encountered issues")
        print("   Please check the error messages above")
    
    return success


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏸️  Demo stopped by user")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
