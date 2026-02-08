"""End-to-end test for MPPSC form filling automation."""
import asyncio
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.core.graph import create_graph, run_graph
from src.core.agent_state import AgentState
from src.automation.browser_manager import browser_manager
from src.utils.logging_config import logger


async def test_mppsc_form_filling():
    """Test MPPSC form filling with sample data."""
    
    print("\n" + "=" * 70)
    print("🧪 MPPSC FORM FILLING - END-TO-END TEST")
    print("=" * 70)
    
    # Sample test data for MPPSC application
    test_user_data = {
        "full_name": "Rajesh Kumar Singh",
        "father_name": "Ram Kumar Singh",
        "mother_name": "Sita Devi Singh",
        "date_of_birth": "15/06/1995",
        "gender": "Male",
        "category": "General",
        "email": "rajesh.kumar@example.com",
        "mobile": "9876543210",
        "address": "123, Gandhi Road, Indore",
        "district": "Indore",
        "state": "Madhya Pradesh",
        "pincode": "452001",
        "qualification": "Bachelor of Engineering",
    }
    
    print("\n📝 Test Data:")
    print("-" * 70)
    for key, value in test_user_data.items():
        print(f"   {key:20s}: {value}")
    print("-" * 70)
    
    # Create initial state
    print("\n🔧 Creating agent state...")
    initial_state: AgentState = {
        "user_data": test_user_data,
        "service_type": "mppsc",
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
    
    print("✅ Agent state created")
    
    # Create graph
    print("\n🔧 Creating LangGraph workflow...")
    graph = create_graph()
    print("✅ Graph compiled successfully")
    
    # Start browser
    print("\n🌐 Starting browser...")
    try:
        page = await browser_manager.start()
        print(f"✅ Browser started (headless={not page._is_closed()})")
    except Exception as e:
        print(f"❌ Browser start failed: {e}")
        return False
    
    # Run the workflow
    print("\n🚀 Starting automation workflow...")
    print("-" * 70)
    
    thread_id = f"test_mppsc_{int(time.time())}"
    
    try:
        print(f"📍 Thread ID: {thread_id}")
        print("\n⏳ Running agents (this may take a minute)...")
        print("\nAgent steps:")
        
        # Run graph with streaming to show progress
        config_dict = {"configurable": {"thread_id": thread_id}}
        
        step_count = 0
        final_state = None
        
        async for state in graph.astream(initial_state, config_dict):
            step_count += 1
            # Get the node that just executed from state
            if state:
                current_step = list(state.keys())[0] if state else "unknown"
                state_data = list(state.values())[0] if state else {}
                
                print(f"\n   Step {step_count}: {current_step}")
                
                # Show current step and URL if available
                if isinstance(state_data, dict):
                    if "current_step" in state_data:
                        print(f"      Current step: {state_data.get('current_step')}")
                    if "current_url" in state_data:
                        print(f"      URL: {state_data.get('current_url', 'N/A')}")
                    if "errors" in state_data and state_data.get("errors"):
                        print(f"      ⚠️  Errors: {state_data.get('errors')}")
                    if "form_progress" in state_data:
                        filled = sum(1 for v in state_data.get("form_progress", {}).values() if v)
                        total = len(state_data.get("form_progress", {}))
                        if total > 0:
                            print(f"      Form progress: {filled}/{total} fields")
                
                final_state = state_data
        
        print("\n" + "-" * 70)
        print(f"\n✅ Workflow completed! ({step_count} steps executed)")
        
        # Show final state
        if final_state:
            print("\n📊 Final State Summary:")
            print(f"   Current step: {final_state.get('current_step', 'N/A')}")
            print(f"   Errors: {len(final_state.get('errors', []))}")
            if final_state.get('screenshot_path'):
                print(f"   Screenshot: {final_state.get('screenshot_path')}")
            
            # Show form progress
            form_progress = final_state.get('form_progress', {})
            if form_progress:
                filled = sum(1 for v in form_progress.values() if v)
                total = len(form_progress)
                print(f"   Form filled: {filled}/{total} fields ({filled/total*100:.1f}%)")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        return False
        
    except Exception as e:
        print(f"\n\n❌ Error during workflow: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Cleanup
        print("\n🧹 Cleaning up...")
        await browser_manager.close()
        print("✅ Browser closed")


async def main():
    """Main test function."""
    print("\n🎯 MPOnline Agent - MPPSC Form Filling Test")
    print("   This test will navigate to MPOnline and attempt to fill")
    print("   the MPPSC application form with sample data.\n")
    
    success = await test_mppsc_form_filling()
    
    print("\n" + "=" * 70)
    if success:
        print("✅ TEST COMPLETED SUCCESSFULLY!")
        print("\n📋 Next Steps:")
        print("   1. Check screenshots in data/screenshots/")
        print("   2. Review logs in data/logs/agent.log")
        print("   3. Try the Streamlit UI at http://localhost:8501")
    else:
        print("❌ TEST FAILED")
        print("\n📋 Troubleshooting:")
        print("   1. Check logs in data/logs/agent.log")
        print("   2. Ensure internet connection is working")
        print("   3. Verify MPOnline portal is accessible")
    print("=" * 70 + "\n")
    
    return success


if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
        sys.exit(1)
