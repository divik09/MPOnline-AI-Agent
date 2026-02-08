"""
LangGraph Browser-Use Agent with Retry Logic

This script demonstrates a robust browser automation agent that:
1. Uses LangGraph to manage state and retries
2. Automatically retries if the browser agent fails
3. Shows ALL browser activity (Headful mode)
4. Uses GPT-4o for reliable instruction following

Based on: https://docs.browser-use.com/
"""
import asyncio
import os
from typing import TypedDict, Annotated, List, Union
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
from pydantic import Field
import operator

# Load environment variables
load_dotenv()

# --- 1. Define LLM Wrapper (Fix for browser-use compatibility) ---
class BrowserUseChatOpenAI(ChatOpenAI):
    provider: str = Field(default="openai")
    
    class Config:
        extra = "allow"
        
    @property
    def model(self):
        return self.model_name

# --- 2. Define State ---
class AgentState(TypedDict):
    task: str
    attempt_count: int
    max_attempts: int
    success: bool
    last_result: str
    messages: List[str]

# --- 3. Define Nodes ---

from playwright.async_api import async_playwright

async def search_node(state: AgentState):
    """
    Executes the browser-use agent search with visible browser.
    """
    attempt = state["attempt_count"] + 1
    print(f"\n🚀 Attempt {attempt}/{state['max_attempts']} starting...")
    
    # Initialize LLM
    llm = BrowserUseChatOpenAI(model="gpt-4o", temperature=0)
    
    # Launch Headful Browser
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    
    try:
        agent = Agent(
            task=state["task"],
            llm=llm,
            browser_context=context,
        )
        
        print("📺 Opening browser window... (Watch it!)")
        result = await agent.run()
        
        final_output = str(result)
        print(f"✅ Attempt {attempt} completed successfully!")
        
        # Cleanup
        await context.close()
        await browser.close()
        await playwright.stop()
        
        return {
            "attempt_count": attempt,
            "success": True,
            "last_result": final_output,
            "messages": [f"Attempt {attempt} succeeded"]
        }
        
    except Exception as e:
        print(f"❌ Attempt {attempt} failed: {str(e)}")
        # Cleanup on failure
        await context.close()
        await browser.close()
        await playwright.stop()
        
        return {
            "attempt_count": attempt,
            "success": False,
            "last_result": str(e),
            "messages": [f"Attempt {attempt} failed: {str(e)}"]
        }

def check_result(state: AgentState) -> str:
    """
    Decides whether to retry or end.
    """
    if state["success"]:
        return "end"
    
    if state["attempt_count"] >= state["max_attempts"]:
        print("\n⚠️  Max attempts reached. Stopping.")
        return "end"
    
    print("\n🔄 Retrying...")
    return "retry"

# --- 4. Build Graph ---
def create_retry_graph():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("search", search_node)
    
    # Set entry point
    workflow.set_entry_point("search")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "search",
        check_result,
        {
            "end": END,
            "retry": "search"
        }
    )
    
    return workflow.compile()

# --- 5. Main Execution ---
async def main():
    print("\n" + "=" * 60)
    print("🤖 LangGraph Resilient Browser Agent")
    print("=" * 60)
    print("This agent will try to perform your task.")
    print("If it fails, it will automatically retry up to 3 times.")
    print("You will see the browser open and perform actions.")
    
    # Get user input
    user_task = input("\n❓ What should the agent do? (e.g. 'Search for MPOnline MPPSC') ")
    
    if not user_task.strip():
        user_task = "Search Google for 'MPOnline MPPSC official website' and click the result."
        print(f"Using default task: {user_task}")
    
    # Initial state
    initial_state = {
        "task": user_task,
        "attempt_count": 0,
        "max_attempts": 3,
        "success": False,
        "last_result": "",
        "messages": []
    }
    
    # Create graph
    app = create_retry_graph()
    
    # Run graph
    print("\n🏁 Starting Workflow...")
    async for output in app.astream(initial_state):
        pass # We print inside the nodes
        
    print("\n" + "=" * 60)
    print("🏁 Workflow Finished")
    print("=" * 60)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏸️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
