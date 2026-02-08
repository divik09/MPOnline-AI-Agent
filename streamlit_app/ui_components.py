"""UI components for Streamlit app."""
import streamlit as st
from typing import Dict, Any, List
from pathlib import Path


def render_chat_message(role: str, content: str):
    """
    Render a chat message.
    
    Args:
        role: 'user' or 'agent'
        content: Message content
    """
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong> {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message agent-message">
            <strong>🤖 Agent:</strong> {content}
        </div>
        """, unsafe_allow_html=True)


def render_progress_tracker(agent_state: Dict[str, Any]):
    """
    Render progress tracking UI.
    
    Args:
        agent_state: Current agent state
    """
    if not agent_state:
        return
    
    current_step = agent_state.get("current_step", "unknown")
    form_progress = agent_state.get("form_progress", {})
    
    steps = ["start", "login", "form_fill", "document_upload", "preview", "payment", "complete"]
    
    # Find current step index
    try:
        current_idx = steps.index(current_step)
    except ValueError:
        current_idx = 0
    
    # Progress bar
    progress = (current_idx + 1) / len(steps)
    st.progress(progress)
    
    # Step indicators
    cols = st.columns(len(steps))
    for idx, step in enumerate(steps):
        with cols[idx]:
            if idx < current_idx:
                st.markdown("✅")
            elif idx == current_idx:
                st.markdown("🔄")
            else:
                st.markdown("⏳")
            st.caption(step.replace("_", " ").title())
    
    # Form progress details
    if form_progress:
        st.subheader("Form Fields")
        filled = sum(1 for v in form_progress.values() if v)
        total = len(form_progress)
        st.metric("Fields Filled", f"{filled}/{total}")
        
        with st.expander("Field Details"):
            for field, status in form_progress.items():
                if status:
                    st.markdown(f"✅ {field}")
                else:
                    st.markdown(f"⏳ {field}")


def render_captcha_input(screenshot_path: str):
    """
    Render CAPTCHA input interface.
    
    Args:
        screenshot_path: Path to CAPTCHA screenshot
    """
    st.subheader("🔒 CAPTCHA Verification")
    
    if Path(screenshot_path).exists():
        st.image(screenshot_path, caption="CAPTCHA Image", use_column_width=True)
    else:
        st.warning("CAPTCHA image not available")
    
    captcha_solution = st.text_input(
        "Enter CAPTCHA text:",
        max_chars=10,
        help="Type the characters you see in the image above"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        submit = st.button("✅ Submit CAPTCHA", use_container_width=True)
    with col2:
        cancel = st.button("❌ Cancel", use_container_width=True)
    
    return captcha_solution, submit, cancel


def render_form_preview(user_data: Dict[str, Any]):
    """
    Render form data preview before submission.
    
    Args:
        user_data: Dictionary of user-provided data
    """
    st.subheader("📋 Preview Your Details")
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    items = list(user_data.items())
    mid = len(items) // 2
    
    with col1:
        for key, value in items[:mid]:
            if "photo" in key or "signature" in key or "certificate" in key:
                st.text(f"{key.replace('_', ' ').title()}: [File uploaded]")
            else:
                st.text(f"{key.replace('_', ' ').title()}: {value}")
    
    with col2:
        for key, value in items[mid:]:
            if "photo" in key or "signature" in key or "certificate" in key:
                st.text(f"{key.replace('_', ' ').title()}: [File uploaded]")
            else:
                st.text(f"{key.replace('_', ' ').title()}: {value}")


def render_error_banner(errors: List[str]):
    """
    Render error messages.
    
    Args:
        errors: List of error messages
    """
    if not errors:
        return
    
    st.error("⚠️ Errors Encountered")
    
    for error in errors:
        st.markdown(f"• {error}")


def render_service_card(service_info: Dict[str, str]):
    """
    Render a service card.
    
    Args:
        service_info: Service information dictionary
    """
    st.markdown(f"""
    <div class="service-card">
        <h4>{service_info['name']}</h4>
        <p>{service_info['description']}</p>
        <p><small><strong>Category:</strong> {service_info['category']}</small></p>
    </div>
    """, unsafe_allow_html=True)


def render_payment_confirmation(payment_details: str):
    """
    Render payment confirmation dialog.
    
    Args:
        payment_details: Payment details string
    """
    st.subheader("💳 Payment Confirmation")
    
    st.info(payment_details)
    
    st.warning("⚠️ Please review the payment details carefully before confirming.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        confirm = st.button("✅ Confirm Payment", use_container_width=True, type="primary")
    
    with col2:
        cancel = st.button("❌ Cancel", use_container_width=True)
    
    return confirm, cancel


def render_logs_panel():
    """Render optional logs panel for debugging."""
    with st.expander("🔍 View Logs (Advanced)"):
        st.caption("Real-time agent logs")
        # This would stream logs from the log file
        st.text("Logs will appear here...")
