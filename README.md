# MPOnline Agent - Agentic Service Automation

🤖 **Production-ready multi-agent system for automating form filling on the MPOnline portal**

Built with **LangGraph**, **Playwright**, and **Streamlit** to provide seamless automation of government services in Madhya Pradesh.

---

## 🌟 Features

- ✅ **Multi-Agent Architecture** - Supervisor pattern with specialized agents
- ✅ **Intelligent Form Filling** - Automatic field detection and filling
- ✅ **Vision-Powered** - GPT-4o/Claude 3.5 for ambiguous element identification
- ✅ **Human-in-the-Loop** - CAPTCHA and payment confirmation support
- ✅ **Stateful Persistence** - Resume from crashes with SqliteSaver checkpointing
- ✅ **Conversational UI** - Streamlit interface with step-by-step data collection
- ✅ **Bot Detection Mitigation** - Random delays and human-like behavior
- ✅ **Comprehensive Logging** - Structured logs for production observability

---

## 🏗️ Architecture

```
┌─────────────────────┐
│  Streamlit Frontend │
│  (User Interface)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   LangGraph Graph   │
│    (Orchestrator)   │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────────────────┐
│     Specialized Agent Nodes      │
├──────────────────────────────────┤
│ • Navigator  (Login & Routing)   │
│ • FormExpert (Form Filling)      │
│ • Auditor    (Validation)        │
│ • CAPTCHA    (HITL)              │
│ • Payment    (HITL)              │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│    Playwright Browser Manager    │
│   (Web Automation Layer)         │
└──────────────────────────────────┘
```

---

## 📋 Supported Services

| Service | Status | Description |
|---------|--------|-------------|
| **MPPSC** | ✅ Ready | Madhya Pradesh Public Service Commission applications |
| **Electricity** | ✅ Ready | Bill payment service |
| **Universities** | ✅ Ready | Barkatullah, Jiwaji, and other university applications |
| **More coming soon** | 🚧 | Additional services can be easily added |

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10 or higher
- Windows/Linux/macOS
- Valid MPOnline account credentials
- OpenAI or Anthropic API key

### 2. Installation

```bash
# Clone the repository
cd d:\workspaces\MPOnline-Agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 3. Configuration

```bash
# Copy environment template
copy .env.template .env

# Edit .env with your credentials
notepad .env
```

**Required configurations:**
- `MPONLINE_USERNAME` - Your MPOnline login username
- `MPONLINE_PASSWORD` - Your MPOnline login password
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` - LLM provider API key
- `ENCRYPTION_KEY` - 32-character encryption key for data security

### 4. Run the Application

```bash
# Start Streamlit app
streamlit run streamlit_app/app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📖 Usage Guide

### Step 1: Select Service

1. Open the Streamlit app
2. Choose a service from the sidebar (e.g., "MPPSC Application")
3. Click "Start New Session"

### Step 2: Provide Details

The agent will ask you questions one by one:

```
Agent: What is your full name?
You: John Doe

Agent: What is your email address?
You: john.doe@example.com

... (continues for all required fields)
```

### Step 3: Review & Confirm

- Preview all collected data
- Edit if needed
- Click "Start Automation"

### Step 4: CAPTCHA Solving

When CAPTCHA appears:
- The workflow pauses
- CAPTCHA image is displayed
- Enter the text you see
- Click "Submit"

### Step 5: Payment Confirmation

When payment page appears:
- Review payment details
- Type "confirm" to proceed
- Agent completes the transaction

### Step 6: Completion

- Download acknowledgment receipt
- View final screenshot
- Start a new session if needed

---

## 🔧 Advanced Configuration

### LLM Provider Selection

```env
# Use OpenAI GPT-4o
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here

# OR use Anthropic Claude 3.5 Sonnet
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### Browser Settings

```env
# Run browser in headless mode (no GUI)
HEADLESS_MODE=true

# Show browser (useful for debugging)
HEADLESS_MODE=false

# Slow down actions (milliseconds)
SLOW_MO=100
```

### Bot Detection Mitigation

```env
# Random delay range (milliseconds)
MIN_DELAY=1000
MAX_DELAY=3000

# Typing speed (milliseconds per character)
TYPING_SPEED=100
```

---

## 🗂️ Project Structure

