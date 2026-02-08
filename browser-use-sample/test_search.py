"""
Quick test script for the browser-use sample project.
"""
import asyncio
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from search_assistant import SearchAssistant


async def test_search():
    """Test the search assistant."""
    
    print("\n🧪 Testing Browser-Use Search Assistant")
    print("=" * 60)
    
    assistant = SearchAssistant()
    
    # Test query
    query = "Find MPOnline MPPSC official website"
    
    print(f"\n📝 Test Query: {query}\n")
    
    try:
        result = await assistant.search(query)
        
        print("\n" + "=" * 60)
        print("✅ TEST PASSED!")
        print("=" * 60)
        print(f"\nResult: {result}")
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ TEST FAILED!")
        print("=" * 60)
        print(f"\nError: {e}")
        
        import traceback
        traceback.print_exc()
        
        return False


if __name__ == "__main__":
    success = asyncio.run(test_search())
    
    input("\nPress ENTER to exit...")
    
    sys.exit(0 if success else 1)
