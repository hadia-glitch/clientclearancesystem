#!/usr/bin/env python3
"""
Setup script for AI-Based Recommendation System
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up AI-Based Recommendation System")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Download spaCy model
    if not run_command("python -m spacy download en_core_web_sm", "Downloading spaCy model"):
        print("❌ Failed to download spaCy model")
        sys.exit(1)
    
    # Download NLTK data
    nltk_script = """
import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
print("NLTK data downloaded successfully")
"""
    
    if not run_command(f'python -c "{nltk_script}"', "Downloading NLTK data"):
        print("❌ Failed to download NLTK data")
        sys.exit(1)
    
    # Generate initial dataset
    print("🔄 Generating initial dataset...")
    try:
        from src.data.dataset_generator import DatasetGenerator
        generator = DatasetGenerator()
        requirements = generator.generate_client_requirements(150)
        generator.save_dataset(requirements)
        print("✅ Dataset generated successfully")
    except Exception as e:
        print(f"❌ Failed to generate dataset: {e}")
        sys.exit(1)
    
    # Run tests
    print("🔄 Running tests...")
    if not run_command("python -m pytest tests/ -v", "Running test suite"):
        print("⚠️  Some tests failed, but setup can continue")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run the system: python main.py")
    print("2. Try test scenarios: python main.py --test")
    print("3. Generate dataset: python main.py --generate-data")
    print("4. View documentation: docs/README.md")

if __name__ == "__main__":
    main() 