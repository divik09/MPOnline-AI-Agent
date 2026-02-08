# Quick Start Guide - MPOnline Agent

## ⚡ Fast Setup (5 minutes)

### Step 1: Install Dependencies

```bash
cd d:\workspaces\MPOnline-Agent

# Run automated setup
python setup.py
```

This will:
- Install all Python packages
- Download Playwright browsers
- Create `.env` file
- Set up directory structure

### Step 2: Configure Credentials

Edit `.env` file:

```env
# Required: Your MPOnline account
MPONLINE_USERNAME=your_actual_username
MPONLINE_PASSWORD=your_actual_password

# Required: Choose ONE LLM provider
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-actual-key

# OR use Anthropic
# LLM_PROVIDER=anthropic
# ANTHROPIC_API_KEY=sk-ant-your-actual-key

# Required: Generate random 32 characters
ENCRYPTION_KEY=abcdefghijklmnopqrstuvwxyz123456
```

### Step 3: Test Installation

```bash
python test_installation.py
```

You should see all ✅ checkmarks.

### Step 4: Run the App

```bash
streamlit run streamlit_app/app.py
```

Browser opens at `http://localhost:8501`

### Step 5: Fill Your First Form

1. Click **"Start New Session"** in sidebar
2. Select **"MPPSC Application"**
3. Answer agent's questions one by one
4. Click **"Start Automation"**
5. Watch the magic! 🎩✨

---

## 🎯 Example: MPPSC Application

```
Agent: What is your full name?
You: Rajesh Kumar

Agent: What is your father's name?
You: Ram Kumar

Agent: What is your email?
You: rajesh@example.com

... (continues for all fields)

Agent: Upload your photo
You: [select photo.jpg]

✅ All details collected!

[Click: Start Automation]

🤖 Agent starts filling form...
📸 Screenshot saved
⏸️  CAPTCHA detected - please solve
[You enter CAPTCHA]
✅ Form submitted successfully!
```

---

## 🔧 Troubleshooting

### "Configuration Errors"
**Fix:** Edit `.env` and fill in all required values

### "playwright not found"
**Fix:** Run `playwright install chromium`

### "API key invalid"
**Fix:** Verify your OpenAI/Anthropic key is correct

### "Can't connect to MPOnline"
**Fix:** Check your internet connection and MPOnline credentials

---

## 📚 Next Steps

- Read [README.md](file:///d:/workspaces/MPOnline-Agent/README.md) for detailed docs
- Check [walkthrough.md](file:///C:/Users/k/.gemini/antigravity/brain/a84740d1-3034-4527-840a-48b5652b3152/walkthrough.md) for implementation details
- Explore `src/` to understand the code
- Add your own service templates in `src/services/`

---

**Happy Automating! 🚀**
