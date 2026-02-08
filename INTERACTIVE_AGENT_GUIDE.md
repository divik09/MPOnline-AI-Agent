# Interactive Browser Agent - User Guide

## Overview
This is your **human-like browser assistant** that helps you navigate websites, search for portals, and fill forms with natural conversation and interaction.

## Features

### 🤖 Conversational Interface
- Ask questions and get responses
- The agent asks for help when stuck
- Waits for your input at each step

### 🔍 Smart Search & Navigation
- Searches Google for portals/websites
- Intelligently selects search results
- Asks for confirmation before clicking

### 👤 Human-like Behavior
- Random delays between actions (0.5-2 seconds)
- Types character-by-character like a human
- Highlights elements before clicking
- Scrolls smoothly into view

### 📝 Interactive Form Filling
- Detects all form fields automatically
- Offers multiple filling options:
  - Auto-fill with sample data
  - Manual filling (you fill while agent waits)
  - Ask for each field value
  - Skip form filling

### 🆘 Gets Help When Stuck
- Takes screenshot when can't find elements
- Asks you what to do
- Waits for manual intervention
- Accepts guidance and retries

### 📸 Evidence Collection
- Screenshots at every major step
- Conversation logs in JSON
- Full interaction history

## How to Use

### Basic Usage

```bash
python interactive_browser_agent.py
```

### Example Session

```
Example 1: MPOnline Portal Navigation

Agent: What portal or website would you like me to visit?
You: MPOnline

Agent: Searching Google for: MPOnline
Agent: Found these search results:
  1. MPOnline Portal - Official Website
  2. MPPSC - MPOnline
  
Agent: Which result should I click? (1-2 or enter URL)
You: 1

Agent: Navigating to: https://mponline.gov.in/portal/

Agent: What would you like me to do next?
Options:
  1. Click on something (I'll search for it)
  2. Fill a form on this page
  3. Take screenshot and describe page
  4. Go to a specific URL
  5. I'm done - close browser

You: 1

Agent: What should I click? (describe it)
You: MPPSC

Agent: Looking for: MPPSC
Agent: ✓ Clicked: MPPSC

Agent: What would you like me to do next?
You: 1

Agent: What should I click?
You: State Service Preliminary Examination 2026

[Agent tries to find and click...]

Agent: ❌ I couldn't find 'State Service...' automatically.
       What should I do?
Options:
  1. I'll click it manually - wait
  2. Try a different search
  3. It's already visible - describe it
  4. Skip this step

You: 3

Agent: Please describe what I should look for:
You: Application Form

Agent: ✓ Found and clicked based on your guidance!

Agent: Analyzing form on current page...
Agent: Found 25 form fields

[Shows all fields...]

Agent: How would you like to proceed?
Options:
  1. Fill with sample data automatically
  2. I'll fill manually
  3. Ask me for each field value
  4. Skip form filling for now

You: 1

Agent: ✓ Filled: Name
Agent: ✓ Filled: Email
...
Agent: Filled 20/25 fields
```

## Key Capabilities

### 1. Smart Element Finding
The agent tries multiple strategies to find elements:
- Exact text match
- Contains text
- Button/link with text
- XPath selectors

### 2. Interactive Problem Solving
When stuck:
1. Takes screenshot
2. Asks for guidance
3. Offers multiple options
4. Waits for your decision
5. Retries with your input

### 3. Form Intelligence
- Auto-detects all form fields
- Shows field labels, placeholders, and requirements
- Offers flexible filling options
- Handles different input types (text, select, textarea, etc.)

### 4. Conversation Memory
- Remembers all interactions
- Saves to JSON log file
- Can reference previous actions

## Output Files

### Screenshots
- Location: `data/screenshots/interactive/`
- Format: `<action>_<timestamp>.png`
- Full page screenshots

### Logs
- Location: `data/logs/interactive/`
- Format: `conversation_<timestamp>.json`
- Contains all messages, actions, and timestamps

## Advanced Features

### Custom User Agent
Uses realistic browser user agent to avoid detection

### Network Waiting
Waits for network idle before proceeding

### Error Recovery
- Try-catch on all actions
- Graceful degradation
- User intervention option

## Tips for Best Results

1. **Be Descriptive**: When agent asks what to click, use the exact text or a clear description
2. **Use Manual Mode**: If agent struggles, switch to manual clicking
3. **Check Screenshots**: Review screenshots to guide the agent better
4. **Be Patient**: Agent adds human-like delays for natural behavior

## Example Use Cases

### Case 1: MPPSC Form Filling
```
Query: MPOnline
Click: MPPSC
Click: State Service Preliminary Examination 2026
Click: Application Form
Fill: Auto-fill with sample data
```

### Case 2: Any Government Portal
```
Query: <Portal Name>
Follow prompts...
Agent asks when stuck...
You guide it...
Form gets filled...
```

### Case 3: Manual Intervention
```
Agent: Can't find element
You: Choose "I'll click manually"
You: Click in browser
You: Press Enter
Agent: Continues...
```

## Troubleshooting

**Q: Agent can't find an element**
A: Choose manual intervention or provide better description

**Q: Form field not filled**
A: Choose "I'll fill manually" option

**Q: Wrong search result clicked**
A: Enter full URL when asked instead of selecting from list

**Q: Agent too fast/slow**
A: Delays are randomized (0.5-2s) - behavior is normal

## Future Enhancements
- Voice interaction
- Multi-tab support
- CAPTCHA solving with user help
- File upload assistance
- Payment page navigation

## Safety Notes
- Always review before submitting forms
- Use sample data for testing
- Agent won't auto-submit without confirmation
- All actions are logged for review
