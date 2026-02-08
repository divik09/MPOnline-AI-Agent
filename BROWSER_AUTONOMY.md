# 🤖 Browser Autonomy for MPOnline - Complete Guide

## 📋 Overview

This guide demonstrates **autonomous browser automation** for the MPOnline portal, showing how to navigate, search, detect forms, and fill them automatically using Playwright-based intelligent agents.

## 🎯 What You Got

### 1. **Autonomous Navigation Agent** (`autonomous_mponline_browser.py`)
- ✅ Automatically navigates to MPOnline
- ✅ Discovers all available services
- ✅ Searches for specific services
- ✅ Analyzes page structure
- ✅ Captures screenshots
- ✅ Logs all actions to JSON

### 2. **Advanced Form Filling Agent** (`advanced_form_filler.py`)
- ✅ Intelligently detects all form fields
- ✅ Matches fields by name, ID, or label
- ✅ Fills forms with human-like behavior
- ✅ Handles text inputs, selects, textareas
- ✅ Finds and identifies submit buttons
- ✅ Full action logging

## 🚀 Quick Start

### Run Autonomous Navigation

```bash
cd d:\workspaces\MPOnline-Agent
python autonomous_mponline_browser.py
```

**What it does:**
1. Opens MPOnline homepage
2. Discovers 18+ available services
3. Analyzes page structure
4. Saves screenshot and action log

**Results:**
- Screenshot: `data/screenshots/mponline_homepage_*.png`
- Action log: `data/logs/autonomous_agent_*.json`

### Run Advanced Form Filler

```bash
cd d:\workspaces\MPOnline-Agent
python advanced_form_filler.py
```

**What it does:**
1. Opens browser
2. Navigates to MPOnline
3. Detects all form fields
4. Shows field analysis
5. Can auto-fill with provided data

## 📊 Latest Test Results

### Autonomous Navigation Results

From the latest run (`autonomous_agent_20260206_103811.json`):

**✅ Services Discovered: 18**

| Service | URL |
|---------|-----|
| Payment Double Verification | `/Portal/Services/DoubleVerification/...` |
| MPPC Pharmacy Council | `http://pharmacy.mponline.gov.in` |
| PanCard | `/portal/services/pancard/home.aspx` |
| MPESB (Selection Board) | `https://esb.mponline.gov.in` |
| RDVV University | `https://rdvv.mponline.gov.in` |
| Labour Department | `https://labour.mponline.gov.in` |
| National Parks | `https://forest.mponline.gov.in` |
| Barkatullah University | `https://bubhopal.mponline.gov.in` |
| And 10 more... | |

**Main Categories:**
- Applications
- Recruitment
- Counselling
- University
- Bill Payments
- Reservation

**Page Analysis:**
- Forms: 2
- Input fields: 21
  - Text: 2
  - Checkbox: 1
  - Hidden: 17
  - Submit: 1

## 🎨 Screenshots

![MPOnline Homepage](data/screenshots/mponline_homepage_20260206_103808.png)

*Screenshot showing all discovered services and categories*

## 📝 Code Examples

### Example 1: Navigate and Discover

```python
from autonomous_mponline_browser import AutonomousMPOnlineAgent
import asyncio

async def explore_mponline():
    agent = AutonomousMPOnlineAgent(headless=False)
    
    await agent.start_browser()
    await agent.navigate_to_mponline()
    
    # Discover all services
    services = await agent.discover_services()
    
    # Search for something
    await agent.search_on_portal("MPPSC")
    
    # Click on a service
    await agent.click_service("Recruitment", services)
    
    # Analyze the page
    await agent.analyze_page()
    
    await agent.save_action_log()
    await agent.close()

asyncio.run(explore_mponline())
```

### Example 2: Auto-Fill a Form

```python
from advanced_form_filler import AdvancedFormFillingAgent
import asyncio

async def fill_mppsc_form():
    # Your form data
    form_data = {
        "name": "Rajesh Kumar",
        "fname": "Ram Kumar",
        "email": "rajesh@example.com",
        "mobile": "9876543210",
        "dob": "01/01/1995",
        "gender": "Male",
        "category": "General",
        "address": "123 Main Street, Bhopal",
        "pincode": "462001",
    }
    
    agent = AdvancedFormFillingAgent(headless=False)
    
    await agent.start_browser()
    
    # Navigate to specific service
    await agent.navigate_to_service("https://esb.mponline.gov.in")
    
    # Auto-fill the form
    await agent.auto_fill_form(form_data)
    
    # Find submit button (but don't click in demo mode)
    await agent.find_and_click_submit()
    
    await agent.save_action_log()
    await agent.close()

asyncio.run(fill_mppsc_form())
```

### Example 3: Custom Service Automation

```python
async def automate_custom_service():
    agent = AdvancedFormFillingAgent(headless=False)
    
    await agent.start_browser()
    
    # Step 1: Navigate to service
    await agent.navigate_to_service("https://your-service-url.mponline.gov.in")
    
    # Step 2: Detect what fields are available
    fields = await agent.detect_form_fields()
    
    # Step 3: Prepare data based on detected fields
    custom_data = {}
    for field in fields:
        field_name = field.get('name') or field.get('label')
        print(f"Field: {field_name}, Type: {field['type']}")
        # Add your logic to populate custom_data
    
    # Step 4: Fill the form
    await agent.auto_fill_form(custom_data)
    
    # Step 5: Submit (if needed)
    # await agent.find_and_click_submit()
    
    await agent.close()

asyncio.run(automate_custom_service())
```

