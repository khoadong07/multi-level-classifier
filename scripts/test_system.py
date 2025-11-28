"""Test script for the classification system"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core import Config, Classifier, CacheManager, CentralProcessor
from app.models import ClassificationTask


def test_classifier():
    """Test the classifier with a sample feedback"""
    print("Testing Classifier...")
    
    try:
        Config.validate()
        prompt_template = Config.load_prompt_template()
        
        classifier = Classifier(
            base_url=Config.OPENAI_BASE_URL,
            api_key=Config.OPENAI_API_KEY,
            model=Config.MODEL,
            prompt_template=prompt_template
        )
        
        # Test feedback
        test_feedback = "Tài xế giao hàng rất nhanh và thái độ tốt"
        
        print(f"Feedback: {test_feedback}")
        result = classifier.classify(test_feedback)
        print(f"Result: {result}")
        
        if result:
            print("✅ Classifier test passed!")
        else:
            print("❌ Classifier test failed - no result")
    
    except Exception as e:
        print(f"❌ Classifier test failed: {e}")


def test_cache():
    """Test the cache manager"""
    print("\nTesting Cache Manager...")
    
    try:
        cache = CacheManager("test_cache.json")
        
        # Test set and get
        cache.set("test_key", "RIDER / Driver Compensation & Benefits / Income")
        result = cache.get("test_key")
        
        if result:
            print(f"Cache get result: {result}")
            print("✅ Cache test passed!")
        else:
            print("❌ Cache test failed")
        
        # Cleanup
        Path("test_cache.json").unlink(missing_ok=True)
    
    except Exception as e:
        print(f"❌ Cache test failed: {e}")


def test_processor():
    """Test the central processor"""
    print("\nTesting Central Processor...")
    
    try:
        Config.validate()
        prompt_template = Config.load_prompt_template()
        
        classifier = Classifier(
            base_url=Config.OPENAI_BASE_URL,
            api_key=Config.OPENAI_API_KEY,
            model=Config.MODEL,
            prompt_template=prompt_template
        )
        
        cache = CacheManager("test_cache.json")
        processor = CentralProcessor(classifier, cache, max_workers=2)
        
        # Create test tasks
        tasks = [
            ClassificationTask(
                index=0,
                feedback="Tài xế giao hàng nhanh",
                feedback_key="tai_xe_giao_hang_nhanh"
            ),
            ClassificationTask(
                index=1,
                feedback="Website bị lag",
                feedback_key="website_bi_lag"
            )
        ]
        
        print(f"Processing {len(tasks)} tasks...")
        results, stats = processor.process_batch(tasks)
        
        print(f"Results: {len(results)} items")
        print(f"Stats: {stats}")
        print("✅ Processor test passed!")
        
        # Cleanup
        Path("test_cache.json").unlink(missing_ok=True)
    
    except Exception as e:
        print(f"❌ Processor test failed: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("SPX Classification System - Test Suite")
    print("=" * 60)
    
    test_classifier()
    test_cache()
    test_processor()
    
    print("\n" + "=" * 60)
    print("Test suite completed!")
    print("=" * 60)
