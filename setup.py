"""Setup script for MPOnline Agent."""
import subprocess
import sys
from pathlib import Path


def main():
    """Run setup tasks."""
    print("🚀 Setting up MPOnline Agent...\n")
    
    # Check Python version
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required")
        sys.exit(1)
    
    print("✅ Python version check passed")
    
    # Install requirements
    print("\n📦 Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    print("\n🌐 Installing Playwright browsers...")
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"])
    
    # Create .env if not exists
    env_file = Path(".env")
    env_template = Path(".env.template")
    
    if not env_file.exists() and env_template.exists():
        print("\n📝 Creating .env file from template...")
        env_file.write_text(env_template.read_text())
        print("⚠️  Please edit .env file with your credentials!")
    
    # Create data directories
    print("\n📁 Creating data directories...")
    (Path("data") / "screenshots").mkdir(parents=True, exist_ok=True)
    (Path("data") / "logs").mkdir(parents=True, exist_ok=True)
    (Path("data") / "uploads").mkdir(parents=True, exist_ok=True)
    
    print("\n✅ Setup complete!")
    print("\n📖 Next steps:")
    print("1. Edit .env file with your credentials")
    print("2. Run: streamlit run streamlit_app/app.py")


if __name__ == "__main__":
    main()
