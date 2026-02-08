# Quick Verification Script
# This script verifies that the environment is set up correctly

import sys
print("=" * 60)
print("MPOnline Agent - Environment Verification")
print("=" * 60)

# Check Python version
print(f"\n✓ Python Version: {sys.version}")

# Check required packages
packages_to_check = [
    "langgraph",
    "streamlit", 
    "openai",
    "requests",
    "browser_use",
    "playwright",
    "langchain",
    "langchain_openai",
    "langchain_google_genai",
    "dotenv"
]

print("\nChecking installed packages:")
print("-" * 60)

all_good = True
for package in packages_to_check:
    try:
        __import__(package)
        print(f"✓ {package:30s} - OK")
    except ImportError as e:
        print(f"✗ {package:30s} - MISSING")
        all_good = False

# Check environment variables
print("\nChecking environment variables:")
print("-" * 60)

import os
from dotenv import load_dotenv
load_dotenv()

env_vars = ["OPENAI_API_KEY"]
for var in env_vars:
    value = os.getenv(var)
    if value:
        # Show only first 10 chars for security
        masked = value[:10] + "..." if len(value) > 10 else "***"
        print(f"✓ {var:30s} - Set ({masked})")
    else:
        print(f"⚠ {var:30s} - NOT SET")

print("\n" + "=" * 60)
if all_good:
    print("✓ Environment is ready to run MPOnlineFlight.py!")
else:
    print("✗ Some packages are missing. Please check installation.")
print("=" * 60)
