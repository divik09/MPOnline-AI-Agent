"""
End-to-end test for Agentic Browser Application.
Tests the complete flow: "I want to apply for MPPSC"
"""
import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.agents.agentic_browser_agent import AgenticBrowserAgent


async def test_mppsc_application():
    """
    Test complete MPPSC application flow.
    """
    print("\n" + "=" * 80)
    print("🧪 END-TO-END TEST: MPPSC Application")
    print("=" * 80)
    
    # Sample user data
    test_data = {
        "full_name": "Rajesh Kumar Sharma",
        "email": "rajesh.sharma@example.com",
        "mobile": "9876543210"
    }
    
    print("\n📋 Test Data:")
    for key, value in test_data.items():
        print(f"   • {key}: {value}")
    
    print("\n🚀 Starting Agentic Browser Agent...")
    print("   This will try multiple strategies until it succeeds!\n")
    
    # Create agent
    agent = AgenticBrowserAgent()
    
    try:
        # Run the agentic workflow
        result = await agent.run(
            goal="Fill out MPPSC application form",
            service_type="mppsc",
            user_data=test_data
        )
        
        print("\n" + "=" * 80)
        print("📊 TEST RESULTS")
        print("=" * 80)
        
        print(f"\n✅ Success: {result.get('success')}")
        print(f"📈 Total Attempts: {result.get('attempt_count')}")
        print(f"🎯 Strategies Tried: {', '.join(result.get('strategies_tried', []))}")
        print(f"💭 Final Reasoning: {result.get('reasoning')}")
        
        if result.get('errors'):
            print(f"\n⚠️  Errors Encountered: {len(result.get('errors'))}")
            for i, error in enumerate(result['errors'], 1):
                print(f"   {i}. {error}")
        
        if result.get('success'):
            print("\n🎉 TEST PASSED!")
            print("   The agent successfully completed the MPPSC application flow.")
        else:
            print("\n❌ TEST FAILED")
            print("   The agent exhausted all strategies without success.")
        
        print("\n" + "=" * 80)
        
        return result.get('success')
        
    except Exception as e:
        print(f"\n❌ TEST ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_simple_navigation():
    """
    Simple test to verify basic browser-use functionality.
    """
    print("\n" + "=" * 80)
    print("🧪 SIMPLE TEST: Basic Navigation")
    print("=" * 80)
    
    try:
        from browser_use import Agent
        from src.utils.browser_use_helper import get_configured_llm
        
        llm = get_configured_llm()
        print("✅ LLM configured")
        
        task = """
        1. Go to google.com
        2. Search for "MPOnline official website"
        3. Stop after seeing search results
        """
        
        print(f"\n📝 Task: {task}")
        print("\n🌐 Opening browser and executing task...")
        
        agent = Agent(task=task, llm=llm)
        result = await agent.run()
        
        print("\n✅ Simple navigation test PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ Simple test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests."""
    print("\n🎯 AGENTIC BROWSER APPLICATION - FULL TEST SUITE")
    print("Testing: 'I want to apply for MPPSC' workflow\n")
    
    # Test 1: Simple navigation
    print("TEST 1: Simple Navigation")
    simple_passed = await test_simple_navigation()
    
    if simple_passed:
        # Test 2: Full MPPSC application
        print("\n\nTEST 2: Full MPPSC Application Flow")
        full_passed = await test_mppsc_application()
        
        if full_passed:
            print("\n\n✅ ALL TESTS PASSED!")
            print("The agentic browser application is working correctly.")
        else:
            print("\n\n⚠️  Full test failed but simple test passed.")
            print("The browser-use integration works, but the agentic workflow needs debugging.")
    else:
        print("\n\n❌ Simple test failed - browser-use may not be configured correctly.")
        print("Please check:")
        print("  1. OPENAI_API_KEY or ANTHROPIC_API_KEY is set in .env")
        print("  2. browser-use is installed: pip install browser-use")
        print("  3. Chrome/Chromium browser is available")
    
    return simple_passed and (full_passed if simple_passed else False)


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏸️  Tests interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
