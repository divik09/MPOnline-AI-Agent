"""Configuration management for MPOnline Agent System."""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
SCREENSHOTS_DIR = DATA_DIR / "screenshots"
LOGS_DIR = DATA_DIR / "logs"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# MPOnline Credentials
MPONLINE_USERNAME = os.getenv("MPONLINE_USERNAME", "")
MPONLINE_PASSWORD = os.getenv("MPONLINE_PASSWORD", "")

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # openai or anthropic
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Database
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", str(DATA_DIR / "checkpoints.db"))

# Browser settings
HEADLESS_MODE = os.getenv("HEADLESS_MODE", "true") == "true"
BROWSER_TIMEOUT = int(os.getenv("BROWSER_TIMEOUT", "30000"))
SLOW_MO = int(os.getenv("SLOW_MO", "0"))

# Real Chrome Browser Connection (Windows)
CHROME_EXECUTABLE_PATH = os.getenv(
    "CHROME_EXECUTABLE_PATH", 
    r"C:\Program Files\Google\Chrome\Application\chrome.exe"
)
CHROME_USER_DATA_DIR = os.getenv(
    "CHROME_USER_DATA_DIR",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
)
CHROME_PROFILE = os.getenv("CHROME_PROFILE", "Default")
USE_REAL_BROWSER = os.getenv("USE_REAL_BROWSER", "false").lower() == "true"

# Browser-use AI automation
USE_AI_AUTOMATION = os.getenv("USE_AI_AUTOMATION", "true").lower() == "true"
BROWSER_USE_TIMEOUT = int(os.getenv("BROWSER_USE_TIMEOUT", "120"))

# Security settings
ENCRYPT_USER_DATA = os.getenv("ENCRYPT_USER_DATA", "true").lower() == "true"
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "")
SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", "1800"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", str(LOGS_DIR / "agent.log"))

# HITL Settings
CAPTCHA_TIMEOUT = int(os.getenv("CAPTCHA_TIMEOUT", "300"))
PAYMENT_TIMEOUT = int(os.getenv("PAYMENT_TIMEOUT", "300"))

# Bot Detection Mitigation
MIN_DELAY = int(os.getenv("MIN_DELAY", "1000"))
MAX_DELAY = int(os.getenv("MAX_DELAY", "3000"))
TYPING_SPEED = int(os.getenv("TYPING_SPEED", "100"))


def validate_config() -> list[str]:
    """
    Validate required configuration settings.
    
    Returns:
        List of error messages for missing/invalid config.
    """
    errors = []
    
    # MPOnline credentials are optional (public portal doesn't require login)
    # Only validate LLM configuration
    
    if LLM_PROVIDER == "openai":
        if not OPENAI_API_KEY or OPENAI_API_KEY.startswith("sk-your"):
            errors.append("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
    elif LLM_PROVIDER == "anthropic":
        if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY.startswith("sk-ant-your"):
            errors.append("ANTHROPIC_API_KEY is required when LLM_PROVIDER=anthropic")
    else:
        errors.append(f"Invalid LLM_PROVIDER: {LLM_PROVIDER}. Must be 'openai' or 'anthropic'")
    
    return errors


def get_llm_config() -> dict:
    """Get LLM configuration based on provider selection."""
    if LLM_PROVIDER == "openai":
        return {
            "provider": "openai",
            "api_key": OPENAI_API_KEY,
            "model": "gpt-4o",
            "temperature": 0.0,
        }
    elif LLM_PROVIDER == "anthropic":
        return {
            "provider": "anthropic",
            "api_key": ANTHROPIC_API_KEY,
            "model": "claude-3-5-sonnet-20241022",
            "temperature": 0.0,
        }
    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")
