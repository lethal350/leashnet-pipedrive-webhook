#!/usr/bin/env python3
"""
Quick Start Script for 3D Printer Maintenance Agent

This script helps you get started quickly by:
1. Checking if dependencies are installed
2. Checking if API key is configured
3. Running a test query
4. Launching the interactive CLI
"""

import sys
import os
import subprocess

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_step(number, text):
    print(f"\n[{number}] {text}")

def check_python_version():
    """Check if Python version is 3.8+"""
    print_step(1, "Checking Python version...")

    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. You have Python {version.major}.{version.minor}")
        print("\nPlease upgrade Python:")
        print("  - Windows: Download from https://python.org/downloads/")
        print("  - Mac: brew install python3")
        print("  - Linux: sudo apt install python3")
        return False

    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    print_step(2, "Checking dependencies...")

    required = ['anthropic', 'python-dotenv', 'rich']
    missing = []

    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ❌ {package} not found")
            missing.append(package)

    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("\nInstall with:")
        print("  pip install -r requirements.txt")
        print("\nOr:")
        print(f"  pip install {' '.join(missing)}")

        # Ask if user wants to install now
        response = input("\nInstall missing packages now? (yes/no): ").lower().strip()
        if response in ['yes', 'y']:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
                print("✓ Dependencies installed successfully!")
                return True
            except subprocess.CalledProcessError:
                print("❌ Installation failed. Please install manually.")
                return False
        return False

    print("✓ All dependencies installed")
    return True

def check_api_key():
    """Check if API key is configured"""
    print_step(3, "Checking API key configuration...")

    # Check environment variable
    api_key = os.getenv('ANTHROPIC_API_KEY')

    # Check .env file
    if not api_key and os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('ANTHROPIC_API_KEY='):
                    api_key = line.split('=', 1)[1].strip()
                    break

    if not api_key:
        print("❌ API key not found")
        print("\nYou need an Anthropic API key to use this agent.")
        print("\nSteps to get your API key:")
        print("  1. Go to https://console.anthropic.com/")
        print("  2. Sign up or log in")
        print("  3. Navigate to 'API Keys'")
        print("  4. Create a new key")
        print("  5. Copy the key (starts with 'sk-ant-...')")

        key = input("\nEnter your API key (or press Enter to skip): ").strip()

        if key:
            # Save to .env file
            with open('.env', 'w') as f:
                f.write(f"ANTHROPIC_API_KEY={key}\n")
                f.write("AGENT_MODEL=claude-3-5-sonnet-20241022\n")
            print("✓ API key saved to .env file")
            return True
        else:
            print("\nSkipping API key setup. You can add it later to .env file")
            return False

    # Mask the key for display
    masked_key = api_key[:10] + "..." + api_key[-4:] if len(api_key) > 14 else "***"
    print(f"✓ API key found: {masked_key}")
    return True

def run_test_query():
    """Run a simple test query"""
    print_step(4, "Testing agent...")

    try:
        from agents.printer_maintenance_agent import PrinterMaintenanceAgent

        print("  Initializing agent...")
        agent = PrinterMaintenanceAgent()

        print("  Running test query...")
        response = agent.diagnose("How do I level the bed on an Ender 3?")

        print("\n✓ Agent is working! Test response:")
        print("-" * 70)
        print(response[:300] + "..." if len(response) > 300 else response)
        print("-" * 70)

        return True

    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        return False

def launch_cli():
    """Launch the interactive CLI"""
    print_step(5, "Launching interactive CLI...")
    print("\nStarting 3D Printer Maintenance Agent CLI...")
    print("(Press Ctrl+C to exit)\n")

    try:
        from cli import main
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"\n❌ Failed to launch CLI: {str(e)}")

def show_menu():
    """Show main menu"""
    print("\nWhat would you like to do?")
    print("  1. Run test query")
    print("  2. Launch interactive CLI")
    print("  3. View documentation")
    print("  4. Exit")

    choice = input("\nChoice (1-4): ").strip()
    return choice

def view_documentation():
    """Show documentation info"""
    print("\nAvailable Documentation:")
    print("  - SETUP_GUIDE.md       - Complete setup instructions")
    print("  - README.md            - Project overview")
    print("  - COREXY_CONVERSION.md - CoreXY build guide")
    print("  - UPGRADE_GUIDE.md     - Hardware upgrade priorities")
    print("  - HARDWARE_DIAGNOSTICS.md - Hardware diagnostic reference")
    print("\nTraining Environment:")
    print("  cd training/")
    print("  python train_agent.py")

def main():
    """Main entry point"""
    print_header("3D Printer Maintenance Agent - Quick Start")

    print("\nThis script will help you get started with your AI printer expert.")

    # Run checks
    if not check_python_version():
        sys.exit(1)

    if not check_dependencies():
        sys.exit(1)

    has_api_key = check_api_key()

    if not has_api_key:
        print("\n" + "=" * 70)
        print("Setup incomplete. Please configure your API key and try again.")
        print("=" * 70)
        sys.exit(1)

    print("\n" + "=" * 70)
    print("  ✓ Setup Complete!")
    print("=" * 70)

    # Show menu
    while True:
        choice = show_menu()

        if choice == '1':
            if run_test_query():
                input("\nPress Enter to continue...")
            else:
                print("\nTest failed. Check your API key and internet connection.")
                input("Press Enter to continue...")

        elif choice == '2':
            launch_cli()
            break

        elif choice == '3':
            view_documentation()
            input("\nPress Enter to continue...")

        elif choice == '4':
            print("\nGoodbye! Happy printing!")
            break

        else:
            print("Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
