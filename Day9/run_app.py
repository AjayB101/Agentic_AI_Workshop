#!/usr/bin/env python3
"""
Run script for the AI-Powered Placement Readiness System
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def check_requirements():
    """Check if all required packages are installed"""
    required_packages = [
        'streamlit',
        'pandas',
        'chromadb',
        'langchain',
        'langchain-community',
        'langchain-google-genai',
        'langchain-chroma',
        'PyPDF2',
        'python-docx',
        'google-generativeai',
        'sentence-transformers'
    ]


def setup_environment():
    """Setup environment variables and directories"""
    # Create necessary directories
    directories = ['./chroma_db', './logs', './temp']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 Created directory: {directory}")

    # Check for API keys


def run_streamlit_app(port=8501, host="localhost"):
    """Run the Streamlit application"""
    try:
        print(f"🚀 Starting Streamlit app on {host}:{port}")
        print(f"🌐 Open your browser to: http://{host}:{port}")
        print("⏹️  Press Ctrl+C to stop the server")

        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", str(port),
            "--server.address", host,
            "--server.headless", "true" if host != "localhost" else "false"
        ])
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped by user")
    except Exception as e:
        print(f"❌ Error running Streamlit app: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="AI-Powered Placement Readiness System")
    parser.add_argument("--port", "-p", type=int,
                        default=8501, help="Port to run the app on")
    parser.add_argument("--host", "-H", default="localhost",
                        help="Host to run the app on")
    parser.add_argument("--skip-checks", action="store_true",
                        help="Skip requirement checks")
    parser.add_argument("--setup-only", action="store_true",
                        help="Only setup environment, don't run app")

    args = parser.parse_args()

    print("🎓 AI-Powered Placement Readiness System")
    print("="*50)

    # Setup environment
    setup_environment()

    # Check requirements
    if not args.skip_checks:
        if not check_requirements():
            sys.exit(1)

    if args.setup_only:
        print("✅ Environment setup complete!")
        return

    # Run the app
    run_streamlit_app(args.port, args.host)


if __name__ == "__main__":
    main()
