"""
Interactive Browser-Use Search Assistant
Based on: https://docs.browser-use.com/quickstart

Ask any question and the AI will search the web to find the answer!
"""
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import sys

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

class SearchAssistant:
    """AI-powered search assistant using browser-use."""
    
    def __init__(self):
        self.llm = BrowserUseChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.search_history = []
    
    async def search(self, command: str) -> str:
        """
        Search the web for information based on user command.
        
        Args:
            command: User's question or search request
            
        Returns:
            Result summary
        """
        print(f"\n🔍 Processing: {command}")
        print("📺 Opening browser...")
        
        # Create intelligent task based on command
        task = self._create_task(command)
        
        print(f"🤖 Task: {task}\n")
        print("⏳ AI is working... (watch the browser window!)\n")
        
        try:
            # Run the agent
            agent = Agent(task=task, llm=self.llm)
            result = await agent.run()
            
            # Save to history
            self.search_history.append({
                "command": command,
                "task": task,
                "success": True
            })
            
            print("\n✅ Search completed!")
            return "Search successful - check browser window for results"
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            self.search_history.append({
                "command": command,
                "task": task,
                "success": False,
                "error": str(e)
            })
            return f"Search failed: {e}"
    
    def _create_task(self, command: str) -> str:
        """
        Convert user command into a specific browser task.
        
        Args:
            command: User's natural language command
            
        Returns:
            Detailed task for the agent
        """
        command_lower = command.lower()
        
        # Detect intent and create appropriate task
        if "find" in command_lower or "search" in command_lower:
            return f"Go to Google and search for: {command}. Show me the top results."
        
        elif "website" in command_lower or "official" in command_lower:
            return f"Find the official website for: {command}. Navigate to it and show me the homepage."
        
        elif "news" in command_lower or "latest" in command_lower:
            return f"Search for the latest news about: {command}. Show me recent articles."
        
        elif "how to" in command_lower or "tutorial" in command_lower:
            return f"Search for tutorials/guides on: {command}. Find helpful resources."
        
        elif "price" in command_lower or "cost" in command_lower:
            return f"Search for pricing information on: {command}. Compare options if available."
        
        else:
            # General search
            return f"Search the web for: {command}. Provide relevant information."
    
    def show_history(self):
        """Display search history."""
        if not self.search_history:
            print("\n📝 No search history yet")
            return
        
        print("\n📝 Search History:")
        print("=" * 60)
        for i, item in enumerate(self.search_history, 1):
            status = "✅" if item['success'] else "❌"
            print(f"{i}. {status} {item['command']}")
        print("=" * 60)


async def interactive_mode():
    """Run interactive search assistant."""
    
    print("\n" + "=" * 60)
    print("🤖 Browser-Use Interactive Search Assistant")
    print("=" * 60)
    print("\n💡 Ask me anything and I'll search the web!")
    print("\nCommands:")
    print("  • Type your question/command")
    print("  • 'history' - Show search history")
    print("  • 'quit' or 'exit' - Exit program")
    print("\n" + "=" * 60)
    
    assistant = SearchAssistant()
    
    while True:
        try:
            command = input("\n❓ What would you like to search for? ").strip()
            
            if not command:
                continue
            
            if command.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if command.lower() == 'history':
                assistant.show_history()
                continue
            
            # Perform search
            await assistant.search(command)
            
        except KeyboardInterrupt:
            print("\n\n⏸️  Interrupted")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


async def single_search_mode(command: str):
    """Run a single search and exit."""
    
    print("\n🤖 Browser-Use Search Assistant")
    print("=" * 60)
    
    assistant = SearchAssistant()
    await assistant.search(command)
    
    input("\nPress ENTER to exit...")


async def main():
    """Main entry point."""
    
    if len(sys.argv) > 1:
        # Single search mode with command from arguments
        command = " ".join(sys.argv[1:])
        await single_search_mode(command)
    else:
        # Interactive mode
        await interactive_mode()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏸️  Bye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
