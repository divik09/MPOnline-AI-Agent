"""
Smart chat app that opens browser first, discovers fields, then asks questions.

Flow:
1. User says "I want MPPSC"
2. Browser opens, searches Google, navigates
3. System analyzes form fields
4. System asks for each discovered field
5. Fills form as user provides data
"""
import streamlit as st
import asyncio
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from src.agents.smart_form_agent import SmartFormAgent

# Page config
st.set_page_config(
    page_title="MPOnline Smart Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "smart_agent" not in st.session_state:
    st.session_state.smart_agent = None
    
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "👋 Hi! I'm your smart MPOnline assistant.\n\nJust tell me what you want to do, and I'll:\n1. **Open the browser** and find the form\n2. **Analyze what fields** are actually needed\n3. **Ask you for each field** one by one\n4. **Fill the form** as you provide answers\n\nTry saying:\n- \"I want to apply for MPPSC\"\n- \"Search for electricity bill payment\"\n- \"Help with university admission\""
    }]

if "workflow_state" not in st.session_state:
    st.session_state.workflow_state = "initial"  # initial, searching, analyzing, collecting, filling

if "current_service" not in st.session_state:
    st.session_state.current_service = None

# Header
st.title("🧠 MPOnline Smart Assistant")
st.caption("Browser-first approach: I'll find the form, then ask what's needed!")

# Sidebar
with st.sidebar:
    st.header("📊 Status")
    
    if st.session_state.workflow_state == "initial":
        st.info("💬 Waiting for your request...")
    elif st.session_state.workflow_state == "searching":
        st.success("🔍 Searching and navigating...")
    elif st.session_state.workflow_state == "analyzing":
        st.success("🔬 Analyzing form fields...")
    elif st.session_state.workflow_state == "collecting":
        st.success("✏️ Collecting information...")
        if st.session_state.smart_agent:
            progress = st.session_state.smart_agent.get_progress()
            st.text(progress)
    elif st.session_state.workflow_state == "filling":
        st.success("🎨 Filling form...")
    
    st.divider()
    
    if st.session_state.current_service:
        st.metric("Service", st.session_state.current_service.upper())
    
    if st.session_state.smart_agent and st.session_state.smart_agent.discovered_fields:
        st.subheader("📝 Discovered Fields")
        for field in st.session_state.smart_agent.discovered_fields[:5]:  # Show first 5
            status = "✅" if field['name'] in st.session_state.smart_agent.collected_data else "⏳"
            st.text(f"{status} {field['label']}")
    
    st.divider()
    
    if st.button("🔄 Start Over"):
        if st.session_state.smart_agent:
            st.session_state.smart_agent.cleanup()
        st.session_state.smart_agent = None
        st.session_state.workflow_state = "initial"
        st.session_state.current_service = None
        st.session_state.messages = [{
            "role": "assistant",
            "content": "All reset! What would you like to help with?"
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
    
    # Process based on workflow state
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
            st.session_state.workflow_state = "searching"
            
            with st.chat_message("assistant"):
                response = f"🚀 Great! I'll help you with **{service.upper()}**.\n\n"
                response += "⏳ Opening browser and searching for the form..."
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Start browser and navigate
            with st.spinner("🌐 Opening browser and navigating..."):
                st.session_state.smart_agent = SmartFormAgent()
                result = st.session_state.smart_agent.search_and_navigate(service)
            
            # Analyze form
            st.session_state.workflow_state = "analyzing"
            with st.chat_message("assistant"):
                st.markdown(f"{result}\n\n🔬 Analyzing form to find required fields...")
                st.session_state.messages.append({"role": "assistant", "content": result})
            
            with st.spinner("🔬 Discovering form fields..."):
                fields = st.session_state.smart_agent.discover_form_fields()
            
            # Start asking questions
            st.session_state.workflow_state = "collecting"
            
            with st.chat_message("assistant"):
                field_list = "\n".join([f"• {f['label']}" for f in fields[:5]])
                response = f"✅ Found {len(fields)} fields on the form!\n\nFirst few:\n{field_list}\n\n"
                
                # Ask first question
                question = st.session_state.smart_agent.get_next_question()
                if question:
                    response += f"\n{question}"
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.rerun()
        else:
            # Didn't understand
            with st.chat_message("assistant"):
                response = "I'm not sure which service you need. Please tell me:\n• **MPPSC** application\n• **Electricity** bill payment\n• **University** admission"
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    elif st.session_state.workflow_state == "collecting":
        # Extract data from user message
        data = st.session_state.smart_agent.extract_data(prompt)
        st.session_state.smart_agent.collected_data.update(data)
        
        # Fill form incrementally
        if data:
            st.session_state.smart_agent.fill_form_incrementally()
        
        # Get next question
        next_question = st.session_state.smart_agent.get_next_question()
        
        with st.chat_message("assistant"):
            if next_question:
                progress = st.session_state.smart_agent.get_progress()
                response = f"✅ Got it! {progress}\n\n{next_question}"
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                # All fields collected!
                response = "🎉 All fields filled!\n\nThe form has been completed. Please check the browser window and:\n1. Solve any CAPTCHA if present\n2. Review the filled information\n3. Click submit when ready!"
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.workflow_state = "complete"
        
        st.rerun()

# Footer
st.divider()
st.caption("🧠 Smart Assistant | Browser-First Approach | Dynamic Field Discovery")
