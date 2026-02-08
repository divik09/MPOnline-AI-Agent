"""
Agentic Browser Agent using LangGraph + browser-use.

This agent:
1. Tries multiple strategies to accomplish a goal
2. Adapts when one approach fails
3. Never gets stuck - always finds alternative routes
4. Uses AI-powered browser control

Based on: https://docs.browser-use.com/introduction
"""
from typing import Dict, Any, List, TypedDict
from langgraph.graph import StateGraph, END
from browser_use import Agent
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from src import config
from src.utils.logging_config import logger


class AgenticBrowserState(TypedDict):
    """State for agentic browser automation."""
    goal: str  # What we're trying to accomplish
    service_type: str  # mppsc, electricity, etc.
    current_strategy: str  # Which strategy we're trying
    attempt_count: int  # How many times we've tried
    strategies_tried: List[str]  # Strategies already attempted
    current_url: str  # Where we are now
    page_content: str  # Current page content
    form_fields_found: List[Dict[str, Any]]  # Fields discovered
    collected_data: Dict[str, Any]  # User data to fill
    errors: List[str]  # Errors encountered
    success: bool  # Whether we succeeded
    next_action: str  # What to do next
    reasoning: str  # Why we're taking this action


class AgenticBrowserAgent:
    """
    Intelligent browser agent that tries multiple strategies.
    """
    
    def __init__(self):
        self.llm = self._get_llm()
        self.browser_controller = None
        
    def _get_llm(self):
        """Get configured LLM for browser-use."""
        if config.LLM_PROVIDER == "openai":
            return ChatOpenAI(model="gpt-4o", temperature=0.1)
        else:
            return ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.1)
    
    async def strategy_google_search(self, state: AgenticBrowserState) -> Dict[str, Any]:
        """
        Strategy 1: Search Google for the service.
        """
        logger.info("agentic_strategy", strategy="google_search", attempt=state['attempt_count'])
        
        service_queries = {
            "mppsc": "MPOnline MPPSC application form official",
            "electricity": "MPOnline electricity bill payment madhya pradesh",
            "university": "MPOnline university admission madhya pradesh"
        }
        
        query = service_queries.get(state['service_type'], f"MPOnline {state['service_type']}")
        
        try:
            task = f"""
            1. Go to google.com
            2. Search for: "{query}"
            3. Look for results from mponline.gov.in
            4. Click on the official MPOnline link
            5. Navigate to the application or service page
            6. Stop when you see a form or application page
            """
            
            agent = Agent(task=task, llm=self.llm)
            result = await agent.run()
            
            return {
                "current_strategy": "google_search",
                "strategies_tried": state['strategies_tried'] + ["google_search"],
                "attempt_count": state['attempt_count'] + 1,
                "success": True,
                "next_action": "discover_fields",
                "reasoning": "Successfully found page via Google search"
            }
            
        except Exception as e:
            logger.error("agentic_strategy_failed", strategy="google_search", error=str(e))
            return {
                "current_strategy": "google_search",
                "strategies_tried": state['strategies_tried'] + ["google_search"],
                "attempt_count": state['attempt_count'] + 1,
                "errors": state['errors'] + [f"Google search failed: {str(e)}"],
                "success": False,
                "next_action": "try_next_strategy",
                "reasoning": "Google search approach didn't work, trying alternative"
            }
    
    async def strategy_direct_url(self, state: AgenticBrowserState) -> Dict[str, Any]:
        """
        Strategy 2: Navigate directly to known URL.
        """
        logger.info("agentic_strategy", strategy="direct_url", attempt=state['attempt_count'])
        
        direct_urls = {
            "mppsc": "https://www.mponline.gov.in/Portal/Examinations/MPPSC/",
            "electricity": "https://www.mponline.gov.in/Portal/Services/MPEDC/Home.aspx",
            "university": "https://www.mponline.gov.in/Portal/Services/Universities/Home.aspx"
        }
        
        url = direct_urls.get(state['service_type'], "https://www.mponline.gov.in")
        
        try:
            task = f"""
            1. Navigate to: {url}
            2. Wait for the page to load completely
            3. Look for application or registration link
            4. Click on it to reach the form
            5. Stop when you see a form
            """
            
            agent = Agent(task=task, llm=self.llm)
            result = await agent.run()
            
            return {
                "current_strategy": "direct_url",
                "strategies_tried": state['strategies_tried'] + ["direct_url"],
                "attempt_count": state['attempt_count'] + 1,
                "success": True,
                "next_action": "discover_fields",
                "reasoning": "Successfully navigated directly to service URL"
            }
            
        except Exception as e:
            logger.error("agentic_strategy_failed", strategy="direct_url", error=str(e))
            return {
                "current_strategy": "direct_url",
                "strategies_tried": state['strategies_tried'] + ["direct_url"],
                "attempt_count": state['attempt_count'] + 1,
                "errors": state['errors'] + [f"Direct URL failed: {str(e)}"],
                "success": False,
                "next_action": "try_next_strategy",
                "reasoning": "Direct URL approach failed, exploring site navigation"
            }
    
    async def strategy_explore_portal(self, state: AgenticBrowserState) -> Dict[str, Any]:
        """
        Strategy 3: Start at homepage and intelligently explore.
        """
        logger.info("agentic_strategy", strategy="explore_portal", attempt=state['attempt_count'])
        
        try:
            task = f"""
            1. Go to https://www.mponline.gov.in
            2. Look at the homepage carefully
            3. Find navigation menu or links related to "{state['service_type']}"
            4. Click through the navigation intelligently
            5. Look for keywords: application, registration, form, {state['service_type']}
            6. Keep exploring until you find a form page
            7. Don't give up easily - try different menu items
            """
            
            agent = Agent(task=task, llm=self.llm)
            result = await agent.run()
            
            return {
                "current_strategy": "explore_portal",
                "strategies_tried": state['strategies_tried'] + ["explore_portal"],
                "attempt_count": state['attempt_count'] + 1,
                "success": True,
                "next_action": "discover_fields",
                "reasoning": "Successfully found form by exploring portal navigation"
            }
            
        except Exception as e:
            logger.error("agentic_strategy_failed", strategy="explore_portal", error=str(e))
            return {
                "current_strategy": "explore_portal",
                "strategies_tried": state['strategies_tried'] + ["explore_portal"],
                "attempt_count": state['attempt_count'] + 1,
                "errors": state['errors'] + [f"Portal exploration failed: {str(e)}"],
                "success": False,
                "next_action": "try_next_strategy",
                "reasoning": "Exploration strategy didn't work, trying search engines"
            }
    
    async def strategy_alternative_search(self, state: AgenticBrowserState) -> Dict[str, Any]:
        """
        Strategy 4: Try DuckDuckGo or Bing as alternative search.
        """
        logger.info("agentic_strategy", strategy="alternative_search", attempt=state['attempt_count'])
        
        try:
            task = f"""
            1. Go to duckduckgo.com
            2. Search for: "MPOnline {state['service_type']} application site:mponline.gov.in"
            3. Click on relevant results
            4. Navigate to the form page
            5. Keep trying different links until you find a form
            """
            
            agent = Agent(task=task, llm=self.llm)
            result = await agent.run()
            
            return {
                "current_strategy": "alternative_search",
                "strategies_tried": state['strategies_tried'] + ["alternative_search"],
                "attempt_count": state['attempt_count'] + 1,
                "success": True,
                "next_action": "discover_fields",
                "reasoning": "Found page using alternative search engine"
            }
            
        except Exception as e:
            logger.error("agentic_strategy_failed", strategy="alternative_search", error=str(e))
            return {
                "current_strategy": "alternative_search",
                "strategies_tried": state['strategies_tried'] + ["alternative_search"],
               "attempt_count": state['attempt_count'] + 1,
                "errors": state['errors'] + [f"Alternative search failed: {str(e)}"],
                "success": False,
                "next_action": "exhausted",
                "reasoning": "All strategies exhausted"
            }
    
    async def discover_form_fields(self, state: AgenticBrowserState) -> Dict[str, Any]:
        """
        Intelligent form field discovery using AI.
        """
        logger.info("agentic_action", action="discover_fields")
        
        try:
            task = """
            Analyze the current page and identify all form fields.
            For each field, note:
            1. The field name or ID
            2. The label text
            3. Whether it's required
            4. What type of input it expects
            
            List all the fields you find.
            """
            
            agent = Agent(task=task, llm=self.llm)
            result = await agent.run()
            
            # Parse result to extract fields (simplified)
            # In real implementation, we'd parse the AI's response
            
            return {
                "form_fields_found": [],  # Would be populated from AI response
                "next_action": "fill_form",
                "reasoning": "Discovered form fields, ready to fill"
            }
            
        except Exception as e:
            logger.error("agentic_field_discovery_failed", error=str(e))
            return {
                "errors": state['errors'] + [f"Field discovery failed: {str(e)}"],
                "next_action": "retry",
                "reasoning": "Field discovery failed, will retry"
            }
    
    async def fill_form_intelligently(self, state: AgenticBrowserState) -> Dict[str, Any]:
        """
        Use AI to fill form fields intelligently.
        """
        logger.info("agentic_action", action="fill_form")
        
        try:
            # Build natural language instructions for filling
            data_description = "\n".join([
                f"- {key.replace('_', ' ').title()}: {value}"
                for key, value in state['collected_data'].items()
            ])
            
            task = f"""
            Fill out the form on this page with the following information:
            
            {data_description}
            
            Instructions:
            1. Find each field that matches the data above
            2. Fill it in carefully
            3. For dropdowns, select the matching option
            4. Skip fields that don't have corresponding data
            5. Do NOT submit the form yet
            6. Take your time and be accurate
            """
            
            agent = Agent(task=task, llm=self.llm)
            result = await agent.run()
            
            return {
                "success": True,
                "next_action": "complete",
                "reasoning": "Successfully filled all form fields"
            }
            
        except Exception as e:
            logger.error("agentic_form_fill_failed", error=str(e))
            return {
                "errors": state['errors'] + [f"Form filling failed: {str(e)}"],
                "next_action": "retry",
                "reasoning": "Form filling failed, will retry"
            }
    
    def create_graph(self) -> StateGraph:
        """
        Create LangGraph workflow for agentic browser automation.
        """
        workflow = StateGraph(AgenticBrowserState)
        
        # Define routing logic
        def route_strategy(state: AgenticBrowserState) -> str:
            """Decide which strategy to try next."""
            tried = state.get('strategies_tried', [])
            
            # Try strategies in order, skipping already tried ones
            if "google_search" not in tried:
                return "google_search"
            elif "direct_url" not in tried:
                return "direct_url"
            elif "explore_portal" not in tried:
                return "explore_portal"
            elif "alternative_search" not in tried:
                return "alternative_search"
            else:
                return "exhausted"
        
        def route_after_strategy(state: AgenticBrowserState) -> str:
            """Route based on strategy success."""
            if state.get('success'):
                return "discover_fields"
            else:
                next_action = state.get('next_action')
                if next_action == "try_next_strategy":
                    return "router"
                elif next_action == "exhausted":
                    return "exhausted"
                else:
                    return "router"
        
        # Add nodes
        workflow.add_node("router", lambda s: s)  # Decision point
        workflow.add_node("google_search", self.strategy_google_search)
        workflow.add_node("direct_url", self.strategy_direct_url)
        workflow.add_node("explore_portal", self.strategy_explore_portal)
        workflow.add_node("alternative_search", self.strategy_alternative_search)
        workflow.add_node("discover_fields", self.discover_form_fields)
        workflow.add_node("fill_form", self.fill_form_intelligently)
        workflow.add_node("exhausted", lambda s: {**s, "success": False, "reasoning": "All strategies exhausted"})
        
        # Set entry point
        workflow.set_entry_point("router")
        
        # Add routing edges
        workflow.add_conditional_edges(
            "router",
            route_strategy,
            {
                "google_search": "google_search",
                "direct_url": "direct_url",
                "explore_portal": "explore_portal",
                "alternative_search": "alternative_search",
                "exhausted": "exhausted"
            }
        )
        
        # Each strategy routes based on success
        for strategy in ["google_search", "direct_url", "explore_portal", "alternative_search"]:
            workflow.add_conditional_edges(
                strategy,
                route_after_strategy,
                {
                    "discover_fields": "discover_fields",
                    "router": "router",
                    "exhausted": "exhausted"
                }
            )
        
        # After discovering fields, fill form
        workflow.add_edge("discover_fields", "fill_form")
        
        # Fill form can succeed or retry
        workflow.add_conditional_edges(
            "fill_form",
            lambda s: END if s.get('success') else "router",
            {
                END: END,
                "router": "router"
            }
        )
        
        # Exhausted ends the workflow
        workflow.add_edge("exhausted", END)
        
        return workflow.compile()
    
    async def run(self, goal: str, service_type: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the agentic browser automation.
        
        Args:
            goal: What we're trying to accomplish
            service_type: Type of service (mppsc, electricity, etc.)
            user_data: Data to fill in the form
            
        Returns:
            Final state after completion
        """
        # Create initial state
        initial_state: AgenticBrowserState = {
            "goal": goal,
            "service_type": service_type,
            "current_strategy": "",
            "attempt_count": 0,
            "strategies_tried": [],
            "current_url": "",
            "page_content": "",
            "form_fields_found": [],
            "collected_data": user_data,
            "errors": [],
            "success": False,
            "next_action": "start",
            "reasoning": "Starting agentic browser automation"
        }
        
        # Create and run graph
        graph = self.create_graph()
        
        logger.info("agentic_browser_starting", goal=goal, service=service_type)
        
        final_state = await graph.ainvoke(initial_state)
        
        logger.info("agentic_browser_completed", 
                   success=final_state.get('success'),
                   attempts=final_state.get('attempt_count'),
                   strategies_tried=final_state.get('strategies_tried'))
        
        return final_state