```
MPOnline-Agent/
├── src/
│   ├── core/
│   │   ├── agent_state.py      # State definition
│   │   └── graph.py            # LangGraph workflow
│   ├── agents/
│   │   ├── navigator_node.py   # URL routing & login
│   │   ├── form_expert_node.py # Form filling
│   │   ├── auditor_node.py     # Validation
│   │   ├── captcha_node.py     # CAPTCHA handling
│   │   └── payment_node.py     # Payment verification
│   ├── automation/
│   │   ├── browser_manager.py  # Playwright lifecycle
│   │   └── browser_actions.py  # Automation utilities
│   ├── tools/
│   │   ├── vision_tool.py      # Multimodal LLM
│   │   └── human_input_tool.py # HITL interface
│   ├── services/
│   │   ├── mppsc_template.py   # MPPSC service
│   │   ├── electricity_template.py
│   │   └── service_registry.py # Service catalog
│   ├── utils/
│   │   ├── logging_config.py   # Structured logging
│   │   └── encryption.py       # Data encryption
│   └── config.py               # Configuration
├── streamlit_app/
│   ├── app.py                  # Main UI
│   └── ui_components.py        # Reusable components
├── data/                       # Generated at runtime
│   ├── checkpoints.db          # State persistence
│   ├── screenshots/            # Captured screens
│   └── logs/                   # Application logs
├── requirements.txt
├── .env.template
├── .gitignore
└── README.md
```

---

## 🛠️ Development

### Adding a New Service

1. Create template in `src/services/your_service_template.py`:

```python
class YourServiceTemplate:
    @staticmethod
    def get_url() -> str:
        return "https://service-url.mponline.gov.in"
    
    @staticmethod
    def get_field_mappings(step: str):
        return {
            "field_name": {
                "selector": "#input_id",
                "type": "text",
                "required": True
            }
        }
```

2. Register in `src/services/service_registry.py`:

```python
SERVICE_REGISTRY = {
    "your_service": YourServiceTemplate,
    # ... other services
}
```

3. Add questions in `streamlit_app/app.py`:

```python
def get_questions_for_service(service_type: str):
    if service_type == "your_service":
        return [
            {"field": "name", "question": "What is your name?", "type": "text"},
            # ... more questions
        ]
```

### Running Tests

```bash
# Unit tests
pytest tests/test_navigator.py
pytest tests/test_form_expert.py

# Integration tests
pytest tests/test_graph_flow.py

# Browser tests (requires browser)
pytest tests/test_browser_actions.py --headed
```

---

## 📊 Monitoring & Debugging

### View Logs

Logs are stored in `data/logs/agent.log` in JSON format:

```json
{
  "event": "safe_click_success",
  "selector": "#btnSubmit",
  "timestamp": "2024-01-18T22:30:45",
  "level": "info"
}
```

### Enable Debug Mode

```env
LOG_LEVEL=DEBUG
HEADLESS_MODE=false  # See browser in action
```

### Resume from Checkpoint

If the workflow crashes, it automatically resumes from the last saved state using the same `thread_id`.

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** - Contains sensitive credentials
2. **Use strong encryption key** - 32 random characters for `ENCRYPTION_KEY`
3. **Rotate API keys regularly** - Update LLM provider keys periodically
4. **Monitor usage** - Check LLM API usage to avoid unexpected costs
5. **Test in non-production** - Use test environments before production

---

## ⚠️ Legal & Compliance

> **Important**: This tool is for educational and authorized use only. Ensure you have:
> - Permission to automate on MPOnline portal
> - Valid account credentials
> - Compliance with Terms of Service
> - Understanding of legal implications

The authors are not responsible for misuse of this tool.

---

## 🐛 Troubleshooting

### Issue: "Configuration Errors"

**Solution**: Ensure all required variables in `.env` are set correctly

### Issue: "CAPTCHA timeout"

**Solution**: Increase `CAPTCHA_TIMEOUT` in `.env`

### Issue: "Selector not found"

**Solution**: Enable headless mode (`HEADLESS_MODE=false`) to debug visually

### Issue: "Browser crashes"

**Solution**: Run `playwright install chromium` to reinstall browser

### Issue: "VisionTool errors"

**Solution**: Verify your API key is valid and has sufficient credits

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License.

---

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review logs in `data/logs/agent.log`

---

## 🙏 Acknowledgments

- **LangGraph** - For powerful agent orchestration
- **Playwright** - For reliable browser automation
- **Streamlit** - For beautiful UI development
- **MPOnline** - For digitizing government services

---

**Made with ❤️ for automating bureaucracy**
