"""
MPOnline Interactive Agent
An end-to-end agent that fills MPPSC forms with user interaction when needed.
"""
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from browser_use import Agent, BrowserSession
from playwright.async_api import async_playwright
from browser_use.llm.openai.chat import ChatOpenAI

load_dotenv()

class MPOnlineInteractiveAgent:
    """Interactive agent for MPOnline MPPSC form filling"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.user_data = {}
        self.browser_session = None
        self.llm = None
        
    def get_user_input(self, prompt: str, default: str = "") -> str:
        """Get input from user with optional default value"""
        if default:
            user_input = input(f"{prompt} (default: {default}): ").strip()
            return user_input if user_input else default
        return input(f"{prompt}: ").strip()
    
    def collect_personal_details(self):
        """Collect personal details from user"""
        print("\n" + "="*80)
        print("📋 MPPSC APPLICATION FORM - PERSONAL DETAILS")
        print("="*80)
        print("\nPlease provide the following information:")
        print("(Press Enter to skip and use dummy data)\n")
        
        self.user_data = {
            # Personal Information
            "exam_type": self.get_user_input(
                "Exam Type (1: State Service, 2: Forest Service, 3: Both)", 
                "3"
            ),
            "full_name": self.get_user_input("Full Name", "Test Candidate"),
            "father_name": self.get_user_input("Father's Name", "Test Father"),
            "mother_name": self.get_user_input("Mother's Name", "Test Mother"),
            "dob": self.get_user_input("Date of Birth (DD/MM/YYYY)", "01/01/1995"),
            "gender": self.get_user_input("Gender (Male/Female/Other)", "Male"),
            "category": self.get_user_input("Category (General/OBC/SC/ST)", "General"),
            
            # Contact Information
            "mobile": self.get_user_input("Mobile Number", "9999999999"),
            "email": self.get_user_input("Email Address", "test@example.com"),
            "address": self.get_user_input("Address", "Test Address, Test City"),
            "pincode": self.get_user_input("Pincode", "462001"),
            "district": self.get_user_input("District", "Bhopal"),
            "state": self.get_user_input("State", "Madhya Pradesh"),
            
            # Educational Qualifications
            "qualification": self.get_user_input("Highest Qualification", "Graduate"),
            "university": self.get_user_input("University", "Test University"),
            "passing_year": self.get_user_input("Year of Passing", "2020"),
            "percentage": self.get_user_input("Percentage/CGPA", "75"),
        }
        
        print("\n✅ Personal details collected successfully!")
        return self.user_data
    
    def display_collected_data(self):
        """Display collected data for verification"""
        print("\n" + "="*80)
        print("📝 COLLECTED DATA SUMMARY")
        print("="*80)
        for key, value in self.user_data.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        print("="*80)
        
        confirm = input("\nIs this information correct? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("\n⚠️ Please re-enter the information...")
            return False
        return True
    
    async def run_agent_with_interaction(self):
        """Run the browser agent with interactive capabilities"""
        
        # Collect user details first
        collected = False
        while not collected:
            self.collect_personal_details()
            collected = self.display_collected_data()
        
        print("\n" + "="*80)
        print("🚀 STARTING MPONLINE FORM FILLING AGENT")
        print("="*80)
        print("\n⚠️ IMPORTANT INSTRUCTIONS:")
        print("1. A browser window will open automatically")
        print("2. The AI agent will navigate and fill the form")
        print("3. If the agent gets stuck, it will ask for help")
        print("4. Monitor the browser window to see progress")
        print("5. Do NOT close the browser window manually")
        print("\nStarting in 3 seconds...\n")
        
        await asyncio.sleep(3)
        
        async with async_playwright() as playwright:
            # Initialize LLM
            self.llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
            
            # Initialize Browser Session (headless=False to show browser)
            self.browser_session = BrowserSession(user_data_dir=None)
            
            # Create the comprehensive task for the agent
            task = self.create_task_prompt()
            
            print("\n🤖 AI Agent Starting...")
            print(f"📋 Task: Fill MPPSC Application Form")
            print(f"🎯 Exam Type: {self.get_exam_type_name()}\n")
            
            # Create and run the agent with vision enabled for multilingual support
            agent = Agent(
                task=task,
                llm=self.llm,
                browser_session=self.browser_session,
                use_vision=True,  # Enable vision to read Hindi/English text
                max_failures=5,  # Allow more retries
            )
            
            try:
                result = await agent.run()
                print("\n" + "="*80)
                print("✅ AGENT COMPLETED SUCCESSFULLY!")
                print("="*80)
                print("\n📊 Summary:")
                print("   ✓ Form accessed")
                print("   ✓ Details filled")
                print("   ✓ Ready for review")
                print("\n⚠️ NEXT STEPS:")
                print("   1. Review the filled form in the browser")
                print("   2. Upload required documents if needed")
                print("   3. Make payment")
                print("   4. Submit the application")
                
            except Exception as e:
                print("\n" + "="*80)
                print("❌ ERROR OCCURRED")
                print("="*80)
                print(f"\nError: {str(e)}")
                print("\n💡 SUGGESTIONS:")
                print("   1. Check your internet connection")
                print("   2. Ensure MPOnline website is accessible")
                print("   3. Try running the agent again")
                print("   4. Check if the form structure has changed")
    
    def get_exam_type_name(self):
        """Get exam type name from code"""
        exam_map = {
            "1": "State Service Preliminary Examination 2026",
            "2": "State Forest Service Preliminary Examination 2026",
            "3": "Both (State Service + Forest Service)"
        }
        return exam_map.get(self.user_data.get("exam_type", "3"), "Both")
    
    def create_task_prompt(self) -> str:
        """Create detailed task prompt for the agent"""
        
        # Convert user data to filling instructions
        exam_type_instruction = {
            "1": "Select 'State Service Preliminary Examination 2026' only",
            "2": "Select 'State Forest Service Preliminary Examination 2026' only",
            "3": "Select 'Both (State Service Preliminary Examination 2026 and State Forest Service Preliminary Examination 2026)'"
        }.get(self.user_data.get("exam_type", "3"))
        
        task = f"""
