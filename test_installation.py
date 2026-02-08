"""Simple test runner to verify installation."""
import sys


def test_imports():
    """Test that all required packages can be imported."""
    print("Testing imports...")
    
    try:
        import langchain
        print("✅ langchain")
    except ImportError as e:
        print(f"❌ langchain: {e}")
        return False
    
    try:
        import langgraph
        print("✅ langgraph")
    except ImportError as e:
        print(f"❌ langgraph: {e}")
        return False
    
    try:
        import playwright
        print("✅ playwright")
    except ImportError as e:
        print(f"❌ playwright: {e}")
        return False
    
    try:
        import streamlit
        print("✅ streamlit")
    except ImportError as e:
        print(f"❌ streamlit: {e}")
        return False
    
    try:
        import structlog
        print("✅ structlog")
    except ImportError as e:
        print(f"❌ structlog: {e}")
        return False
    
    try:
        from cryptography.fernet import Fernet
        print("✅ cryptography")
    except ImportError as e:
        print(f"❌ cryptography: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv")
    except ImportError as e:
        print(f"❌ python-dotenv: {e}")
        return False
    
    print("\n✅ All imports successful!")
    return True


def test_project_structure():
    """Test that project structure is correct."""
    print("\nTesting project structure...")
    
    from pathlib import Path
    
    required_dirs = [
        "src",
        "src/core",
        "src/agents",
        "src/automation",
        "src/tools",
        "src/services",
        "src/utils",
        "streamlit_app",
        "data"
    ]
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} not found")
            return False
    
    print("\n✅ Project structure is correct!")
    return True


def test_config():
    """Test configuration loading."""
    print("\nTesting configuration...")
    
    try:
        from src import config
        print("✅ Configuration module loaded")
        
        # Test if .env exists
        from pathlib import Path
        if Path(".env").exists():
            print("✅ .env file found")
        else:
            print("⚠️  .env file not found (use .env.template)")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


if __name__ == "__main__":
    print("🧪 MPOnline Agent - Installation Test\n")
    print("=" * 50)
    
    success = True
    
    success &= test_imports()
    success &= test_project_structure()
    success &= test_config()
    
    print("\n" + "=" * 50)
    
    if success:
        print("\n✅ All tests passed! System is ready.")
        print("\n📖 Next steps:")
        print("1. Configure .env file")
        print("2. Run: streamlit run streamlit_app/app.py")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)
