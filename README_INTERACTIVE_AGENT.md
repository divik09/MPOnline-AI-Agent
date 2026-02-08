# MPOnline Interactive Agent - User Guide

## Overview
This interactive agent helps you fill the MPPSC (Madhya Pradesh Public Service Commission) application form automatically using AI-powered browser automation.

## Features
✅ **Interactive Data Collection** - Asks for your details before starting  
✅ **Smart Form Filling** - Automatically navigates and fills the form  
✅ **Error Handling** - Asks for help when stuck  
✅ **Safe Execution** - Stops before payment for your review  
✅ **Visual Feedback** - Shows browser window so you can monitor progress  

## Prerequisites
1. Python environment set up with dependencies installed
2. OpenAI API key configured in `.env` file
3. Internet connection
4. Active browser (Chrome/Chromium)

## How to Use

### Step 1: Activate Virtual Environment
```powershell
.\venv\Scripts\activate
```

### Step 2: Run the Interactive Agent
```powershell
python mponline_interactive_agent.py
```

### Step 3: Provide Your Details
The agent will ask for the following information:
- **Exam Type**: Choose between State Service, Forest Service, or Both
- **Personal Information**: Name, Father's name, Mother's name, DOB, Gender, Category
- **Contact Details**: Mobile, Email, Address, Pincode, District, State
- **Education**: Qualification, University, Year of Passing, Percentage

💡 **Tip**: Press Enter to use dummy/default values for testing

### Step 4: Verify Your Information
The agent will display all collected data for your confirmation.
Review carefully and confirm with "yes"

### Step 5: Monitor the Browser
- A browser window will open automatically
- Watch as the AI agent navigates and fills the form
- **DO NOT close the browser manually**
- The agent will show progress in the terminal

### Step 6: Review and Complete
Once the agent finishes:
1. Review the filled form in the browser
2. Upload required documents (photo, signature, etc.)
3. Proceed to payment
4. Submit the application

## What the Agent Does

### ✅ Agent WILL Do:
- Navigate to MPOnline website
- Search for MPPSC exam
- Accept candidate declaration
- Fill personal details
- Fill contact information
- Fill educational qualifications
- Navigate through form sections
- Stop at payment page

### ❌ Agent WILL NOT Do:
- Make payment (requires manual intervention)
- Upload documents (photos, signatures)
- Submit final application
- Handle CAPTCHAs (requires manual input)

## Troubleshooting

### Problem: "Module not found" error
**Solution**: Make sure virtual environment is activated and dependencies installed
```powershell
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Problem: "No OpenAI API key" error
**Solution**: Check your `.env` file has:
```
OPENAI_API_KEY=your-actual-api-key-here
```

### Problem: Agent gets stuck or errors out
**Solution**: 
1. Check if MPOnline website is accessible
2. Ensure form structure hasn't changed
3. Try running again with different data
4. Check terminal for specific error messages

### Problem: Browser closes immediately
**Solution**: The agent might have encountered an error. Check the terminal output for error messages.

## Advanced Usage

### Using Real Data
Edit the data collection prompts or directly modify the `user_data` dictionary in the script.

### Customizing the Task
Modify the `create_task_prompt()` method to change how the agent fills the form.

### Adding More Fields
Extend the `collect_personal_details()` method to collect additional information.

## Safety Notes

⚠️ **IMPORTANT**:
- Always review the filled form before payment
- Keep your API key secure
- Don't share filled forms with incorrect information
- Use dummy data for testing purposes only
- The agent stops before payment - you complete it manually

## Example Run

```
================================================================================
🎓 MPOnline MPPSC Interactive Form Filling Agent
================================================================================

This agent will help you fill the MPPSC application form automatically.
You will be asked for your details, and the agent will fill the form for you.

================================================================================
📋 MPPSC APPLICATION FORM - PERSONAL DETAILS
================================================================================

Please provide the following information:
(Press Enter to skip and use dummy data)

Exam Type (1: State Service, 2: Forest Service, 3: Both) (default: 3): 
Full Name (default: Test Candidate): John Doe
Father's Name (default: Test Father): 
...

✅ Personal details collected successfully!

================================================================================
📝 COLLECTED DATA SUMMARY
================================================================================
Exam Type: 3
Full Name: John Doe
...

Is this information correct? (yes/no): yes

================================================================================
🚀 STARTING MPONLINE FORM FILLING AGENT
================================================================================

⚠️ IMPORTANT INSTRUCTIONS:
1. A browser window will open automatically
2. The AI agent will navigate and fill the form
3. If the agent gets stuck, it will ask for help
4. Monitor the browser window to see progress
5. Do NOT close the browser window manually

Starting in 3 seconds...

🤖 AI Agent Starting...
📋 Task: Fill MPPSC Application Form
🎯 Exam Type: Both (State Service + Forest Service)

[Agent proceeds to fill the form...]

================================================================================
✅ AGENT COMPLETED SUCCESSFULLY!
================================================================================

📊 Summary:
   ✓ Form accessed
   ✓ Details filled
   ✓ Ready for review

⚠️ NEXT STEPS:
   1. Review the filled form in the browser
   2. Upload required documents if needed
   3. Make payment
   4. Submit the application
```

## Support

If you encounter issues:
1. Check the terminal output for error messages
2. Verify MPOnline website is accessible
3. Ensure your data format is correct
4. Try with dummy data first
5. Check browser console for errors

## License

This tool is for educational and automation purposes. Use responsibly and ensure compliance with MPOnline terms of service.
