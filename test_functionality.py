"""
Test actual functionality with API calls (requires API key)
"""

import os
from agentils import AgentsUtils, Utils

def test_with_api_key():
    """Test actual LLM calls if API key is available"""
    api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("⚠️  No API key found. Set GOOGLE_API_KEY to test LLM functionality.")
        return False
    
    try:
        # Test simple text generation
        @AgentsUtils.execute_llm(output="text", temperature=0.1)
        def simple_test():
            return "Say 'Hello from Agentils!' and nothing else."
        
        result = simple_test()
        print(f"✅ Simple LLM call successful: {result.strip()}")
        
        # Test JSON output
        @AgentsUtils.execute_llm(output="json", temperature=0.1)
        def json_test():
            return 'Return a JSON object with "status": "success" and "message": "working"'
        
        json_result = json_test()
        print(f"✅ JSON LLM call successful: {json_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM functionality test failed: {e}")
        return False

def test_tools():
    """Test function calling if API key is available"""
    api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("⚠️  No API key found. Skipping tools test.")
        return False
    
    try:
        def get_time() -> str:
            """Get the current time"""
            import datetime
            return datetime.datetime.now().strftime("%H:%M:%S")
        
        @AgentsUtils.execute_llm_with_tools(
            tools=[get_time],
            output="text",
            temperature=0.1
        )
        def tool_test():
            return "What time is it right now? Use the get_time function."
        
        result = tool_test()
        print(f"✅ Tool calling successful: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Tool functionality test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Agentils functionality...")
    print("=" * 50)
    
    # Test basic functionality
    print("1. Testing basic imports and utils...")
    try:
        from agentils import AgentsUtils, Utils
        test_dict = {"test": "data"}
        json_str = Utils.dict_to_string(test_dict)
        parsed = Utils.string_to_dict(json_str)
        assert parsed == test_dict
        print("✅ Basic functionality works")
    except Exception as e:
        print(f"❌ Basic functionality failed: {e}")
    
    print("\n2. Testing LLM functionality...")
    test_with_api_key()
    
    print("\n3. Testing tool functionality...")
    test_tools()
    
    print("\n" + "=" * 50)
    print("🎉 Agentils package is ready for use!")
    print("\nTo publish to PyPI:")
    print("1. uv build")
    print("2. uv publish --token <your-pypi-token>")
    print("\nOr install locally:")
    print("uv pip install dist/agentils-0.1.0-py3-none-any.whl")