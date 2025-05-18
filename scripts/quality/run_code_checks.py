import subprocess
import os
import platform

# Configuration (customize as needed)
PYTHON_LINTER = "flake8"  # or "pylint"
PYTHON_FORMATTER = "black"
JAVASCRIPT_LINTER = "eslint" # Assumes eslint is configured
JAVASCRIPT_FORMATTER = "prettier" # Assumes prettier is configured

# Define project subdirectories to check (can be more granular)
# These paths are relative to the project root.
PYTHON_PATHS_TO_CHECK = [
    "api",
    "tms_project",
    "transport",
    "scripts" # Also lint the scripts themselves
]
# For frontend, typically you run linters/formatters from the frontend project's root
# This script will attempt to cd into those directories.
FRONTEND_PROJECT_DIRS = {
    "management-portal": "management-portal",
    "driver-portal/driver_portal": "driver_portal/driver_portal", # Adjusted path
    "parentstudent-portal/parentstudent_portal": "parentstudent_portal/parentstudent_portal" # Adjusted path
}

# --- Helper Functions ---
def run_command(command, working_dir=None, shell=False):
    """Runs a command and prints its output."""
    original_dir = None
    if working_dir:
        original_dir = os.getcwd()
        try:
            os.chdir(working_dir)
            print(f"\nRunning in {os.getcwd()}: {' '.join(command)}")
        except FileNotFoundError:
            print(f"Error: Directory not found: {working_dir}")
            return False
    else:
        print(f"\nRunning: {' '.join(command)}")

    try:
        # For Windows, shell=True might be needed for some commands if they are .cmd or .bat files
        # For cross-platform, try to avoid shell=True if direct executable path is known
        use_shell = shell or platform.system() == "Windows"
        
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=use_shell)
        stdout, stderr = process.communicate()
        
        if stdout:
            print("Output:\n", stdout)
        if stderr:
            # ESLint and Prettier often output to stderr for info/warnings too
            print("Errors/Warnings:\n", stderr)
            
        if process.returncode != 0:
            print(f"Command failed with exit code {process.returncode}")
            return False
        return True
    except FileNotFoundError:
        print(f"Error: Command not found: {command[0]}. Is it installed and in PATH?")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        if original_dir:
            os.chdir(original_dir)

def check_tool_exists(tool_name):
    """Placeholder: In a real scenario, you'd check if a tool is callable."""
    # This is a very basic check. A robust check would use `shutil.which` or similar.
    # For now, we'll assume tools are in PATH.
    return True

# --- Main Script Logic ---
def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    all_checks_passed = True
    tools_missing = False

    print("--- Starting Code Quality Checks ---")

    # 1. Python Checks
    print("\n--- Python Checks ---")
    if check_tool_exists(PYTHON_LINTER):
        for path_to_check in PYTHON_PATHS_TO_CHECK:
            full_path = os.path.join(project_root, path_to_check)
            if os.path.exists(full_path):
                print(f"\nLinting Python in: {path_to_check}")
                if not run_command([PYTHON_LINTER, full_path], working_dir=project_root):
                    all_checks_passed = False
            else:
                print(f"Warning: Python path not found: {full_path}")
    else:
        print(f"Warning: Python linter '{PYTHON_LINTER}' not found. Skipping.")
        tools_missing = True

    if check_tool_exists(PYTHON_FORMATTER):
        for path_to_check in PYTHON_PATHS_TO_CHECK:
            full_path = os.path.join(project_root, path_to_check)
            if os.path.exists(full_path):
                print(f"\nFormatting Python in: {path_to_check} (checking format)")
                 # Add --check for formatters to see if changes are needed without applying them
                if not run_command([PYTHON_FORMATTER, "--check", full_path], working_dir=project_root):
                    all_checks_passed = False
                    print(f"Run '{PYTHON_FORMATTER} {full_path}' to fix formatting issues.")
            else:
                print(f"Warning: Python path not found: {full_path}")
    else:
        print(f"Warning: Python formatter '{PYTHON_FORMATTER}' not found. Skipping.")
        tools_missing = True

    # 2. JavaScript/React Checks
    print("\n--- JavaScript/React Checks ---")
    for portal_name, portal_dir_suffix in FRONTEND_PROJECT_DIRS.items():
        portal_path = os.path.join(project_root, portal_dir_suffix)
        if os.path.isdir(portal_path) and os.path.exists(os.path.join(portal_path, "package.json")):
            print(f"\n--- Checking Frontend: {portal_name} ---")
            
            # Check for common script names in package.json or run tools directly
            # This example directly calls eslint and prettier, assuming they are globally installed
            # or accessible via npx. A better approach for projects with local npm packages
            # would be to use `npm run lint` or `npm run format` if defined in package.json.

            if check_tool_exists(JAVASCRIPT_LINTER): # or use npx
                # Adjust src path as per project structure, e.g. 'src' or '.'
                lint_command = ["npx", JAVASCRIPT_LINTER, "src", "--ext", ".js,.jsx"] # Common for React
                print(f"\nLinting JavaScript/React in: {portal_name}/src")
                if not run_command(lint_command, working_dir=portal_path, shell=True): # shell=True for npx on Windows
                    all_checks_passed = False
            else:
                print(f"Warning: JavaScript linter '{JAVASCRIPT_LINTER}' not found for {portal_name}. Skipping.")
                tools_missing = True

            if check_tool_exists(JAVASCRIPT_FORMATTER): # or use npx
                # Adjust path as per project structure, e.g. 'src/**/*.{js,jsx}'
                format_command = ["npx", JAVASCRIPT_FORMATTER, "--check", "src/**/*.{js,jsx,css,md}"] # Common pattern
                print(f"\nFormatting JavaScript/React in: {portal_name}/src (checking format)")
                if not run_command(format_command, working_dir=portal_path, shell=True): # shell=True for npx on Windows
                    all_checks_passed = False
                    print(f"Run 'npx {JAVASCRIPT_FORMATTER} --write \"src/**/*.{'{js,jsx,css,md}'}\"' in {portal_path} to fix.")
            else:
                print(f"Warning: JavaScript formatter '{JAVASCRIPT_FORMATTER}' not found for {portal_name}. Skipping.")
                tools_missing = True
        else:
            print(f"\nWarning: Frontend project directory or package.json not found for '{portal_name}' at '{portal_path}'. Skipping.")


    print("\n--- Code Quality Checks Summary ---")
    if tools_missing:
        print("Warning: Some tools were not found. Please ensure they are installed and in your PATH or project dependencies.")
    
    if all_checks_passed:
        print("All checks passed successfully!")
    else:
        print("Some checks failed. Please review the output above.")
        exit(1) # Exit with error code if checks fail

if __name__ == "__main__":
    main()