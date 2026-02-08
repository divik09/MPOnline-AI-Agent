from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

load_dotenv()

print("Testing ChatOpenAI initialization...")
print(f"OPENAI_API_KEY is set: {bool(os.getenv('OPENAI_API_KEY'))}")

try:
    llm = ChatOpenAI(model="gpt-4o")
    print("✓ ChatOpenAI initialized successfully with defaults")
except Exception as e:
    print(f"✗ Error with defaults: {e}")

try:
    llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
    print("✓ ChatOpenAI initialized successfully with temperature")
except Exception as e:
    print(f"✗ Error with temperature: {e}")
