"""
Example usage of the execute_llm_with_tools decorator with the new Google Gen AI SDK
"""

from src.agentils.main import AgentsUtils
import os

# Set your API key (you can also pass it as a parameter)
# os.environ['GOOGLE_API_KEY'] = 'your-api-key-here'

# Example 1: Simple text generation
@AgentsUtils.execute_llm(output="text", temperature=0.7)
def generate_story():
    return "Write a short story about a robot learning to paint."

# Example 2: JSON output with system instruction
@AgentsUtils.execute_llm(
    output="json",
    system_instruction="You are a sentiment analysis expert. Always return valid JSON.",
    temperature=0.1
)
def analyze_sentiment():
    return """
    Analyze the sentiment of this text and return a JSON with 'sentiment' (positive/negative/neutral) 
    and 'confidence' (0-1): "I love this new AI assistant, it's incredibly helpful!"
    """

# Example 3: Define a simple tool function
def get_weather(location: str) -> str:
    """Get the current weather for a location.
    
    Args:
        location: The city and state, e.g. San Francisco, CA
        
    Returns:
        Weather description
    """
    # This is a mock function - in reality you'd call a weather API
    return f"The weather in {location} is sunny and 72°F"

def calculate_budget(days: int, daily_budget: float) -> float:
    """Calculate total budget for a trip.
    
    Args:
        days: Number of days for the trip
        daily_budget: Budget per day in USD
        
    Returns:
        Total budget needed
    """
    return days * daily_budget

# Example 4: Using tools with automatic function calling
@AgentsUtils.execute_llm_with_tools(
    model_name="gemini-2.0-flash-001",
    output="text",
    tools=[get_weather, calculate_budget],  # Pass Python functions directly
    automatic_function_calling=True,
    system_instruction="You are a helpful travel assistant."
)
def plan_trip():
    return "Help me plan a 7-day trip to Tokyo. What's the weather like and what budget should I expect for $200 per day?"

# Example 5: Using manual tool creation
weather_tool = AgentsUtils.create_function_tool(get_weather)

@AgentsUtils.execute_llm_with_tools(
    output="json",
    tools=[weather_tool],
    automatic_function_calling=False  # Manual function calling
)
def get_weather_info():
    return "What's the weather like in New York, NY? Return the result as JSON."

# Example 6: Chat session example
def chat_example():
    """Example of using chat sessions for multi-turn conversations"""
    chat = AgentsUtils.create_chat_session(
        system_instruction="You are a helpful coding assistant.",
        tools=[get_weather]
    )
    
    # First message
    response1 = chat.send_message("Hello! Can you help me with Python?")
    print("Assistant:", response1.text)
    
    # Follow-up message
    response2 = chat.send_message("What's the weather like in San Francisco?")
    print("Assistant:", response2.text)
    
    return chat

if __name__ == "__main__":
    print("Example usage file created. Set your GOOGLE_API_KEY and uncomment the test calls.")
    
    # Test the functions (uncomment when you have an API key)
    
    # print("=== Simple Story Generation ===")
    # story = generate_story()
    # print("Generated story:", story)
    
    # print("\n=== Sentiment Analysis ===")
    # sentiment = analyze_sentiment()
    # print("Sentiment analysis:", sentiment)
    
    # print("\n=== Trip Planning with Tools ===")
    # trip_plan = plan_trip()
    # print("Trip plan:", trip_plan)
    
    # print("\n=== Manual Tool Usage ===")
    # weather_info = get_weather_info()
    # print("Weather info:", weather_info)
    
    # print("\n=== Chat Session ===")
    # chat = chat_example()