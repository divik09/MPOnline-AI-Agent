"""
Simple Browser-Use Example
Based on: https://docs.browser-use.com/quickstart

This will search for any topic you specify and show you the results.
"""
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


from pydantic import Field

class BrowserUseChatOpenAI(ChatOpenAI):
    provider: str = Field(default="openai")
    
    class Config:
        extra = "allow"
        
    @property
    def model(self):
        return self.model_name

async def search_web(query: str):
    """
    Use AI to search the web and find information.
    
    Args:
        query: What to search for
    """
    
    print(f"\n🔍 Searching for: {query}")
    print("📺 Browser window will open - watch the AI work!\n")
    
    # Initialize LLM
    llm = BrowserUseChatOpenAI(model="gpt-4o", temperature=0)
    
    # Create task
    task = f"Search Google for '{query}' and tell me what you find."
    
    print("🤖 AI is working...")
    print("=" * 60)
    
    # Create and run agent
    agent = Agent(task=task, llm=llm)
    
    try:
        result = await agent.run()
        
        print("\n" + "=" * 60)
        print("✅ Search complete!")
        print("=" * 60)
        print("\n💡 Check the browser window to see what the AI found.")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


async def main():
    """Main function."""
    
    print("\n" + "=" * 60)
    print("🤖 Browser-Use Simple Search Example")
    print("=" * 60)
    print("\nThis AI will search the web for anything you ask!")
    
    # Example search
    query = input("\n❓what is mppsc how to apply for exam ")
    
    if query.strip():
        await search_web(query)
    else:
        print("\n⚠️  No query provided. Using example...")
        await search_web("MPOnline MPPSC official website")
    
    input("\n\nPress ENTER to exit...")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏸️  Interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
