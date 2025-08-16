#!/usr/bin/env python3
"""
Development environment setup script
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ {description} failed: {result.stderr}")
        return False
    
    print(f"✅ {description} completed")
    return True

def setup_development():
    """Set up development environment"""
    print("🚀 Setting up development environment...")
    
    # Install package in editable mode
    if not run_command("uv pip install -e .", "Installing package in editable mode"):
        return False
    
    # Install development dependencies
    if not run_command("uv pip install pytest black isort mypy", "Installing dev dependencies"):
        return False
    
    # Run basic tests
    if Path("test_basic.py").exists():
        if not run_command("python test_basic.py", "Running basic tests"):
            return False
    
    print("🎉 Development environment ready!")
    print("\nNext steps:")
    print("1. Copy .env.example to .env and add your credentials")
    print("2. Run: python test_basic.py")
    print("3. Run: python publish.py (when ready to publish)")
    
    return True

if __name__ == "__main__":
    if not setup_development():
        sys.exit(1)