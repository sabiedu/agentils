# Agentils - AI Agent Utilities

A powerful Python toolkit for building AI agents with LLM integration, decorators for easy function calling, and utility functions.

## Features

- 🤖 **Easy LLM Integration**: Simple decorators for Google Gemini API
- 🛠️ **Function Calling**: Automatic tool integration with Python functions
- 📝 **JSON/Text Output**: Flexible output formatting
- 🔧 **Utility Functions**: JSON parsing, file operations, and more
- 🎯 **Type Safe**: Full type hints for better development experience
- 🚀 **Simple API**: Minimal setup, maximum productivity

## Installation

```bash
pip install agentils
```

## Development Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your credentials
3. Run the setup script:
   ```bash
   python setup_dev.py
   ```

## Publishing (for maintainers)

**⚠️ Security Note**: Never commit credentials to version control!

### Quick Publishing

```bash
# Publish to both PyPI and private repo
python publish.py

# Publish to PyPI only
python publish.py --target pypi

# Publish to private repo only
python publish.py --target repoflow

# Windows users
publish.bat both
```

### First-time PyPI Setup

1. Create PyPI account and API token
2. Add credentials to `.env` file
3. See [PYPI_SETUP.md](PYPI_SETUP.md) for detailed instructions

### Installation from Different Sources

```bash
# From PyPI (public)
pip install agentils

# From private repository
pip install agentils --index-url https://api.repoflow.io/pypi/eric-4092/erpy/simple/
```

## Quick Start

### Basic Usage

```python
from agentils import AgentsUtils
import os

# Set your API key
os.environ['GOOGLE_API_KEY'] = 'your-api-key-here'

# Simple text generation
@AgentsUtils.execute_llm(output="text")
def generate_story():
    return "Write a short story about a robot learning to paint."

story = generate_story()
print(story)
```

### JSON Output

```python
@AgentsUtils.execute_llm(output="json")
def analyze_sentiment():
    return """
    Analyze the sentiment of this text and return JSON with 'sentiment' and 'confidence':
    "I love this new AI assistant!"
    """

result = analyze_sentiment()
print(result)  # {'sentiment': 'positive', 'confidence': 0.95}
```

### Function Calling with Tools

```python
def get_weather(location: str) -> str:
    """Get the current weather for a location."""
    return f"The weather in {location} is sunny and 72°F"

@AgentsUtils.execute_llm_with_tools(
    tools=[get_weather],  # Pass Python functions directly!
    automatic_function_calling=True
)
def weather_assistant():
    return "What's the weather like in San Francisco?"

response = weather_assistant()
print(response)
```

### Advanced Configuration

```python
@AgentsUtils.execute_llm_with_tools(
    model_name="gemini-2.0-flash-001",
    temperature=0.7,
    max_output_tokens=1000,
    system_instruction="You are a helpful coding assistant",
    tools=[get_weather],
    output="json"
)
def advanced_task():
    return "Help me plan a coding project with weather considerations"
```

### Chat Sessions

```python
# Create a chat session for multi-turn conversations
chat = AgentsUtils.create_chat_session(
    system_instruction="You are a helpful assistant",
    tools=[get_weather]
)

response1 = chat.send_message("Hello!")
response2 = chat.send_message("What's the weather in Tokyo?")
```

## Utility Functions

```python
from agentils import Utils

# JSON operations
data = Utils.string_to_dict('{"key": "value"}')
json_str = Utils.dict_to_string({"key": "value"})

# File operations
Utils.save_dict_to_file(data, "data.json")
loaded_data = Utils.load_dict_from_file("data.json")
```

## API Reference

### AgentsUtils

#### `execute_llm(**kwargs)`
Simple decorator for LLM calls without tools.

**Parameters:**
- `model_name` (str): Model to use (default: "gemini-2.0-flash-001")
- `output` (str): "json" or "text"
- `api_key` (str, optional): API key (uses GOOGLE_API_KEY env var)
- `system_instruction` (str, optional): System instruction
- `temperature` (float, optional): Temperature setting
- `max_output_tokens` (int, optional): Max output tokens

#### `execute_llm_with_tools(**kwargs)`
Advanced decorator with tools support.

**Additional Parameters:**
- `tools` (list): List of Python functions or Tool objects
- `automatic_function_calling` (bool): Enable automatic function calling
- `max_function_calls` (int): Maximum number of function calls

#### `create_chat_session(**kwargs)`
Create a chat session for multi-turn conversations.

### Utils

#### `string_to_dict(s: str) -> dict`
Convert JSON string to dictionary.

#### `dict_to_string(d: dict) -> str`
Convert dictionary to JSON string.

#### `save_dict_to_file(d: dict, filename: str)`
Save dictionary to JSON file.

#### `load_dict_from_file(filename: str) -> dict`
Load dictionary from JSON file.

## Environment Variables

- `GOOGLE_API_KEY`: Your Google AI API key (required)
- `GEMINI_API_KEY`: Alternative API key variable name

## Requirements

- Python 3.8+
- google-genai >= 0.3.0
- pydantic >= 2.11.7

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.