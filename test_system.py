"""Quick test script to verify MPOnline Agent functionality."""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src import config
from src.core.graph import create_graph


async def test_system():
    """Test basic system functionality."""
    print("🧪 Testing MPOnline Agent System\n")
    print("=" * 60)
    
    # Test 1: Configuration
    print("\n1️⃣ Testing Configuration...")
    errors = config.validate_config()
    if errors:
        print(f"   ❌ Config errors: {errors}")
        return False
    print("   ✅ Configuration valid!")
    print(f"   📍 LLM Provider: {config.LLM_PROVIDER}")
    
    # Test 2: Graph Creation
    print("\n2️⃣ Testing Graph Creation...")
    try:
        graph = create_graph()
        print("   ✅ Graph created successfully!")
        print(f"   📊 Graph compiled with checkpointer")
    except Exception as e:
        print(f"   ❌ Graph creation failed: {e}")
        return False
    
    # Test 3: Service Templates
    print("\n3️⃣ Testing Service Templates...")
    try:
        from src.services.service_registry import get_service_list
        services = get_service_list()
        print(f"   ✅ Found {len(services)} services:")
        for svc in services:
            print(f"      • {svc['name']} ({svc['key']})")
    except Exception as e:
        print(f"   ❌ Service loading failed: {e}")
        return False
    
    # Test 4: Import all modules
    print("\n4️⃣ Testing Module Imports...")
    modules_to_test = [
        ("Navigator", "src.agents.navigator_node"),
        ("FormExpert", "src.agents.form_expert_node"),
        ("Auditor", "src.agents.auditor_node"),
        ("CAPTCHA", "src.agents.captcha_node"),
        ("Payment", "src.agents.payment_node"),
        ("VisionTool", "src.tools.vision_tool"),
        ("HumanInputTool", "src.tools.human_input_tool"),
        ("BrowserManager", "src.automation.browser_manager"),
    ]
    
    for name, module_path in modules_to_test:
        try:
            __import__(module_path)
            print(f"   ✅ {name}")
        except Exception as e:
            print(f"   ❌ {name}: {e}")
            return False
    
    print("\n" + "=" * 60)
    print("\n🎉 All tests passed! System is ready.\n")
    print("📖 Next steps:")
    print("   1. Open http://localhost:8501 in your browser")
    print("   2. Select 'MPPSC Application'")
    print("   3. Answer the questions")
    print("   4. Watch the automation!")
    print()
    
    return True


if __name__ == "__main__":
    result = asyncio.run(test_system())
    sys.exit(0 if result else 1)
