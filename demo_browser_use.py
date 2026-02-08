"""
Live demo of browser-use AI automation for MPPSC form filling.

This script demonstrates the complete workflow:
1. Google search for "MPOnline MPPSC"
2. Navigate to the official portal
3. Find the MPPSC application form
4. Fill the form with sample data using AI
"""
import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.core.agent_state import AgentState
from src.agents.browser_use_node import browser_use_node
from src.utils.logging_config import logger
import time


async def demonstrate_browser_use():
    """
    Live demonstration of AI-powered browser automation.
    
    This will:
    - Search Google for MPOnline MPPSC
    - Navigate to the portal
    - Fill the application form
    - Show you the AI working in real-time!
    """
    
    print("\n" + "=" * 80)
    print("🤖 BROWSER-USE AI AUTOMATION - LIVE DEMO")
    print("=" * 80)
    print("\nThis demo will show AI-powered browser automation in action!")
    print("The browser will open and you'll see the AI:")
    print("  1. Search Google for 'MPOnline MPPSC application'")
    print("  2. Click on the official MPOnline link")
    print("  3. Navigate to the MPPSC application section")
    print("  4. Fill out the form with the test data below")
    print("\n" + "-" * 80)
    
    # Sample test data
    test_data = {
        "full_name": "Amit Kumar Sharma",
        "father_name": "Rajesh Kumar Sharma",
        "mother_name": "Sunita Sharma",
        "date_of_birth": "15/08/1995",
        "gender": "Male",
        "category": "General",
        "email": "amit.sharma@example.com",
        "mobile": "9876543210",
        "address": "123, Nehru Nagar, Bhopal",
        "district": "Bhopal",
        "state": "Madhya Pradesh",
        "pincode": "462001",
        "qualification": "Bachelor of Technology"
    }
    
    print("\n📋 Test Data:")
    for key, value in test_data.items():
        print(f"   • {key.replace('_', ' ').title()}: {value}")
    
    print("\n" + "-" * 80)
    print("\n⚙️  Configuration:")
    print("   • Automation Mode: AI-Powered (browser-use)")
    print("   • Browser: Visible (you can watch!)")
    print("   • Service: MPPSC Application")
    print("\n" + "-" * 80)
    
    input("\n👉 Press ENTER to start the AI automation demo...")
    
    # Create agent state
    print("\n🔧 Initializing agent state...")
    state: AgentState = {
        "user_data": test_data,
        "service_type": "mppsc",
        "use_ai_automation": True,  # Enable AI mode
        "current_step": "start",
        "form_progress": {},
        "dom_snapshot": None,
        "screenshot_path": None,
        "current_url": None,
        "session_data": {},
        "errors": [],
        "messages": [],
        "next_action": "navigate",
        "captcha_solution": None,
        "payment_confirmed": False,
        "attempt_count": {},
        "start_time": time.time(),
        "last_update_time": time.time()
    }
    
    print("✅ State initialized")
    
    # Run browser-use automation
    print("\n🚀 Starting AI-powered browser automation...")
    print("\n📺 Watch the browser window - AI is now working!\n")
    print("The AI will:")
    print("   ⏳ Think about what to do")
    print("   👀 Observe the page")
    print("   🖱️  Take actions (click, type, navigate)")
    print("   🔄 Repeat until form is filled")
    
    print("\n" + "=" * 80)
    print("🤖 AI AGENT RUNNING... (this may take 1-2 minutes)")
    print("=" * 80 + "\n")
    
    start_time = time.time()
    
    try:
        result = await browser_use_node(state)
        
        duration = time.time() - start_time
        
        print("\n" + "=" * 80)
        print(f"✅ AI AUTOMATION COMPLETED in {duration:.1f} seconds!")
        print("=" * 80)
        
        # Show results
        print("\n📊 Results:")
        print(f"   • Final Step: {result.get('current_step')}")
        print(f"   • Current URL: {result.get('current_url', 'N/A')}")
        print(f"   • Errors: {len(result.get('errors', []))}")
        
        if result.get('screenshot_path'):
            print(f"   • Screenshot: {result.get('screenshot_path')}")
        
        form_progress = result.get('form_progress', {})
        if form_progress:
            filled = sum(1 for v in form_progress.values() if v)
            total = len(form_progress)
            print(f"   • Form Progress: {filled}/{total} fields ({filled/total*100:.1f}%)")
        
        if result.get('current_step') == 'form_filled':
            print("\n🎉 SUCCESS! Form has been filled by AI!")
            print("\n📝 Next Steps:")
            print("   1. Check the browser (should still be open)")
            print("   2. Verify the form data is correct")
            print("   3. Solve any CAPTCHA if present")
            print("   4. Click submit to complete the application")
        elif result.get('errors'):
            print("\n⚠️  AI encountered some issues:")
            for error in result.get('errors', []):
                print(f"   • {error}")
        
        print("\n" + "=" * 80)
        
        return result.get('current_step') == 'form_filled'
        
    except Exception as e:
        print(f"\n❌ Error during automation: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main entry point."""
    print("\n🎯 MPOnline Agent - Browser-Use AI Automation Demo")
    print("   This demonstration shows AI filling an MPPSC form automatically\n")
    
    success = await demonstrate_browser_use()
    
    if success:
        print("\n✅ Demo completed successfully!")
        print("\n💡 To use this in the Streamlit UI:")
        print("   1. Run: streamlit run streamlit_app/app.py")
        print("   2. Select '🤖 AI-Powered (Recommended)' mode")
        print("   3. Choose MPPSC Application")
        print("   4. Fill in your details")
        print("   5. Watch the AI work!\n")
    else:
        print("\n⚠️  Demo encountered issues")
        print("   Check the error messages above for details\n")
    
    return success


if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\n⏸️  Demo interrupted by user\n")
        sys.exit(0)
