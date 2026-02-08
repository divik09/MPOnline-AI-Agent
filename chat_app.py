"""
Chat-based Streamlit app for conversational MPOnline automation.

Users can chat naturally:
- "I want to apply for MPPSC"
- "Search for electricity bill payment"
- "My name is John, email john@example.com"

The AI understands and automates accordingly!
"""
import streamlit as st
import asyncio
import time
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.agents.conversational_agent import ConversationalAgent
from src.agents.browser_use_node import browser_use_node
from src.core.agent_state import AgentState
from src.utils.browser_use_helper import estimate_ai_automation_cost
from src import config


# Page config
st.set_page_config(
    page_title="MPOnline AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "chat_agent" not in st.session_state:
    st.session_state.chat_agent = ConversationalAgent()
    
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "👋 Hello! I'm your MPOnline AI assistant. I can help you with:\n\n• **MPPSC Applications** - Government job applications\n• **Electricity Bill Payments** - Pay your MP electricity bills\n• **University Admissions** - College applications\n\nJust tell me what you need in plain language! For example:\n- \"I want to apply for MPPSC\"\n- \"Search for electricity bill payment\"\n- \"Help me with university admission\""
    }]

if "automation_running" not in st.session_state:
    st.session_state.automation_running = False


# Header
st.title("🤖 MPOnline AI Assistant")
st.caption("Chat naturally - I'll understand and automate for you!")

# Sidebar - Info
with st.sidebar:
    st.header("📊 Session Info")
    
    agent = st.session_state.chat_agent
    
    if agent.current_service:
        st.success(f"**Service:** {agent.current_service.upper()}")
    else:
        st.info("**Service:** Not selected yet")
    
    if agent.collected_data:
        st.subheader("📝 Collected Information")
        for key, value in agent.collected_data.items():
            st.text(f"{key.replace('_', ' ').title()}: {value}")
    
    st.divider()
    
    st.subheader("💡 Example Prompts")
    st.code("I want to apply for MPPSC")
    st.code("Search for electricity bill")
    st.code("My name is John Doe")
    st.code("Email: john@example.com")
    st.code("Mobile: 9876543210")
    
    st.divider()
    
    if st.button("🔄 Reset Conversation"):
        st.session_state.chat_agent = ConversationalAgent()
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Conversation reset! How can I help you today?"
        }]
        st.rerun()


# Chat messages display
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# Chat input
if prompt := st.chat_input("Type your message... (e.g., 'I want to apply for MPPSC')"):
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get agent response
    with st.spinner("🤔 Understanding your request..."):
        response = st.session_state.chat_agent.chat(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response["message"])
        
        # Show collected data if significant
        if response["data"] and len(response["data"]) > 0:
            with st.expander("📋 Information Collected"):
                for key, value in response["data"].items():
                    st.text(f"• {key.replace('_', ' ').title()}: {value}")
        
        # Show automation button if ready
        if response.get("ready_to_automate"):
            st.success("✅ Ready to automate!")
            
            # Show cost estimate
            if response.get("service"):
                cost = estimate_ai_automation_cost(
                    response["service"],
                    config.LLM_PROVIDER
                )
                st.info(f"💰 Estimated cost: ${cost['estimated_min_cost']:.2f} - ${cost['estimated_max_cost']:.2f}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🚀 Start Automation", type="primary", use_container_width=True):
                    # Trigger automation
                    st.session_state.automation_running = True
                    st.rerun()
            
            with col2:
                if st.button("✏️ Edit Details", use_container_width=True):
                    st.info("Just tell me what to change! For example: 'Change email to newemail@example.com'")
    
    # Add assistant response to messages
    st.session_state.messages.append({
        "role": "assistant",
        "content": response["message"]
    })
    
    st.rerun()


# Run automation if triggered
if st.session_state.automation_running:
    st.divider()
    st.header("🤖 AI Automation in Progress")
    
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    with progress_placeholder.container():
        st.info("🔄 Preparing automation...")
        
        # Create automation state
        agent = st.session_state.chat_agent
        
        initial_state: AgentState = {
            "user_data": agent.collected_data,
            "service_type": agent.current_service,
            "use_ai_automation": True,
            "current_step": "start",
            "form_progress": {},
            "dom_snapshot": None,
            "screenshot_path": None,
            "current_url": None,
            "session_data": {},
            "errors": [],
            "messages": [],
            "next_action": "navigate",
            "captcha_solution": None,
            "payment_confirmed": False,
            "attempt_count": {},
            "start_time": time.time(),
            "last_update_time": time.time()
        }
        
        st.success("✅ State prepared")
        st.info("🌐 Launching browser...")
        
        # Run automation
        try:
            result = asyncio.run(browser_use_node(initial_state))
            
            with status_placeholder.container():
                if result.get("current_step") == "form_filled":
                    st.success("🎉 Automation completed successfully!")
                    
                    st.markdown("### 📊 Results")
                    st.text(f"✅ Current URL: {result.get('current_url', 'N/A')}")
                    
                    if result.get('screenshot_path'):
                        st.image(result['screenshot_path'], caption="Form Screenshot")
                    
                    st.markdown("### ⏭️ Next Steps")
                    st.info("The form has been filled. Please check the browser window, solve any CAPTCHA if present, and submit the form.")
                    
                    # Add result to chat
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"✅ I've successfully filled the form! Please check the browser window and complete any CAPTCHA or final verification needed."
                    })
                else:
                    st.warning("⚠️ Automation completed with issues")
                    if result.get('errors'):
                        st.error("Errors encountered:")
                        for error in result['errors']:
                            st.text(f"• {error}")
        
        except Exception as e:
            st.error(f"❌ Automation failed: {e}")
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Sorry, I encountered an error: {str(e)}. Would you like to try again?"
            })
        
        finally:
            st.session_state.automation_running = False
            if st.button("↩️ Back to Chat"):
                st.rerun()


# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🤖 Powered by browser-use + LangGraph")
with col2:
    st.caption(f"🔧 LLM: {config.LLM_PROVIDER.upper()}")
with col3:
    if st.session_state.chat_agent.current_service:
        st.caption(f"📋 Service: {st.session_state.chat_agent.current_service.upper()}")
