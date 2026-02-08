"""
Agentic Smart Chat App - Powered by LangGraph + browser-use.

Never gets stuck. Always tries alternative strategies.
Truly intelligent browser automation!
"""
import streamlit as st
import asyncio
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from src.agents.agentic_browser_agent import AgenticBrowserAgent

# Page config
st.set_page_config(
    page_title="Agentic MPOnline Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "agentic_agent" not in st.session_state:
    st.session_state.agentic_agent = AgenticBrowserAgent()
    
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": """👋 Hi! I'm your **Agentic** MPOnline AI assistant.

I'm powered by **LangGraph + browser-use** which means:
- 🔄 I **never get stuck** - if one approach fails, I try another
- 🧠 I'm **intelligent** - I adapt my strategy based on results
- 🎯 I'm **persistent** - I keep trying until I succeed
- 🔍 I use **multiple strategies**: Google search, direct URLs, site exploration

Just tell me what you need, and I'll figure out the best way to get it done!

Try saying:
- "I want to apply for MPPSC"
- "Help me with electricity bill"
- "University admission form"""
    }]

if "current_service" not in st.session_state:
    st.session_state.current_service = None

if "user_data" not in st.session_state:
    st.session_state.user_data = {}

if "workflow_state" not in st.session_state:
    st.session_state.workflow_state = "initial"  # initial, collecting, running, complete

# Header
st.title("🧠 Agentic MPOnline Assistant")
st.caption("Powered by LangGraph + browser-use | Multi-Strategy AI Browser Automation")

# Sidebar
with st.sidebar:
    st.header("🎯 Agentic Features")
    
    st.markdown("""
    **What makes this Agentic?**
    
    ✅ **Adaptive**: Tries multiple strategies
    - Google Search
    - Direct URL navigation
    - Portal exploration  
    - Alternative search engines
    
    ✅ **Resilient**: Never gets stuck
    - If one approach fails, tries another
    - Learns from errors
    - Keeps going until success
    
    ✅ **Intelligent**: AI-powered decisions
    - Uses LangGraph for routing
    - Uses browser-use for actions
    - Makes smart choices
    """)
    
    st.divider()
    
    if st.session_state.current_service:
        st.metric("Service", st.session_state.current_service.upper())
    
    if st.session_state.user_data:
        st.subheader("📝 Collected Data")
        for key, value in st.session_state.user_data.items():
            st.text(f"{key}: {value}")
    
    st.divider()
    
    if st.button("🔄 Reset"):
        st.session_state.current_service = None
        st.session_state.user_data = {}
        st.session_state.workflow_state = "initial"
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Reset complete! What would you like help with?"
        }]
        st.rerun()

# Chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Tell me what you need..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process based on state
    if st.session_state.workflow_state == "initial":
        # Detect service
        prompt_lower = prompt.lower()
        service = None
        
        if any(word in prompt_lower for word in ["mppsc", "psc", "recruitment"]):
            service = "mppsc"
        elif any(word in prompt_lower for word in ["electricity", "bill", "bijli"]):
            service = "electricity"
        elif any(word in prompt_lower for word in ["university", "college", "admission"]):
            service = "university"
        
        if service:
            st.session_state.current_service = service
            st.session_state.workflow_state = "collecting"
            
            with st.chat_message("assistant"):
                response = f"""🚀 Great! I'll help you with **{service.upper()}**.

Before I start my agentic browser automation, I need some basic information for the form.

**What is your full name?**"""
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        else:
            with st.chat_message("assistant"):
                response = "I'm not sure which service you need. Please tell me:\n• **MPPSC** application\n• **Electricity** bill payment\n• **University** admission"
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    elif st.session_state.workflow_state == "collecting":
        # Collect user data
        # Simple field collection (you can enhance this)
        if "full_name" not in st.session_state.user_data:
            st.session_state.user_data["full_name"] = prompt
            next_q = "**What is your email address?**"
        elif "email" not in st.session_state.user_data:
            st.session_state.user_data["email"] = prompt
            next_q = "**What is your mobile number?**"
        elif "mobile" not in st.session_state.user_data:
            st.session_state.user_data["mobile"] = prompt
            next_q = None  # Done collecting minimum data
        else:
            next_q = None
        
        with st.chat_message("assistant"):
            if next_q:
                response = f"✅ Got it!\n\n{next_q}"
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                # Ready to run agentic automation
                response = """✅ Perfect! I have enough information to start.

🎯 I'm now activating my **agentic browser automation**!

I'll try multiple strategies to find and fill the form:
1. **Google Search** - Search for the official page
2. **Direct URL** - Navigate directly if Google fails
3. **Portal Exploration** - Intelligently explore the site
4. **Alternative Search** - Try DuckDuckGo if needed

Watchas I work my magic! 🪄"""
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.workflow_state = "running"
            
            st.rerun()

# Run agentic automation if ready
if st.session_state.workflow_state == "running":
    st.divider()
    st.header("🤖 Agentic Automation Running")
    
    with st.spinner("🧠 Agent is thinking and trying different strategies..."):
        # Create agentic agent and run
        agent = st.session_state.agentic_agent
        
        goal = f"Fill out {st.session_state.current_service.upper()} application form"
        
        try:
            # Run the agentic workflow
            result = asyncio.run(agent.run(
                goal=goal,
                service_type=st.session_state.current_service,
                user_data=st.session_state.user_data
            ))
            
            # Show results
            st.success("✅ Agentic automation completed!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Success", "Yes" if result.get('success') else "No")
                st.metric("Attempts", result.get('attempt_count', 0))
            with col2:
                strategies = ", ".join(result.get('strategies_tried', []))
                st.text(f"Strategies tried: {strategies}")
            
            st.info(f"**Reasoning**: {result.get('reasoning', 'N/A')}")
            
            if result.get('errors'):
                with st.expander("⚠️ Errors Encountered"):
                    for error in result['errors']:
                        st.text(f"• {error}")
            
            # Add result to chat
            if result.get('success'):
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"""🎉 **Success!** 

I successfully filled out your form using **{len(result.get('strategies_tried', []))} different strategies**.

Final reasoning: {result.get('reasoning')}

Please check the browser window and complete any CAPTCHA or final verification!"""
                })
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"""⚠️ I tried {result.get('attempt_count')} different approaches but couldn't complete the task.

Strategies attempted: {', '.join(result.get('strategies_tried', []))}

Would you like me to try again with different parameters?"""
                })
            
            st.session_state.workflow_state = "complete"
            
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Sorry, I encountered an error: {str(e)}"
            })
            st.session_state.workflow_state = "complete"
        
        if st.button("↩️ Back to Chat"):
            st.rerun()

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🤖 LangGraph + browser-use")
with col2:
    st.caption("🔄 Multi-Strategy Agent")
with col3:
    st.caption("🧠 Never Gets Stuck")