## 🔧 Integration with Your Existing Agent

Your MPOnline Agent already has the infrastructure. Here's how to integrate:

### Option 1: Use as Standalone Tool

Just run the scripts when you need autonomous exploration or form filling.

### Option 2: Integrate into LangGraph Workflow

```python
# In src/agents/form_expert_node.py

from advanced_form_filler import AdvancedFormFillingAgent

async def form_expert(state: AgentState) -> AgentState:
    """Enhanced with autonomous form filling."""
    
    # Create autonomous agent
    auto_agent = AdvancedFormFillingAgent(headless=config.HEADLESS_MODE)
    
    # Start browser (or reuse existing)
    await auto_agent.start_browser()
    
    # Auto-detect and fill form
    await auto_agent.auto_fill_form(state.form_data)
    
    # Continue with existing logic...
    
    return state
```

### Option 3: Add as New Agent Node

```python
# Create new src/agents/autonomous_navigator_node.py

from autonomous_mponline_browser import AutonomousMPOnlineAgent

async def autonomous_navigator(state: AgentState) -> AgentState:
    """
    Autonomous navigation and service discovery.
    """
    agent = AutonomousMPOnlineAgent(headless=config.HEADLESS_MODE)
    
    await agent.start_browser()
    
    # Discover services
    services = await agent.discover_services()
    
    # Find matching service for user's request
    target_service = None
    for service in services:
        if state.service_type.lower() in service['text'].lower():
            target_service = service
            break
    
    if target_service:
        await agent.click_service(target_service['text'], services)
        state.current_url = agent.page.url
        state.status = "service_found"
    else:
        state.status = "service_not_found"
    
    await agent.close()
    return state
```

## 🎯 Key Features Explained

### 1. **Autonomous Service Discovery**

The agent can find services without knowing the exact URLs:

```python
services = await agent.discover_services()
# Returns: [
#   {"text": "MPPSC", "href": "...", "selector": "..."},
#   {"text": "University", "href": "...", "selector": "..."},
#   ...
# ]
```

### 2. **Intelligent Field Detection**

Auto-detects all types of form fields:

```python
fields = await agent.detect_form_fields()
# For each field, returns:
# - type: text, email, select, textarea, etc.
# - name, id, label
# - required: boolean
# - options: for select fields
# - placeholder
```

### 3. **Smart Field Matching**

Automatically matches your data to form fields:

```python
form_data = {"name": "John", "email": "john@example.com"}
# Agent matches:
# - "name" -> input[name="full_name"] or input[id="userName"]
# - "email" -> input[type="email"] or input[name="email_address"]
```

### 4. **Human-Like Behavior**

- Random delays (1-3 seconds)
- Variable typing speed (50-150ms per character)
- Scroll into view before interaction
- Realistic user agent and browser settings

### 5. **Complete Action Logging**

Every action is logged:

```json
{
  "timestamp": "2026-02-06T10:38:04.306440",
  "action": "navigate",
  "details": {"url": "https://www.mponline.gov.in"}
}
```

## 📂 Output Files

### Screenshots
Location: `data/screenshots/`
- `mponline_homepage_*.png` - Homepage
- `service_page_*.png` - Service pages
- `search_results_*.png` - Search results
- `form_filled_*.png` - After form filling
- `before_submit_*.png` - Before submission

### Action Logs
Location: `data/logs/`
- `autonomous_agent_*.json` - Navigation actions
- `form_filling_*.json` - Form filling actions

## 🛡️ Safety Features

### Demo Mode
By default, the `find_and_click_submit()` function **does NOT** click submit:

```python
print("⚠️  NOT clicking submit (demo mode)")
# Uncomment to actually submit:
# await submit_btn.click()
```

### Action Logging
All actions are logged before execution, allowing you to:
- Review what the agent did
- Debug issues
- Audit for compliance

### Screenshot Evidence
Screenshots are taken at every major step for:
- Verification
- Debugging
- Documentation
- Compliance

## 🔍 Troubleshooting

### Browser Won't Start

```bash
# Install Playwright browsers
playwright install chromium
```

### No Services Discovered

The selectors might have changed. Update in `discover_services()`:

```python
service_selectors = [
    'a[href*="citizen"]',
    # Add more selectors here
]
```

### Fields Not Detected

Enable headless=False and check the page manually:

```python
agent = AdvancedFormFillingAgent(headless=False)
```

## 📚 Next Steps

1. **Test on Specific Service**
   - Modify the demo functions
   - Add your target service URL
   - Run and verify

2. **Integrate with Main Agent**
   - Add autonomous modules to your LangGraph workflow
   - Enhance existing form_expert with auto-detection
   - Add service discovery to navigator

3. **Add More Intelligence**
   - Use GPT-4 Vision for CAPTCHA reading
   - Add OCR for PDF extraction
   - Implement retry logic with backoff

4. **Production Deployment**
   - Add error recovery
   - Implement session management
   - Add monitoring and alerts

## 🎉 Summary

You now have **two powerful autonomous agents**:

1. **Navigation Agent** - Explores, discovers, and navigates
2. **Form Filling Agent** - Detects and fills forms intelligently

Both integrate seamlessly with your existing MPOnline Agent architecture!

---

**Built with ❤️ using Playwright and Python**

*Last updated: February 6, 2026*
