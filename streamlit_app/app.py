"""Main Streamlit application for MPOnline Agent."""
import streamlit as st
import asyncio
import time
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.core.graph import create_graph, run_graph, resume_graph
from src.core.agent_state import AgentState
from src.services.service_registry import get_service_list
from src.tools.human_input_tool import human_input_tool
from src import config
from src.utils.logging_config import logger
from streamlit_app.ui_components import (
    render_chat_message,
    render_progress_tracker,
    render_captcha_input,
    render_form_preview,
    render_error_banner
)


# Page config
st.set_page_config(
    page_title="MPOnline Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .service-card {
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ddd;
        margin: 0.5rem 0;
    }
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .agent-message {
        background-color: #f5f5f5;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state."""
    if "graph" not in st.session_state:
        st.session_state.graph = None
    
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = f"thread_{int(time.time())}"
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}
    
    if "service_type" not in st.session_state:
        st.session_state.service_type = None
    
    if "workflow_state" not in st.session_state:
        st.session_state.workflow_state = "idle"  # idle, collecting, running, paused, complete
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
    
    if "question_index" not in st.session_state:
        st.session_state.question_index = 0
    
    if "agent_state" not in st.session_state:
        st.session_state.agent_state = None


def get_questions_for_service(service_type: str) -> list:
    """Get questions to ask user for a service."""
    if service_type == "general":
        # General assistant - just ask for the query
        return [
            {"field": "query", "question": "What would you like me to help you with?", "type": "text"},
        ]
    elif service_type == "mppsc":
        return [
            {"field": "full_name", "question": "What is your full name?", "type": "text"},
            {"field": "father_name", "question": "What is your father's name?", "type": "text"},
            {"field": "mother_name", "question": "What is your mother's name?", "type": "text"},
            {"field": "date_of_birth", "question": "What is your date of birth? (DD/MM/YYYY)", "type": "text"},
            {"field": "gender", "question": "What is your gender?", "type": "select", "options": ["Male", "Female", "Other"]},
            {"field": "category", "question": "Select your category:", "type": "select", "options": ["General", "OBC", "SC", "ST"]},
            {"field": "email", "question": "What is your email address?", "type": "text"},
            {"field": "mobile", "question": "What is your mobile number?", "type": "text"},
            {"field": "address", "question": "What is your permanent address?", "type": "text"},
            {"field": "district", "question": "Select your district:", "type": "text"},
            {"field": "state", "question": "Select your state:", "type": "text"},
            {"field": "pincode", "question": "What is your PIN code?", "type": "text"},
            {"field": "qualification", "question": "What is your highest qualification?", "type": "text"},
            {"field": "photo", "question": "Upload your passport-size photograph (JPG, max 50KB):", "type": "file"},
            {"field": "signature", "question": "Upload your signature (JPG, max 20KB):", "type": "file"},
        ]
    elif service_type == "electricity":
        return [
            {"field": "consumer_number", "question": "What is your electricity consumer number?", "type": "text"},
            {"field": "mobile", "question": "What is your registered mobile number?", "type": "text"},
            {"field": "email", "question": "What is your email for receipt? (optional)", "type": "text"},
        ]
    else:
        return []


