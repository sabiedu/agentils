#!/usr/bin/env python3
"""
Multi-repository publishing script for agentils package
Supports publishing to PyPI and private repositories
"""

import os
import subprocess
import sys
from pathlib import Path
import argparse

def load_env():
    """Load environment variables from .env file"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found. Please create it with your credentials.")
        sys.exit(1)
    
    env_vars = {}
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key] = value
    
    return env_vars

def build_package():
    """Build the package"""
    print("🔨 Building package...")
    result = subprocess.run(["uv", "build"], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Build failed: {result.stderr}")
        return False
    
    print("✅ Package built successfully")
    return True

def publish_to_pypi(env_vars):
    """Publish to PyPI"""
    username = env_vars.get('PYPI_USERNAME', '__token__')
    password = env_vars.get('PYPI_PASSWORD')
    
    if not password:
        print("❌ Missing PYPI_PASSWORD in .env file")
        print("💡 Get your API token from: https://pypi.org/manage/account/token/")
        return False
    
    print("📦 Publishing to PyPI...")
    
    # Use uv publish to PyPI
    cmd = [
        "uv", "publish",
        "--username", username,
        "--password", password,
        "dist/*"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ PyPI publish failed: {result.stderr}")
        return False
    
    print("✅ Package published to PyPI successfully!")
    return True

def publish_to_repoflow(env_vars):
    """Publish to private RepoFlow repository"""
    username = env_vars.get('REPOFLOW_USERNAME')
    password = env_vars.get('REPOFLOW_PASSWORD')
    
    if not username or not password:
        print("❌ Missing REPOFLOW_USERNAME or REPOFLOW_PASSWORD in .env file")
        return False
    
    # Build the publish URL with credentials
    publish_url = f"https://{username}:{password}@api.repoflow.io/pypi/eric-4092/erpy"
    
    print("📦 Publishing to RepoFlow...")
    
    # Use uv publish with the credentials
    cmd = [
        "uv", "publish",
        "--publish-url", publish_url,
        "dist/*"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ RepoFlow publish failed: {result.stderr}")
        print("💡 This might be normal if RepoFlow requires different authentication")
        print("💡 Your package is still available on PyPI!")
        return False
    return True

def main():
    """Main publishing workflow"""
    parser = argparse.ArgumentParser(description="Publish agentils package")
    parser.add_argument(
        "--target", 
        choices=["pypi", "repoflow", "both"], 
        default="both",
        help="Where to publish the package (default: both)"
    )
    parser.add_argument(
        "--skip-build", 
        action="store_true",
        help="Skip building the package (use existing dist/)"
    )
    
    args = parser.parse_args()
    
    print(f"🚀 Starting publish workflow (target: {args.target})...")
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ pyproject.toml not found. Run this from the package root.")
        sys.exit(1)
    
    # Load environment variables
    env_vars = load_env()
    
    # Build the package (unless skipped)
    if not args.skip_build:
        if not build_package():
            sys.exit(1)
    else:
        print("⏭️  Skipping build (using existing dist/)")
    
    # Check if dist files exist
    dist_files = list(Path("dist").glob("*.whl")) + list(Path("dist").glob("*.tar.gz"))
    if not dist_files:
        print("❌ No distribution files found in dist/. Run without --skip-build.")
        sys.exit(1)
    
    # Ask for confirmation
    print(f"\n📋 Ready to publish to: {args.target}")
    print(f"📦 Distribution files: {len(dist_files)} files")
    response = input("📤 Continue with publish? (y/N): ")
    if response.lower() != 'y':
        print("❌ Publish cancelled")
        sys.exit(0)
    
    # Publish based on target
    success = True
    
    if args.target in ["pypi", "both"]:
        if not publish_to_pypi(env_vars):
            success = False
    
    if args.target in ["repoflow", "both"]:
        if not publish_to_repoflow(env_vars):
            success = False
    
    if success:
        print("🎉 All publishing completed successfully!")
        if args.target == "both":
            print("📍 Your package is now available on:")
            print("   • PyPI: https://pypi.org/project/agentils/")
            print("   • RepoFlow: https://api.repoflow.io/pypi/eric-4092/erpy/")
    else:
        print("⚠️  Some publishing steps failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()