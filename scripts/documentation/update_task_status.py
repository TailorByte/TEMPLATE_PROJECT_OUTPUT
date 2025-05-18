import argparse
import datetime
import os

def update_task_status(task_description, mode_involved, key_changes, project_root_dir):
    """
    Appends task completion details to the ProjectScope_Updates_CompletionStatus.txt file.
    """
    status_file_path = os.path.join(
        project_root_dir,
        "management-portal",
        "src",
        "docs",
        "ProjectScope_Updates_CompletionStatus.txt"
    )
    
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    entry = (
        f"- Task: {task_description}\n"
        f"  - Status: COMPLETED\n"
        f"  - Date: {current_date}\n"
        f"  - Mode(s) Involved: {mode_involved}\n"
        f"  - Key Changes: {key_changes}\n\n"
    )
    
    try:
        with open(status_file_path, "a", encoding="utf-8") as f:
            f.write(entry)
        print(f"Successfully updated {os.path.basename(status_file_path)}")
    except IOError as e:
        print(f"Error: Could not write to {status_file_path}. {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Update the ProjectScope_Updates_CompletionStatus.txt file with task details."
    )
    parser.add_argument(
        "--task",
        required=True,
        help="Brief description of the completed task."
    )
    parser.add_argument(
        "--mode",
        required=True,
        help="The mode(s) involved in completing the task."
    )
    parser.add_argument(
        "--changes",
        required=True,
        help="Key changes made during the task."
    )
    parser.add_argument(
        "--project_root",
        default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")),
        help="The root directory of the GuardianRoute project. Defaults to two levels up from script's directory."
    )
    
    args = parser.parse_args()
    
    update_task_status(args.task, args.mode, args.changes, args.project_root)