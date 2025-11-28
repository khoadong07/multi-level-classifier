"""Test script for backend initialization"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("=" * 60)
print("Testing Backend Initialization")
print("=" * 60)

# Test 1: Import modules
print("\n1. Testing imports...")
try:
    from app.core import Config, Classifier, CacheManager, CentralProcessor
    print("   ✅ All imports successful")
except Exception as e:
    print(f"   ❌ Import error: {e}")
    sys.exit(1)

# Test 2: Check .env file
print("\n2. Checking .env file...")
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    print("   ✅ .env file exists")
else:
    print("   ❌ .env file not found")
    print("   Please create .env from .env.example")
    sys.exit(1)

# Test 3: Check prompt template
print("\n3. Checking prompt_template.txt...")
prompt_path = Path(__file__).parent.parent / "prompt_template.txt"
if prompt_path.exists():
    print("   ✅ prompt_template.txt exists")
else:
    print("   ❌ prompt_template.txt not found")
    sys.exit(1)

# Test 4: Validate configuration
print("\n4. Validating configuration...")
try:
    Config.validate()
    print("   ✅ Configuration is valid")
    print(f"   - Model: {Config.MODEL}")
    print(f"   - Base URL: {Config.OPENAI_BASE_URL}")
    print(f"   - Max Workers: {Config.MAX_WORKERS}")
except Exception as e:
    print(f"   ❌ Configuration error: {e}")
    sys.exit(1)

# Test 5: Load prompt template
print("\n5. Loading prompt template...")
try:
    prompt_template = Config.load_prompt_template()
    print(f"   ✅ Prompt template loaded ({len(prompt_template)} characters)")
except Exception as e:
    print(f"   ❌ Failed to load prompt template: {e}")
    sys.exit(1)

# Test 6: Initialize components
print("\n6. Initializing components...")
try:
    classifier = Classifier(
        base_url=Config.OPENAI_BASE_URL,
        api_key=Config.OPENAI_API_KEY,
        model=Config.MODEL,
        prompt_template=prompt_template,
        temperature=Config.TEMPERATURE,
        max_tokens=Config.MAX_TOKENS
    )
    print("   ✅ Classifier initialized")
    
    cache_manager = CacheManager(Config.CACHE_FILE)
    print(f"   ✅ CacheManager initialized (cache size: {len(cache_manager.cache)})")
    
    processor = CentralProcessor(classifier, cache_manager, Config.MAX_WORKERS)
    print("   ✅ CentralProcessor initialized")
    
except Exception as e:
    print(f"   ❌ Initialization error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 7: Check directories
print("\n7. Checking directories...")
upload_dir = Path(__file__).parent.parent / "uploads"
output_dir = Path(__file__).parent.parent / "outputs"

if not upload_dir.exists():
    upload_dir.mkdir(exist_ok=True)
    print("   ✅ Created uploads directory")
else:
    print("   ✅ uploads directory exists")

if not output_dir.exists():
    output_dir.mkdir(exist_ok=True)
    print("   ✅ Created outputs directory")
else:
    print("   ✅ outputs directory exists")

print("\n" + "=" * 60)
print("✅ All tests passed! Backend is ready to run.")
print("=" * 60)
print("\nTo start the backend, run:")
print("  uvicorn backend.main:app --reload")
print("\nOr use the run script:")
print("  cd backend && ./run.sh")
