#!/usr/bin/env python3
"""Check environment configuration for backend"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

# Load .env from parent directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

print("=" * 60)
print("SPX Classification Backend - Environment Check")
print("=" * 60)

# Check .env file
print(f"\n📁 .env file: {env_path}")
if env_path.exists():
    print("   ✅ Found")
else:
    print("   ❌ Not found")
    print("   Please create .env file from .env.example")
    sys.exit(1)

# Check required variables
print("\n🔑 Required Variables:")
required_vars = {
    "OPENAI_API_KEY": "OpenAI API Key",
    "OPENAI_BASE_URL": "API Base URL",
    "MODEL": "Model name"
}

all_ok = True
for var, description in required_vars.items():
    value = os.getenv(var)
    if value and value != "DUMMY_KEY":
        # Mask API key
        if "KEY" in var:
            display_value = value[:10] + "..." if len(value) > 10 else "***"
        else:
            display_value = value
        print(f"   ✅ {var}: {display_value}")
    else:
        print(f"   ❌ {var}: Not set")
        all_ok = False

# Check optional variables
print("\n⚙️  Optional Variables:")
optional_vars = {
    "MAX_WORKERS": "10",
    "MAX_RETRY": "3",
    "RETRY_WAIT": "0.5",
    "TEMPERATURE": "0",
    "MAX_TOKENS": "150"
}

for var, default in optional_vars.items():
    value = os.getenv(var, default)
    print(f"   • {var}: {value}")

# Check prompt template
print("\n📄 Files:")
prompt_file = Path(__file__).parent.parent / "prompt_template.txt"
if prompt_file.exists():
    print(f"   ✅ prompt_template.txt: Found ({prompt_file.stat().st_size} bytes)")
else:
    print(f"   ❌ prompt_template.txt: Not found")
    all_ok = False

print("\n" + "=" * 60)
if all_ok:
    print("✅ All checks passed! You can start the backend.")
    print("\nRun: cd backend && uvicorn main:app --reload")
else:
    print("❌ Configuration incomplete. Please fix the issues above.")
    sys.exit(1)

print("=" * 60)
