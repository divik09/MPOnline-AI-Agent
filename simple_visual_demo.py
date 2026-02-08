"""
Simple Visual Browser Demo - Watch AI Search Google!
No complex dependencies - just pure browser-use demonstration.
"""
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()


async def demo():
    """Simple demo showing browser search."""
    
    print("\n" + "=" * 80)
    print("🎬 WATCH THE AI SEARCH IN BROWSER!")
    print("=" * 80)
    
    print("\n📺 A browser window will open - WATCH IT!")
    print("   You'll see the AI:")
    print("   • Navigate to Google")
    print("   • Type a search query  ")
    print("   • Click search")
    print("   • Find and click results")
    
    input("\n👉 Press ENTER to start the demo...")
    
    print("\n🚀 Starting browser automation...\n")
    
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0.1)
    
    # Simple task
    task = """
    Go to Google and search for "MPOnline MPPSC official website".
    Click on the first result from mponline.gov.in domain.
    Stop when you reach the MPOnline website.
    """
    
    print("🤖 AI Task: Search Google for MPOnline MPPSC")
    print("\n🔴 BROWSER OPENING - WATCH NOW!\n")
    
    # Run agent
    agent = Agent(task=task, llm=llm)
    result = await agent.run()
    
    print("\n✅ AI completed the search!")
    print("   Check the browser window to see where it navigated.\n")
    
    input("Press ENTER to close...")
    
    return result


if __name__ == "__main__":
    try:
        asyncio.run(demo())
        print("\n✅ Demo complete!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure OPENAI_API_KEY is set in your .env file!")
