#!/usr/bin/env python
import subprocess
import shutil
import os
import sys

def check_command_exists(command):
    """Checks if a command exists on the system path."""
    return shutil.which(command) is not None

def run_setup_command(command_args, cwd=None, success_message=None, failure_message=None):
    """Runs a setup command and prints success or failure messages."""
    try:
        print(f"Running: {' '.join(command_args)} {'in ' + cwd if cwd else ''}...")
        process = subprocess.Popen(command_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print(failure_message or f"Error running command: {' '.join(command_args)}")
            if stderr: print(f"Stderr: {stderr.strip()}")
            if stdout: print(f"Stdout: {stdout.strip()}")
            return False
        if success_message:
            print(success_message)
        if stdout: print(stdout.strip())
        return True
    except FileNotFoundError:
        print(f"Error: Command '{command_args[0]}' not found. Is it installed and in your PATH?")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def main():
    print("Configuring pre-commit hooks...")
    project_root = os.getcwd() # Assumes script is run from the project root

    # 1. Check if pre-commit is installed
    if not check_command_exists("pre-commit"):
        print("Error: 'pre-commit' command not found.")
        print("Please install pre-commit first. You can usually install it with pip:")
        print("  pip install pre-commit")
        print("Then, add it to your project's development requirements.")
        sys.exit(1)

    # 2. Check for .pre-commit-config.yaml
    pre_commit_config_file = os.path.join(project_root, ".pre-commit-config.yaml")
    if not os.path.exists(pre_commit_config_file):
        print(f"Warning: '.pre-commit-config.yaml' not found at '{project_root}'.")
        print("Please create a .pre-commit-config.yaml file with your desired hooks.")
        print("Skipping 'pre-commit install'.")
        # Optionally, you could offer to create a default one here.
        sys.exit(0) # Not a fatal error, just can't install hooks.

    # 3. Run 'pre-commit install'
    if run_setup_command(
        ["pre-commit", "install"],
        cwd=project_root,
        success_message="Successfully ran 'pre-commit install'. Hooks are now set up.",
        failure_message="Failed to install pre-commit hooks."
    ):
        print("\nPre-commit hooks have been configured for this repository.")
        print("Commits will now be checked by the configured hooks.")
    else:
        print("\nPre-commit hook setup encountered an issue.")

if __name__ == "__main__":
    # This script should be run from the root of a generated project.
    # Example: python scripts/setup/configure_pre_commit_hooks.py
    main()