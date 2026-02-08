"""
Autonomous Form Filling Application
Simple interface to collect user details and auto-fill MPOnline forms
"""
import streamlit as st
import asyncio
from advanced_form_filler import AdvancedFormFillingAgent
from datetime import datetime
import json
import os

# Page configuration
st.set_page_config(
    page_title="MPOnline Auto Form Filler",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'result_log' not in st.session_state:
    st.session_state.result_log = []

# Header
st.markdown('<div class="main-header">🤖 MPOnline Autonomous Form Filler</div>', unsafe_allow_html=True)

# Sidebar - Service Selection
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=MPOnline", use_container_width=True)
    st.markdown("### 📋 Select Service")
    
    service_type = st.selectbox(
        "Service Type",
        [
            "MPPSC Application",
            "MPESB Recruitment",
            "University Admission",
            "Bill Payment",
            "Custom URL"
        ]
    )
    
    # Service URLs mapping
    service_urls = {
        "MPPSC Application": "https://mppsc.mponline.gov.in",
        "MPESB Recruitment": "https://esb.mponline.gov.in",
        "University Admission": "https://bubhopal.mponline.gov.in",
        "Bill Payment": "https://www.mponline.gov.in/Portal/Services/MPEDB/Home.aspx",
    }
    
    if service_type == "Custom URL":
        target_url = st.text_input("Enter Custom URL", "https://www.mponline.gov.in")
    else:
        target_url = service_urls.get(service_type, "https://www.mponline.gov.in")
    
    st.markdown(f"**Target URL:** {target_url}")
    
    st.markdown("---")
    st.markdown("### ⚙️ Browser Settings")
    headless_mode = st.checkbox("Headless Mode", value=False, help="Run browser in background")
    demo_mode = st.checkbox("Demo Mode (Don't Submit)", value=True, help="Preview without submitting")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="section-header">📝 Enter Your Details</div>', unsafe_allow_html=True)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["👤 Personal Info", "📍 Contact Details", "🎓 Education", "📎 Documents"])
    
    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            full_name = st.text_input("Full Name *", placeholder="e.g., Rajesh Kumar")
            father_name = st.text_input("Father's Name", placeholder="e.g., Ram Kumar")
            mother_name = st.text_input("Mother's Name", placeholder="e.g., Sita Devi")
        with col_b:
            dob = st.date_input("Date of Birth *")
            gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
            category = st.selectbox("Category", ["General", "OBC", "SC", "ST", "EWS"])
    
    with tab2:
        col_a, col_b = st.columns(2)
        with col_a:
            email = st.text_input("Email *", placeholder="your.email@example.com")
            mobile = st.text_input("Mobile Number *", placeholder="10-digit mobile number")
            alt_mobile = st.text_input("Alternate Mobile", placeholder="Optional")
        with col_b:
            address = st.text_area("Address *", placeholder="Complete address")
            city = st.text_input("City", placeholder="e.g., Bhopal")
            pincode = st.text_input("Pincode", placeholder="6-digit pincode")
    
    with tab3:
        col_a, col_b = st.columns(2)
        with col_a:
            qualification = st.selectbox(
                "Highest Qualification",
                ["High School", "Intermediate", "Graduate", "Post Graduate", "Doctorate"]
            )
            university = st.text_input("University/Board", placeholder="e.g., Barkatullah University")
        with col_b:
            passing_year = st.text_input("Passing Year", placeholder="e.g., 2020")
            percentage = st.text_input("Percentage/CGPA", placeholder="e.g., 75.5%")
    
    with tab4:
        st.markdown("**Upload Documents (optional)**")
        photo = st.file_uploader("Photograph", type=["jpg", "jpeg", "png"])
        signature = st.file_uploader("Signature", type=["jpg", "jpeg", "png"])
        id_proof = st.file_uploader("ID Proof", type=["pdf", "jpg", "jpeg", "png"])
        
        if st.checkbox("Use default test documents"):
            st.info("Will use sample documents from data/uploads/ folder")

with col2:
    st.markdown('<div class="section-header">📊 Form Summary</div>', unsafe_allow_html=True)
    
    # Count filled fields
    filled_fields = sum([
        bool(full_name), bool(father_name), bool(mother_name),
        bool(email), bool(mobile), bool(address),
        bool(qualification), bool(university)
    ])
    total_fields = 8
    
    st.progress(filled_fields / total_fields)
    st.markdown(f"**Fields Filled:** {filled_fields}/{total_fields}")
    
    st.markdown("---")
    
    # Data preview
    form_data = {
        "name": full_name,
        "fname": father_name,
        "mname": mother_name,
        "father": father_name,
        "mother": mother_name,
        "dob": dob.strftime("%d/%m/%Y") if dob else "",
        "dateofbirth": dob.strftime("%d/%m/%Y") if dob else "",
        "gender": gender,
        "category": category,
        "email": email,
        "mobile": mobile,
        "phone": mobile,
        "contact": mobile,
        "address": address,
        "city": city,
        "pincode": pincode,
        "pin": pincode,
        "qualification": qualification,
        "university": university,
        "passing_year": passing_year,
        "percentage": percentage,
    }
    
    # Remove empty values
    form_data = {k: v for k, v in form_data.items() if v}
    
    with st.expander("📄 View Data to be Filled"):
        st.json(form_data)

# Action buttons
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])

