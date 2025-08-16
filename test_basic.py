"""
Basic tests for agentils package
"""

def test_imports():
    """Test that basic imports work"""
    try:
        from agentils import AgentsUtils, Utils
        print("✅ Basic imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_utils():
    """Test utility functions"""
    try:
        from agentils import Utils
        
        # Test JSON operations
        test_dict = {"key": "value", "number": 42}
        json_str = Utils.dict_to_string(test_dict)
        parsed_dict = Utils.string_to_dict(json_str)
        
        assert parsed_dict == test_dict
        print("✅ Utils JSON operations work")
        return True
    except Exception as e:
        print(f"❌ Utils test failed: {e}")
        return False

def test_decorators():
    """Test that decorators can be created (without API calls)"""
    try:
        from agentils import AgentsUtils
        
        # Test decorator creation (don't actually call it)
        @AgentsUtils.execute_llm(output="text")
        def dummy_function():
            return "test prompt"
        
        print("✅ Decorator creation successful")
        return True
    except Exception as e:
        print(f"❌ Decorator test failed: {e}")
        return False

if __name__ == "__main__":
    print("Running basic tests for agentils...")
    
    tests = [test_imports, test_utils, test_decorators]
    passed = 0
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\nResults: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Package is ready to build.")
    else:
        print("⚠️  Some tests failed. Check the issues above.")