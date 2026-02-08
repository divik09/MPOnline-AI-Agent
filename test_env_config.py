"""
Quick test to verify .env configuration and API connectivity.
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# Load environment
load_dotenv()

print("\n" + "=" * 80)
print("🔍 TESTING .ENV CONFIGURATION")
print("=" * 80)

# Check environment variables
openai_key = os.getenv('OPENAI_API_KEY', '')
anthropic_key = os.getenv('ANTHROPIC_API_KEY', '')
llm_provider = os.getenv('LLM_PROVIDER', 'openai')

print("\n📋 Environment Variables:")
print(f"   • LLM_PROVIDER: {llm_provider}")
print(f"   • OPENAI_API_KEY: {'✅ Set (' + openai_key[:15] + '...)' if openai_key else '❌ Not set'}")
print(f"   • ANTHROPIC_API_KEY: {'✅ Set (' + anthropic_key[:15] + '...)' if anthropic_key else '❌ Not set'}")

# Test LLM connection
print("\n🧪 Testing LLM Connection...")

try:
    if llm_provider == "openai" and openai_key:
        print("   Testing OpenAI connection...")
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        response = llm.invoke("Say 'Hello!' in one word.")
        print(f"   ✅ OpenAI working! Response: {response.content}")
        
    elif llm_provider == "anthropic" and anthropic_key:
        print("   Testing Anthropic connection...")
        llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)
        response = llm.invoke("Say 'Hello!' in one word.")
        print(f"   ✅ Anthropic working! Response: {response.content}")
        
    else:
        print(f"   ❌ No valid API key found for provider: {llm_provider}")
        print("\n💡 Action Required:")
        print("   1. Open .env file")
        print("   2. Set OPENAI_API_KEY=sk-your-key-here")
        print("   3. Or set ANTHROPIC_API_KEY=sk-ant-your-key-here")
        exit(1)
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED!")
    print("=" * 80)
    print("\n🚀 You're ready to use:")
    print("   • python simple_visual_demo.py (browser demo)")
    print("   • python demo_browser_use.py (full demo)")
    print("   • http://localhost:8505 (agentic chat app)")
    print("\n")
    
except Exception as e:
    print(f"\n❌ LLM Test Failed: {e}")
    print("\n💡 Common Issues:")
    print("   • Invalid API key")
    print("   • Network connection problem")
    print("   • API key doesn't have access to the model")
    print("\n")
    exit(1)