with col_btn1:
    start_button = st.button("🚀 Start Auto-Fill", type="primary", use_container_width=True)

with col_btn2:
    test_button = st.button("🧪 Test Connection", use_container_width=True)

with col_btn3:
    clear_button = st.button("🗑️ Clear All", use_container_width=True)

# Handle clear button
if clear_button:
    st.rerun()

# Handle test connection
if test_button:
    with st.spinner("Testing connection to MPOnline..."):
        async def test_connection():
            agent = AdvancedFormFillingAgent(headless=True)
            try:
                await agent.start_browser()
                success = await agent.navigate_to_service(target_url)
                await agent.close()
                return success
            except Exception as e:
                return False
        
        result = asyncio.run(test_connection())
        
        if result:
            st.success(f"✅ Successfully connected to {target_url}")
        else:
            st.error(f"❌ Failed to connect to {target_url}")

# Handle start automation
if start_button:
    # Validation
    if not full_name or not email or not mobile:
        st.error("⚠️ Please fill required fields: Full Name, Email, Mobile")
    else:
        st.session_state.form_data = form_data
        st.session_state.automation_running = True
        
        # Create progress area
        progress_container = st.container()
        
        with progress_container:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown("### 🤖 Automation in Progress...")
            st.markdown('</div>', unsafe_allow_html=True)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            log_area = st.empty()
            
            # Run automation
            async def run_automation():
                logs = []
                
                try:
                    # Initialize agent
                    status_text.text("🚀 Initializing browser...")
                    progress_bar.progress(10)
                    logs.append("✓ Browser initialization started")
                    
                    agent = AdvancedFormFillingAgent(headless=headless_mode)
                    await agent.start_browser()
                    
                    progress_bar.progress(20)
                    logs.append("✓ Browser started successfully")
                    log_area.text("\n".join(logs))
                    
                    # Navigate
                    status_text.text(f"🌐 Navigating to {service_type}...")
                    progress_bar.progress(30)
                    
                    success = await agent.navigate_to_service(target_url)
                    if not success:
                        logs.append("✗ Navigation failed")
                        return logs, False
                    
                    progress_bar.progress(40)
                    logs.append(f"✓ Navigated to {target_url}")
                    log_area.text("\n".join(logs))
                    
                    # Detect fields
                    status_text.text("🔍 Detecting form fields...")
                    progress_bar.progress(50)
                    
                    fields = await agent.detect_form_fields()
                    logs.append(f"✓ Detected {len(fields)} form fields")
                    log_area.text("\n".join(logs))
                    
                    progress_bar.progress(60)
                    
                    # Fill form
                    status_text.text("✏️ Filling form with your data...")
                    progress_bar.progress(70)
                    
                    filled = await agent.auto_fill_form(form_data)
                    if not filled:
                        logs.append("⚠ No fields were filled")
                    else:
                        logs.append("✓ Form filled successfully")
                    
                    log_area.text("\n".join(logs))
                    progress_bar.progress(85)
                    
                    # Find submit button
                    if not demo_mode:
                        status_text.text("🔍 Finding submit button...")
                        found_submit = await agent.find_and_click_submit()
                        if found_submit:
                            logs.append("✓ Submit button found and clicked")
                        else:
                            logs.append("⚠ Submit button not found")
                    else:
                        status_text.text("⚠️ Demo mode - Not submitting form")
                        logs.append("⚠ Demo mode - Form not submitted")
                        await agent.find_and_click_submit()
                    
                    log_area.text("\n".join(logs))
                    progress_bar.progress(95)
                    
                    # Save logs
                    await agent.save_action_log()
                    logs.append("✓ Action log saved")
                    
                    progress_bar.progress(100)
                    log_area.text("\n".join(logs))
                    
                    await agent.close()
                    logs.append("✓ Browser closed")
                    
                    return logs, True
                    
                except Exception as e:
                    logs.append(f"✗ Error: {str(e)}")
                    return logs, False
            
            # Run the automation
            logs, success = asyncio.run(run_automation())
            
            # Show results
            st.markdown("---")
            if success:
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.markdown("### ✅ Automation Completed Successfully!")
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("**📊 Results:**")
                for log in logs:
                    st.text(log)
                
                st.markdown("**📸 Screenshots saved in:** `data/screenshots/`")
                st.markdown("**📝 Action logs saved in:** `data/logs/`")
                
                if demo_mode:
                    st.warning("⚠️ Demo mode was enabled - Form was NOT submitted. Review the screenshots and disable demo mode to actually submit.")
                
            else:
                st.error("❌ Automation encountered errors. Check the logs above.")
        
        st.session_state.automation_running = False

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d; font-size: 0.9rem;'>
        🤖 MPOnline Autonomous Form Filler | Built with Playwright + Streamlit<br>
        ⚠️ Use responsibly and in compliance with MPOnline Terms of Service
    </div>
""", unsafe_allow_html=True)