You are an expert multilingual form-filling assistant. Your task is to navigate to the MPOnline website and fill the MPPSC application form with the following details:

# IMPORTANT NOTES:
- The website has content in BOTH Hindi (हिंदी) and English
- You can read and understand BOTH languages
- Field labels may be in Hindi: राज्य सेवा (State Service), वन सेवा (Forest Service), नाम (Name), पिता का नाम (Father's Name), etc.
- Button text may be in Hindi: आवेदन करें (Apply), स्वीकार करें (Accept), आगे बढ़ें (Proceed)
- Work QUICKLY and EFFICIENTLY - fill fields as fast as possible
- Use vision capabilities to read all text accurately

# STEP-BY-STEP INSTRUCTIONS:

## Step 1: Navigate to MPOnline (Hindi/English)
1. Go to the MPOnline website (https://www.mponline.gov.in)
2. Search for "MPPSC" or "एमपीपीएससी" in the search box
3. Look for "State Service Preliminary Examination 2026" OR "राज्य सेवा प्रारंभिक परीक्षा 2026"
4. Click on the exam notification/application link
5. Be prepared to read BOTH Hindi and English text on the page

## Step 2: Access Application Form (Look for Hindi/English)
1. Find and click on "State Service Preliminary Examination 2026" OR "राज्य सेवा प्रारंभिक परीक्षा 2026"
2. Click on "Apply" / "आवेदन करें" OR "Action" / "कार्रवाई" button
3. If there are information links:
   - राज्य सेवा परीक्षा 2026 (State Service Exam)
   - राज्य वन सेवा परीक्षा 2026 (Forest Service Exam)
   Open them in new tabs for reference
4. Return to the main application page

## Step 3: Candidate Declaration (उम्मीदवार घोषणा)
1. Look for "Candidate Declaration" OR "उम्मीदवार घोषणा" section
2. Read the declaration carefully (may be in Hindi/English)
3. Check the checkbox to accept the declaration
4. Click on "I Accept" / "मैं स्वीकार करता हूं" OR "Proceed" / "आगे बढ़ें" button

## Step 4: Fill Personal Details
Fill the form fields with the following information:

**Exam Selection:**
- {exam_type_instruction}

**Personal Information:**
- Full Name: {self.user_data['full_name']}
- Father's Name: {self.user_data['father_name']}
- Mother's Name: {self.user_data['mother_name']}
- Date of Birth: {self.user_data['dob']}
- Gender: {self.user_data['gender']}
- Category: {self.user_data['category']}

**Contact Information:**
- Mobile Number: {self.user_data['mobile']}
- Email Address: {self.user_data['email']}
- Address: {self.user_data['address']}
- Pincode: {self.user_data['pincode']}
- District: {self.user_data['district']}
- State: {self.user_data['state']}

**Educational Qualifications:**
- Highest Qualification: {self.user_data['qualification']}
- University/Board: {self.user_data['university']}
- Year of Passing: {self.user_data['passing_year']}
- Percentage/CGPA: {self.user_data['percentage']}

## Step 5: Important Guidelines (महत्वपूर्ण दिशानिर्देश)
1. Fill the form serially from top to bottom - WORK QUICKLY
2. Field labels may be in Hindi (नाम, पिता का नाम, माता का नाम, जन्म तिथि, etc.) - use vision to read them
3. For dropdown menus, select the appropriate option in Hindi or English
4. Skip optional fields if no data is provided - don't waste time
5. Do NOT click on final "Submit" / "जमा करें" or "Pay" / "भुगतान करें" buttons
6. Stop before payment section - user will complete payment manually
7. OPTIMIZE FOR SPEED - fill fields rapidly without delays

## Step 6: Error Handling (त्रुटि प्रबंधन)
- If you encounter CAPTCHA / कैप्चा, stop and report that manual intervention is needed
- If you get stuck on any field, describe the issue in English
- Error messages may be in Hindi - read them using vision and translate if needed
- If the website structure is different, quickly adapt and find equivalent fields
- For Hindi buttons/links, use context clues and visual recognition
- If absolutely stuck, report the current state concisely

## Step 7: Final Action
Once all details are filled:
1. Review the filled information one more time
2. Report completion status
3. Stop at the review/payment page - DO NOT PROCEED TO PAYMENT
4. Leave the browser open for user to review and complete payment

REMEMBER (याद रखें):
- You can READ and UNDERSTAND both Hindi (हिंदी) and English text
- Use vision capabilities to accurately read field labels in any language
- Common Hindi terms: नाम (Name), पिता (Father), माता (Mother), जन्म तिथि (DOB), मोबाइल (Mobile)
- Work FAST but ACCURATELY - don't wait unnecessarily between fields
- Verify each field after filling
- Stop before payment/submission (भुगतान से पहले रुकें)
"""
        return task

def main():
    """Main entry point"""
    print("\n" + "="*80)
    print("🎓 MPOnline MPPSC Interactive Form Filling Agent")
    print("="*80)
    print("\nThis agent will help you fill the MPPSC application form automatically.")
    print("You will be asked for your details, and the agent will fill the form for you.\n")
    
    agent = MPOnlineInteractiveAgent()
    asyncio.run(agent.run_agent_with_interaction())

if __name__ == "__main__":
    main()
