"""
Interactive Browser Agent Test Script
Automated testing wrapper for the interactive agent
"""

import asyncio
from interactive_browser_agent import InteractiveBrowserAgent

async def test_mppsc_flow():
    """Test the MPPSC form filling flow with the interactive agent"""
    
    agent = InteractiveBrowserAgent()
    
    print("\n" + "="*90)
    print("🧪 TESTING INTERACTIVE BROWSER AGENT - MPPSC FLOW")
    print("="*90 + "\n")
    
    # Start the agent
    await agent.run_interactive_session()

if __name__ == "__main__":
    asyncio.run(test_mppsc_flow())
