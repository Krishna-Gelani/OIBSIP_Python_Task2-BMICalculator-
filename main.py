import sys
from cli_app import run_cli

def main():
    """
    Application Entry Point.
    Redirects to the CLI application.
    """
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\nForce Termination Detected.")
        sys.exit(0)
    except Exception as e:
        print(f"CRITICAL SYSTEM FAILURE: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
