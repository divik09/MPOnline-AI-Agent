# MPOnline Agent - Project Structure

```
MPOnline-Agent/
│
├── 📄 Configuration Files
│   ├── .env.template          # Environment variables template
│   ├── .gitignore            # Git ignore rules
│   ├── requirements.txt      # Python dependencies
│   └── setup.py              # Automated setup script
│
├── 📚 Documentation
│   ├── README.md             # Main documentation (11KB)
│   ├── QUICKSTART.md         # 5-minute setup guide
│   └── test_installation.py  # Installation verification
│
├── 🧠 src/ - Core Application
│   │
│   ├── config.py             # Configuration management
│   ├── __init__.py
│   │
│   ├── 🎯 core/             # LangGraph Architecture
│   │   ├── agent_state.py   # State definition (TypedDict)
│   │   ├── graph.py         # Workflow orchestration
│   │   └── __init__.py
│   │
│   ├── 🤖 agents/           # Specialized Agent Nodes
│   │   ├── navigator_node.py    # URL routing & login
│   │   ├── form_expert_node.py  # Form filling
│   │   ├── auditor_node.py      # Validation
│   │   ├── captcha_node.py      # CAPTCHA handler (HITL)
│   │   ├── payment_node.py      # Payment verifier (HITL)
│   │   └── __init__.py
│   │
│   ├── 🌐 automation/       # Browser Automation
│   │   ├── browser_manager.py  # Playwright lifecycle
│   │   ├── browser_actions.py  # Utilities (click, fill, etc)
│   │   └── __init__.py
│   │
│   ├── 🔧 tools/           # Advanced Tools
│   │   ├── vision_tool.py      # GPT-4o/Claude element detection
│   │   ├── human_input_tool.py # HITL interface
│   │   └── __init__.py
│   │
│   ├── 📋 services/        # Service Templates
│   │   ├── mppsc_template.py      # MPPSC forms
│   │   ├── electricity_template.py # Bill payment
│   │   ├── service_registry.py    # Service catalog
│   │   └── __init__.py
│   │
│   └── 🛠️ utils/          # Utilities
│       ├── logging_config.py  # Structured logging
│       ├── encryption.py      # Data encryption
│       └── __init__.py
│
├── 🖥️ streamlit_app/      # User Interface
│   ├── app.py              # Main Streamlit app
│   ├── ui_components.py    # Reusable components
│   └── __init__.py
│
└── 📁 data/               # Generated at Runtime
    ├── checkpoints.db     # SqliteSaver state
    ├── screenshots/       # Captured images
    ├── logs/             # Application logs
    └── uploads/          # User uploaded files

Total: 26 Python files | ~5,800 lines of code
```

## 📊 Component Breakdown

| Category | Files | Purpose |
|----------|-------|---------|
| **Core Architecture** | 2 | LangGraph state & workflow |
| **Agent Nodes** | 5 | Specialized automation agents |
| **Browser Layer** | 2 | Playwright automation |
| **Tools** | 2 | Vision AI & HITL |
| **Services** | 3 | Form templates |
| **Utilities** | 3 | Logging, encryption |
| **Frontend** | 2 | Streamlit UI |
| **Config** | 1 | Settings management |
| **Setup/Test** | 2 | Installation scripts |
| **Docs** | 3 | README, guides |

## 🎯 Key Files to Understand

1. **[graph.py](file:///d:/workspaces/MPOnline-Agent/src/core/graph.py)** - Entry point, workflow orchestration
2. **[app.py](file:///d:/workspaces/MPOnline-Agent/streamlit_app/app.py)** - UI entry point
3. **[agent_state.py](file:///d:/workspaces/MPOnline-Agent/src/core/agent_state.py)** - State structure
4. **[navigator_node.py](file:///d:/workspaces/MPOnline-Agent/src/agents/navigator_node.py)** - First agent in workflow
5. **[service_registry.py](file:///d:/workspaces/MPOnline-Agent/src/services/service_registry.py)** - Service catalog

## 🔄 Data Flow

```
User (Streamlit UI)
    ↓
[Service Selection + Data Collection]
    ↓
LangGraph Workflow
    ↓
Navigator → FormExpert → Auditor → CAPTCHA → Payment
    ↓         ↓          ↓         ↓          ↓
    └─────────┴──────────┴─────────┴──────────┘
                    ↓
            Playwright Browser
                    ↓
            MPOnline Portal
                    ↓
          [Success/Failure]
                    ↓
            User Notification
```

## 📝 Next Steps

1. Run `python setup.py` to install
2. Edit `.env` with credentials
3. Run `python test_installation.py`
4. Start with `streamlit run streamlit_app/app.py`
5. Read [QUICKSTART.md](file:///d:/workspaces/MPOnline-Agent/QUICKSTART.md)
