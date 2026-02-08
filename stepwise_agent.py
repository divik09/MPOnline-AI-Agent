"""
MPOnline Step-by-Step Agent
Asks for help when stuck and waits for user response
"""
import asyncio
import os
from dotenv import load_dotenv
from browser_use import Agent, BrowserSession
from browser_use.llm.openai.chat import ChatOpenAI

load_dotenv()

def ask_user(question: str) -> str:
    """Ask user a question and wait for response"""
    print("\n" + "="*60)
    print("🤔 AGENT NEEDS YOUR HELP:")
    print("="*60)
    print(f"\n{question}\n")
    response = input("👉 Your response: ").strip()
    print("="*60 + "\n")
    return response

async def step_by_step_agent():
    """Run agent step by step with user interaction"""
    
    print("\n" + "="*80)
    print("📝 MPOnline MPPSC Form Filler - Step by Step Mode")
    print("="*80)
    print("\n✨ This agent will:")
    print("   - Work step by step")
    print("   - Ask for your help if stuck")
    print("   - Wait for your response before continuing")
    print("\n")
    
    # Initialize browser
    async with async_playwright() as playwright:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        browser_session = BrowserSession(user_data_dir=None)
        
        # STEP 1: Navigate to MPOnline
        print("="*60)
        print("📍 STEP 1: Navigate to MPOnline website")
        print("="*60)
        
        step1_task = """
        Navigate to https://www.mponline.gov.in
        
        After you reach the website:
        - Describe what you see on the page
        - Tell me what buttons/links are visible
        - Report done when page is loaded
        """
        
        agent1 = Agent(
            task=step1_task,
            llm=llm,
            browser_session=browser_session,
            use_vision=False,
            max_failures=2,
        )
        
        try:
            await asyncio.wait_for(agent1.run(), timeout=30.0)
            print("\n✅ Step 1 completed!")
        except asyncio.TimeoutError:
            response = ask_user("Step 1 took too long. What do you see in the browser? Should I continue? (yes/no)")
            if response.lower() != 'yes':
                print("Stopping as requested.")
                return
        except Exception as e:
            response = ask_user(f"Error in Step 1: {str(e)}\nShould I continue? (yes/no)")
            if response.lower() != 'yes':
                return
        
        # STEP 2: Search for MPPSC
        print("\n" + "="*60)
        print("📍 STEP 2: Search for MPPSC exam")
        print("="*60)
        
        step2_task = """
        On the MPOnline website:
        1. Find the search box
        2. Type "MPPSC" in the search box
        3. Press Enter or click search
        4. Report what results appear
        """
        
        agent2 = Agent(
            task=step2_task,
            llm=llm,
            browser_session=browser_session,
            use_vision=False,
            max_failures=2,
        )
        
        try:
            await asyncio.wait_for(agent2.run(), timeout=30.0)
            print("\n✅ Step 2 completed!")
        except asyncio.TimeoutError:
            response = ask_user("Step 2 took too long. Can you see search results? What should I search for?")
            if not response:
                return
        except Exception as e:
            response = ask_user(f"Error in Step 2: {str(e)}\nWhat should I do next?")
        
        # STEP 3: Find MPPSC 2026 exam
        print("\n" + "="*60)
        print("📍 STEP 3: Find State Service Exam 2026")
        print("="*60)
        
        step3_task = """
        In the search results:
        1. Look for "State Service Preliminary Examination 2026"
        2. OR look for "MPPSC 2026"
        3. Click on the exam link
        4. Report what page opens
        """
        
        agent3 = Agent(
            task=step3_task,
            llm=llm,
            browser_session=browser_session,
            use_vision=False,
            max_failures=2,
        )
        
        try:
            await asyncio.wait_for(agent3.run(), timeout=30.0)
            print("\n✅ Step 3 completed!")
        except asyncio.TimeoutError:
            response = ask_user("Step 3 took too long. Can you see the exam link? What should I click on?")
        except Exception as e:
            response = ask_user(f"Error in Step 3: {str(e)}\nWhat do you see on the page?")
        
        # STEP 4: Click Apply
        print("\n" + "="*60)
        print("📍 STEP 4: Click Apply button")
        print("="*60)
        
        step4_task = """
        On the exam page:
        1. Find the "Apply" or "आवेदन करें" button
        2. Click on it
        3. Report what happens
        """
        
        agent4 = Agent(
            task=step4_task,
            llm=llm,
            browser_session=browser_session,
            use_vision=False,
            max_failures=2,
        )
        
        try:
            await asyncio.wait_for(agent4.run(), timeout=30.0)
            print("\n✅ Step 4 completed!")
        except asyncio.TimeoutError:
            response = ask_user("Step 4 took too long. Where is the Apply button?")
        except Exception as e:
            response = ask_user(f"Error in Step 4: {str(e)}\nWhat button should I click?")
        
        # STEP 5: Accept Declaration
        print("\n" + "="*60)
        print("📍 STEP 5: Accept Declaration")
        print("="*60)
        
        step5_task = """
        If there is a declaration page:
        1. Check any checkbox for acceptance
        2. Click "I Accept" or "स्वीकार करें" button
        3. Report the current page
        """
        
        agent5 = Agent(
            task=step5_task,
            llm=llm,
            browser_session=browser_session,
            use_vision=False,
            max_failures=2,
        )
        
        try:
            await asyncio.wait_for(agent5.run(), timeout=30.0)
            print("\n✅ Step 5 completed!")
        except asyncio.TimeoutError:
            response = ask_user("Step 5 took too long. Is there a declaration? Should I skip?")
        except Exception as e:
            response = ask_user(f"Error in Step 5: {str(e)}\nNo declaration found?")
        
        # STEP 6: Fill Form
        print("\n" + "="*60)
        print("📍 STEP 6: Fill the Application Form")
        print("="*60)
        
        test_data = {
            "name": "Test Candidate Demo",
            "father": "Test Father",
            "mother": "Test Mother",
            "dob": "01/01/1995",
            "mobile": "9876543210",
            "email": "test@example.com"
        }
        
        print("\n📋 Will use this test data:")
        for k, v in test_data.items():
            print(f"   {k}: {v}")
        
        confirm = ask_user("Should I fill the form with this data? (yes to continue)")
        
        if confirm.lower() == 'yes':
            step6_task = f"""
            Fill the application form with:
            - Name: {test_data['name']}
            - Father's Name: {test_data['father']}
            - Mother's Name: {test_data['mother']}
            - DOB: {test_data['dob']}
            - Mobile: {test_data['mobile']}
            - Email: {test_data['email']}
            
            Fill any other required fields with appropriate test data.
            DO NOT click submit or pay.
            Report what fields you filled.
            """
            
            agent6 = Agent(
                task=step6_task,
                llm=llm,
                browser_session=browser_session,
                use_vision=False,
                max_failures=3,
            )
            
            try:
                await asyncio.wait_for(agent6.run(), timeout=60.0)
                print("\n✅ Step 6 completed!")
            except asyncio.TimeoutError:
                ask_user("Step 6 took too long. What fields are visible? Help me understand the form.")
            except Exception as e:
                ask_user(f"Error in Step 6: {str(e)}\nCan you describe the form fields?")
        
        # Final
        print("\n" + "="*80)
        print("✅ PROCESS COMPLETE")
        print("="*80)
        print("\n📺 Check the browser window for results")
        print("💡 Review the filled form before payment")
        print("⚠️  Agent stopped before payment - complete manually\n")
        
        input("Press Enter to close the browser...")

if __name__ == "__main__":
    from playwright.async_api import async_playwright
    asyncio.run(step_by_step_agent())
