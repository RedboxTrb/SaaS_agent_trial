import os
import sys
from datetime import datetime

from agent.orchestrator import StatefulAgent
from use_cases.saas_launch import run_saas_dashboard_launch
from use_cases.investor_update import run_investor_update


def print_banner():
    print("\nSTATEFUL EXECUTION AGENT\n")


def get_api_key():
    # check environment variable first
    api_key = os.getenv("GEMINI_API_KEY")

    # prompt user if not found
    if not api_key:
        api_key = None

    if not api_key:
        print("GEMINI_API_KEY not found.")
        api_key = input("Enter your Gemini API key: ").strip()
        if not api_key:
            print("API key required to run.")
            sys.exit(1)
    return api_key


def main():
    print_banner()

    api_key = get_api_key()
    agent = StatefulAgent(api_key=api_key)

    print(f"Agent initialized. Session ID: {agent.session_id[:8]}...\n")

    run_saas_dashboard_launch(agent)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
    except Exception as e:
        print(f"\n\nError: {str(e)}")
        import traceback
        traceback.print_exc()