async def start_automation():
    """Start the automation workflow."""
    st.session_state.workflow_state = "running"
    
    # Create initial state
    initial_state: AgentState = {
        "user_data": st.session_state.user_data,
        "service_type": st.session_state.service_type,
        "use_ai_automation": st.session_state.get("use_ai_automation", True),
        "use_real_browser": st.session_state.get("use_real_browser", False),
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
    
    # Create graph if not exists
    if not st.session_state.graph:
        st.session_state.graph = create_graph()
    
    # Run graph
    try:
        final_state = await run_graph(
            st.session_state.graph,
            initial_state,
            st.session_state.thread_id
        )
        
        st.session_state.agent_state = final_state
        
        # Check if paused for HITL
        if final_state.get("next_action") in ["captcha", "payment"]:
            st.session_state.workflow_state = "paused"
        else:
            st.session_state.workflow_state = "complete"
        
    except Exception as e:
        logger.error("streamlit_automation_error", error=str(e))
        st.error(f"Error during automation: {str(e)}")
        st.session_state.workflow_state = "idle"


def main():
    """Main Streamlit application."""
    initialize_session_state()
    
    # Validate configuration
    config_errors = config.validate_config()
    if config_errors:
        st.error("⚠️ Configuration Errors")
        for error in config_errors:
            st.error(f"• {error}")
        st.info("Please update your .env file with correct values. See .env.template for reference.")
        return
    
    # Header
    st.markdown('<div class="main-header">🤖 MPOnline Agent</div>', unsafe_allow_html=True)
    st.markdown("*Automated form filling for MPOnline portal services*")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Service selection
        services = get_service_list()
        
        # Add General Assistant service
        services.insert(0, {
            "key": "general",
            "name": "General Assistant",
            "description": "Ask the AI to help with any MPOnline query or task",
            "category": "General"
        })
        
        service_names = [f"{s['name']} ({s['category']})" for s in services]
        service_keys = [s['key'] for s in services]
        
        if st.session_state.workflow_state == "idle":
            selected_idx = st.selectbox(
                "Select Service",
                range(len(service_names)),
                format_func=lambda x: service_names[x]
            )
            
            # Automation mode selector
            st.divider()
            st.subheader("⚙️ Automation Mode")
            
            automation_mode = st.radio(
                "Choose automation approach",
                options=["🤖 AI-Powered (Recommended)", "📋 Template-Based (Legacy)"],
                help="""
                **AI-Powered**: Uses natural language to intelligently navigate and fill forms. 
                Adapts to any website changes automatically.
                
                **Template-Based**: Uses pre-defined selectors. Faster but breaks if website changes.
                """
            )
            
            use_ai = "AI-Powered" in automation_mode
            
            # Show mode comparison
            with st.expander("📊 Mode Comparison"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**🤖 AI-Powered**")
                    st.markdown("✅ Adapts to changes")
                    st.markdown("✅ Works on any form")
                    st.markdown("✅ No maintenance")
                    st.markdown("⏱️ Slower (30-60s)")
                    st.markdown("💰 ~$0.15-0.40 per form")
                with col2:
                    st.markdown("**📋 Template-Based**")
                    st.markdown("✅ Very fast (5-10s)")
                    st.markdown("✅ Free (no LLM costs)")
                    st.markdown("❌ Breaks on changes")
                    st.markdown("❌ Limited to known services")
                    st.markdown("❌ Requires maintenance")
            
            st.divider()
            
            # Real Browser mode (for General Assistant)
            st.subheader("🌐 Browser Mode")
            use_real_browser = st.checkbox(
                "Use my existing Chrome browser",
                value=config.USE_REAL_BROWSER,
                help="""Connect to your existing Chrome browser to preserve logins and cookies.
                **IMPORTANT**: You must close Chrome before running the agent."""
            )
            
            st.divider()
            
            if st.button("🚀 Start New Session"):
                st.session_state.service_type = service_keys[selected_idx]
                st.session_state.use_ai_automation = use_ai
                st.session_state.use_real_browser = use_real_browser
                st.session_state.workflow_state = "collecting"
                
                mode_text = "AI-powered" if use_ai else "template-based"
                st.session_state.conversation.append({
                    "role": "agent",
                    "content": f"Great! Let's fill your {services[selected_idx]['name']} form using {mode_text} automation. I'll ask you a few questions."
                })
                st.rerun()
        
        st.divider()
        
        # Show thread ID
        st.caption(f"Thread ID: {st.session_state.thread_id}")
        
        # Reset button
        if st.button("🔄 Reset Session"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Main content
    if st.session_state.workflow_state == "idle":
        # Welcome screen
        st.info("👋 Welcome! Select a service from the sidebar to get started.")
        
        # Show available services
        st.subheader("Available Services")
        cols = st.columns(2)
        for idx, service in enumerate(services):
            with cols[idx % 2]:
                st.markdown(f"""
                <div class="service-card">
                    <h4>{service['name']}</h4>
                    <p>{service['description']}</p>
                    <small>Category: {service['category']}</small>
                </div>
                """, unsafe_allow_html=True)
    
    elif st.session_state.workflow_state == "collecting":
        # Collect user data conversationally
        st.subheader("📝 Provide Your Details")
        
        # Display conversation
        for msg in st.session_state.conversation:
            render_chat_message(msg["role"], msg["content"])
        
        # Get questions for service
        questions = get_questions_for_service(st.session_state.service_type)
        
        if st.session_state.question_index < len(questions):
            current_q = questions[st.session_state.question_index]
            st.session_state.current_question = current_q
            
            # Ask question
            with st.form(key=f"question_{st.session_state.question_index}"):
                st.markdown(f"**{current_q['question']}**")
                
                if current_q["type"] == "text":
                    answer = st.text_input("Your answer:", key=f"answer_{st.session_state.question_index}")
                elif current_q["type"] == "select":
                    answer = st.selectbox("Select option:", current_q.get("options", []))
                elif current_q["type"] == "file":
                    answer = st.file_uploader("Upload file:", type=["jpg", "jpeg", "pdf"])
                
                submitted = st.form_submit_button("Submit")
                
                if submitted and answer:
                    # Save answer
                    if current_q["type"] == "file":
                        # Save uploaded file
                        file_path = config.DATA_DIR / "uploads" / answer.name
                        file_path.parent.mkdir(exist_ok=True)
                        with open(file_path, "wb") as f:
                            f.write(answer.getbuffer())
                        st.session_state.user_data[current_q["field"]] = str(file_path)
                    else:
                        st.session_state.user_data[current_q["field"]] = answer
                    
                    # Add to conversation
                    st.session_state.conversation.append({
                        "role": "user",
                        "content": str(answer) if current_q["type"] != "file" else f"[File: {answer.name}]"
                    })
                    
                    # Move to next question
                    st.session_state.question_index += 1
                    
                    if st.session_state.question_index < len(questions):
                        st.session_state.conversation.append({
                            "role": "agent",
                            "content": f"Got it! {questions[st.session_state.question_index]['question']}"
                        })
                    
                    st.rerun()
        
        else:
            # All questions answered
            st.success("✅ All details collected!")
            
            # Show preview
            render_form_preview(st.session_state.user_data)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ Edit Details"):
                    st.session_state.question_index = 0
                    st.rerun()
            
            with col2:
                if st.button("🚀 Start Automation"):
                    asyncio.run(start_automation())
                    st.rerun()
    
    elif st.session_state.workflow_state == "running":
        # Show automation in progress
        st.subheader("🤖 Automation in Progress")
        
        with st.spinner("Agent is working..."):
            st.info("The agent is filling your form. Please wait...")
            render_progress_tracker(st.session_state.agent_state)
    
    elif st.session_state.workflow_state == "paused":
        # HITL - CAPTCHA or Payment
        st.subheader("⏸️ Human Input Required")
        
        if st.session_state.agent_state:
            # Check if CAPTCHA
            screenshot = st.session_state.agent_state.get("screenshot_path")
            
            if screenshot and Path(screenshot).exists():
                st.image(str(screenshot), caption="Current Page")
            
            # Check for pending requests
            pending = human_input_tool.list_pending_requests()
            
            if pending:
                request_id = pending[0]
                request = human_input_tool.get_pending_request(request_id)
                
                st.info(request["prompt"])
                
                user_input = st.text_input("Your response:")
                
                if st.button("Submit"):
                    # Submit response
                    human_input_tool.submit_response(request_id, user_input)
                    
                    # Resume graph
                    asyncio.run(resume_graph(
                        st.session_state.graph,
                        st.session_state.thread_id
                    ))
                    
                    st.session_state.workflow_state = "running"
                    st.rerun()
    
    elif st.session_state.workflow_state == "complete":
        # Automation complete
        st.success("✅ Automation completed successfully!")
        
        if st.session_state.agent_state:
            screenshot = st.session_state.agent_state.get("screenshot_path")
            if screenshot and Path(screenshot).exists():
                st.image(str(screenshot), caption="Final Result")
            
            errors = st.session_state.agent_state.get("errors", [])
            if errors:
                render_error_banner(errors)
        
        if st.button("🏠 Return Home"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


if __name__ == "__main__":
    main()
