#!/usr/bin/env python
import os
import re

README_FILENAME = "README.md"
# Common placeholders found in the initial TEMPLATE_PROJECT_OUTPUT/README.md
GENERIC_PROJECT_PLACEHOLDER = "[Original Project Name/GuardianRoute]"
NEW_PROJECT_NAME_PLACEHOLDER_TEXT = "[New Project Name]" # If used explicitly
CUSTOMIZE_PROJECT_OVERVIEW_TEXT = "Customize this for your new project."

def update_readme_interactive(project_root_path, new_project_name):
    """
    Interactively helps update placeholders in the project's README.md.
    """
    readme_path = os.path.join(project_root_path, README_FILENAME)

    if not os.path.exists(readme_path):
        print(f"Error: {README_FILENAME} not found at '{readme_path}'.")
        return

    print(f"Updating {readme_path} for project: {new_project_name}\n")
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {readme_path}: {e}")
        return

    original_content = content
    
    # 1. Automatic replacements
    content = content.replace(GENERIC_PROJECT_PLACEHOLDER, new_project_name)
    content = content.replace(NEW_PROJECT_NAME_PLACEHOLDER_TEXT, new_project_name)
    
    # A more specific replacement for the title if it's generic
    # Example: "# Project Template" -> "# MyNewApp Project" (if new_project_name is MyNewApp)
    # This is a simple replacement; a more robust one might use regex for more flexible title lines.
    if content.startswith("# Project Template"):
        content = content.replace("# Project Template", f"# {new_project_name} Project", 1)
        print(f"- Automatically updated main title to '{new_project_name} Project'.")


    # 2. Interactive prompts for sections that need manual review/update
    #    We'll look for common "TODO" or placeholder phrases.
    
    # Example: Prompt for Project Overview customization
    # In GuardianRoute's README.md, it says:
    # `docs/00_Project_Overview.md` (Customize this for your new project)
    # And in the "Getting Started" section:
    # Customize the `Project_Overview.md` with specifics for your new project.
    
    if CUSTOMIZE_PROJECT_OVERVIEW_TEXT in content:
        print(f"\nFound placeholder: \"{CUSTOMIZE_PROJECT_OVERVIEW_TEXT}\"")
        print("This typically refers to customizing 'docs/00_Project_Overview.md'.")
        user_input = input("Have you customized 'docs/00_Project_Overview.md' yet? (yes/no/skip): ").lower()
        if user_input == 'yes':
            # Optionally, remove the placeholder text from README if desired, or just note it.
            # content = content.replace(f"({CUSTOMIZE_PROJECT_OVERVIEW_TEXT})", "(Customized)")
            print("Great! Noted.")
        elif user_input == 'no':
            print(f"Reminder: Please customize 'docs/00_Project_Overview.md' with specifics for '{new_project_name}'.")
        else:
            print("Skipping this reminder.")

    # Add more checks for other common placeholders or TODOs you expect in your README template.
    # For example, if you have sections like:
    # - "[Describe Your Key Features Here]"
    # - "[Setup Instructions for Specific Tool]"
    
    # Example: Check for generic "Getting Started" steps that might need review
    getting_started_section_match = re.search(r"## Getting Started\n([\s\S]*?)\n##", content, re.IGNORECASE)
    if getting_started_section_match:
        gs_content = getting_started_section_match.group(1)
        # Check for lines that might be too generic from the template
        if "Rename `backend_template` and `frontend_template`" in gs_content:
            print("\nFound 'Rename backend_template/frontend_template' in 'Getting Started'.")
            print("The initialize_new_project.py script should now handle this.")
            print("Consider updating this part of your README.md to reflect the new automated process.")
            if input("Mark this as reviewed in the script's context? (yes/no): ").lower() == 'yes':
                 # Could offer to comment it out or remove it, but for now, just a reminder.
                 pass


    if content != original_content:
        try:
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"\n{README_FILENAME} has been partially updated with the project name.")
        except Exception as e:
            print(f"Error writing updates to {readme_path}: {e}")
    else:
        print(f"\nNo automatic updates were made to {readme_path} based on current placeholders.")

    print("\nPlease manually review the rest of README.md to ensure all sections are relevant and customized for your new project.")


def main():
    project_root = os.getcwd()
    project_name_from_dir = os.path.basename(project_root) # Infer project name from current dir

    print(f"Interactive README.md Updater for project: {project_name_from_dir}")
    print("This script helps update common placeholders in your README.md.")
    
    # Confirm inferred project name or ask for it
    confirmed_project_name = input(f"Is '{project_name_from_dir}' the correct project name for replacements? (yes/custom_name): ").strip()
    if confirmed_project_name.lower() != 'yes' and confirmed_project_name:
        project_name_to_use = confirmed_project_name
    elif confirmed_project_name.lower() == 'yes':
        project_name_to_use = project_name_from_dir
    else:
        print("Invalid input. Exiting.")
        return
        
    update_readme_interactive(project_root, project_name_to_use)

if __name__ == "__main__":
    # This script should be run from the root of a newly generated project.
    # Example: python ../TEMPLATE_PROJECT_OUTPUT/scripts/project_management/update_readme_todos.py
    # Or, if copied into the new project's scripts/project_management/ folder:
    # python scripts/project_management/update_readme_todos.py
    main()