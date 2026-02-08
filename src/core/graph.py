"""LangGraph workflow definition for MPOnline automation."""
import time
from typing import Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from src.core.agent_state import AgentState
from src.agents.navigator_node import navigator_node
from src.agents.form_expert_node import form_expert_node
from src.agents.auditor_node import auditor_node
from src.agents.captcha_node import captcha_node
from src.agents.payment_node import payment_node
from src.agents.browser_use_node import browser_use_node
from src import config
from src.utils.logging_config import logger


def create_graph():
    """
    Create the LangGraph workflow with supervisor pattern.
    
    Returns:
        Compiled graph with checkpointer
    """
    # Define routing logic
    def route_after_navigator(state: AgentState) -> Literal["form_expert", "browser_use", "error", END]:
        """Route after navigator node."""
        if state.get("errors"):
            return "error"
        
        next_action = state.get("next_action", "")
        
        # Check if AI automation is enabled
        use_ai = state.get("use_ai_automation", config.USE_AI_AUTOMATION)
        
        if use_ai:
            logger.info("routing_to_browser_use", ai_mode=True)
            return "browser_use"
        elif next_action == "fill_form":
            return "form_expert"
        elif next_action == "error":
            return "error"
        else:
            return "form_expert"
    
    def route_after_form_expert(state: AgentState) -> Literal["auditor", "captcha", "error"]:
        """Route after form expert node."""
        if state.get("errors") and len(state.get("errors", [])) > 5:
            # Too many errors, stop
            return "error"
        
        # Check for CAPTCHA
        # Note: In real implementation, captcha detection happens in captcha_node
        # For routing, we always go to auditor first
        return "auditor"
    
    def route_after_auditor(state: AgentState) -> Literal["form_expert", "navigator", "captcha", END]:
        """Route after auditor node."""
        next_action = state.get("next_action", "")
        
        if next_action == "fill_form":
            # Validation failed, go back to form expert
            return "form_expert"
        elif next_action == "upload_documents":
            # Move to document upload step
            return "navigator"
        elif next_action == "preview":
            return "navigator"
        elif next_action == "payment":
            return "captcha"  # Check for CAPTCHA before payment
        elif next_action == "complete":
            return END
        else:
            return "captcha"
    
    def route_after_captcha(state: AgentState) -> Literal["payment", "navigator", "error", END]:
        """Route after CAPTCHA node."""
        next_action = state.get("next_action", "")
        
        if next_action == "error":
            return "error"
        elif next_action == "continue":
            # Proceed to payment or next step
            if state.get("current_step") == "payment" or state.get("next_action") == "payment":
                return "payment"
            else:
                return "navigator"
        else:
            return "navigator"
    
    def route_after_payment(state: AgentState) -> Literal["error", END]:
        """Route after payment node."""
        if state.get("errors"):
            return "error"
        return END
    
    def handle_error(state: AgentState) -> dict:
        """Error handler node."""
        logger.error("workflow_error", errors=state.get("errors"))
        return {
            "current_step": "error",
            "last_update_time": time.time()
        }
    
    # Create graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("navigator", navigator_node)
    workflow.add_node("form_expert", form_expert_node)
    workflow.add_node("browser_use", browser_use_node)  # NEW: AI-driven automation
    workflow.add_node("auditor", auditor_node)
    workflow.add_node("captcha", captcha_node)
    workflow.add_node("payment", payment_node)
    workflow.add_node("error", handle_error)
    
    # Set entry point
    workflow.set_entry_point("navigator")
    
    # Add edges with routing logic
    workflow.add_conditional_edges(
        "navigator",
        route_after_navigator,
        {
            "form_expert": "form_expert",
            "browser_use": "browser_use",  # NEW: Route to AI automation
            "error": "error",
            END: END
        }
    )
    
    # Add edge from browser_use to captcha (AI fills form, then CAPTCHA)
    workflow.add_conditional_edges(
        "browser_use",
        lambda state: "captcha" if state.get("next_action") == "captcha" else "error",
        {
            "captcha": "captcha",
            "error": "error"
        }
    )
    
    workflow.add_conditional_edges(
        "form_expert",
        route_after_form_expert,
        {
            "auditor": "auditor",
            "captcha": "captcha",
            "error": "error"
        }
    )
    
    workflow.add_conditional_edges(
        "auditor",
        route_after_auditor,
        {
            "form_expert": "form_expert",
            "navigator": "navigator",
            "captcha": "captcha",
            END: END
        }
    )
    
    workflow.add_conditional_edges(
        "captcha",
        route_after_captcha,
        {
            "payment": "payment",
            "navigator": "navigator",
            "error": "error",
            END: END
        }
    )
    
    workflow.add_conditional_edges(
        "payment",
        route_after_payment,
        {
            "error": "error",
            END: END
        }
    )
    
    # Error node goes to END
    workflow.add_edge("error", END)
    
    # Create checkpointer (in-memory for now, can be upgraded to SQLite later)
    checkpointer = MemorySaver()
    
    # Compile graph with HITL interrupts
    graph = workflow.compile(
        checkpointer=checkpointer,
        interrupt_before=["captcha", "payment"]  # Human-in-the-loop
    )
    
    logger.info("graph_compiled", nodes=len(workflow.nodes))
    
    return graph


async def run_graph(graph, initial_state: AgentState, thread_id: str):
    """
    Run the graph with given initial state.
    
    Args:
        graph: Compiled graph
        initial_state: Initial agent state
        thread_id: Thread ID for checkpointing
        
    Returns:
        Final state
    """
    config_dict = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    
    logger.info("graph_execution_started", thread_id=thread_id)
    
    try:
        final_state = None
        async for state in graph.astream(initial_state, config_dict):
            logger.info("graph_state_update", state_keys=list(state.keys()))
            final_state = state
        
        logger.info("graph_execution_completed", thread_id=thread_id)
        return final_state
        
    except Exception as e:
        logger.error("graph_execution_error", error=str(e), thread_id=thread_id)
        raise


async def resume_graph(graph, thread_id: str, updates: dict = None):
    """
    Resume a paused graph execution.
    
    Args:
        graph: Compiled graph
        thread_id: Thread ID to resume
        updates: State updates (e.g., CAPTCHA solution, payment confirmation)
        
    Returns:
        Final state
    """
    config_dict = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    
    logger.info("graph_resuming", thread_id=thread_id, updates=updates)
    
    try:
        final_state = None
        
        # If updates provided, continue with them
        if updates:
            async for state in graph.astream(updates, config_dict):
                logger.info("graph_state_update", state_keys=list(state.keys()))
                final_state = state
        else:
            # Just resume from checkpoint
            async for state in graph.astream(None, config_dict):
                logger.info("graph_state_update", state_keys=list(state.keys()))
                final_state = state
        
        logger.info("graph_resumed_completed", thread_id=thread_id)
        return final_state
        
    except Exception as e:
        logger.error("graph_resume_error", error=str(e), thread_id=thread_id)
        raise
