# Recommendations for Resolving Absolute Path Issues

This document outlines recommendations to improve file path handling in the project initialization script (`initialize_new_project.py`) and ensure robust, relative path usage throughout the generated project structure, particularly within `custom_modes.json` and related scripts.

## 1. Refactor `initialize_new_project.py`

The initialization script contains several hardcoded absolute paths and replacement logic that can be made more robust and portable.

### 1.1. Make `BASE_GIT_DIR` and `SOURCE_DIR_PATH` configurable or relative

**Issue:**
`BASE_GIT_DIR = r"C:\git"` and `SOURCE_DIR_PATH = r"C:\git\TEMPLATE_PROJECT_OUTPUT"` are hardcoded. This limits the script's usability to a specific directory structure on a specific machine.

**Recommendation:**

*   **Option A (Preferred for flexibility):** Allow these to be set via command-line arguments.
    ```python
    # In initialize_new_project.py
    import argparse
    # ...
    # At the beginning of main() or globally:
    # parser = argparse.ArgumentParser(description="Initialize a new project.")
    # parser.add_argument("--base-git-dir", default=r"C:\git", help="The base directory where projects are stored.")
    # parser.add_argument("--source-dir-path", default=r"C:\git\TEMPLATE_PROJECT_OUTPUT", help="Path to the template project directory.")
    # args = parser.parse_args()
    # BASE_GIT_DIR = args.base_git_dir
    # SOURCE_DIR_PATH = args.source_dir_path
    ```

### 1.2. Robustly locate the source `custom_modes.json`

**Issue:**
The current logic `project_root = os.path.dirname(script_dir)` assumes a specific directory structure.

**Recommendation:**
If `initialize_new_project.py` is, for example, located in `TEMPLATE_PROJECT_OUTPUT/tools/`, and `custom_modes.json` (the template version) is in `TEMPLATE_PROJECT_OUTPUT/`, use:
```python
# In initialize_new_project.py, inside main()
script_dir = os.path.dirname(os.path.abspath(__file__))
# Assuming custom_modes.json is in the parent directory of the script's directory
template_project_root = os.path.abspath(os.path.join(script_dir, ".."))
source_custom_modes_file = os.path.join(template_project_root, original_custom_modes_filename)

# Ensure SOURCE_DIR_PATH also aligns with this. If SOURCE_DIR_PATH is meant to be template_project_root:
# SOURCE_DIR_PATH = template_project_root

### 1.3. Refine replace_in_file_content function
**Issue:**

The line content = content.replace(PLACEHOLDER_TEMPLATE_DIR_NAME, new_project_name) is problematic. It replaces the template's root directory name ("TEMPLATE_PROJECT_OUTPUT") with the new project's name in any file content. This is usually not desired. For example, if a file path was TEMPLATE_PROJECT_OUTPUT/docs/some_guide.md, it would become NewProjectName/docs/some_guide.md. If this is an absolute path in the content C:\git\TEMPLATE_PROJECT_OUTPUT\docs it becomes C:\git\NewProjectName\docs. However, typically, such internal paths should be relative from the start or stripped of the template root prefix.
The replacement content = content.replace(template_project_path_placeholder, new_project_path_placeholder) changes one absolute path to another. This is okay if some template files must contain absolute references to their own project structure, but it's better if template files use relative paths or placeholders.
Recommendation:
Review necessity: Determine if PLACEHOLDER_TEMPLATE_DIR_NAME actually needs to be replaced by new_project_name in file contents. It's more likely that if PLACEHOLDER_TEMPLATE_DIR_NAME appears as part of a path prefix in content, it should be removed to make the path relative to the project root, or the paths in templates should be relative from the start.
If this replacement is truly needed for specific files (e.g., a settings file that uses the directory name as part of a module path), consider making it more targeted rather than global.
Prioritize using relative paths within template files, reducing the need for complex path replacements.
The replacement content = content.replace(PLACEHOLDER_PROJECT_NAME_GENERIC, new_project_name) is generally fine for textual project name mentions.
The replacement content = content.replace(DJANGO_CORE_PLACEHOLDER_NAME, new_project_name_slugified) is also fine for the Django project's internal name.

**Recommendation:**

def replace_in_file_content(content, new_project_name, new_project_name_slugified, base_git_dir_val, template_dir_name_val):
    """Performs string replacements in the given content."""
    # Generic project name placeholder
    content = content.replace(PLACEHOLDER_PROJECT_NAME_GENERIC, new_project_name)
    # Django core project placeholder name
    content = content.replace(DJANGO_CORE_PLACEHOLDER_NAME, new_project_name_slugified)

    # Handle full path replacement: C:\git\TEMPLATE_PROJECT_OUTPUT -> C:\git\NewProjectName
    # This is for absolute paths embedded in files that refer to the project's own location.
    # Prefer relative paths in templates to minimize need for this.
    if base_git_dir_val and template_dir_name_val:
        old_abs_path_prefix = os.path.join(base_git_dir_val, template_dir_name_val)
        new_abs_path_prefix = os.path.join(base_git_dir_val, new_project_name)
        content = content.replace(old_abs_path_prefix, new_abs_path_prefix)

    # Consider if replacing just "TEMPLATE_PROJECT_OUTPUT" with new_project_name is actually correct.
    # It might be better to remove "TEMPLATE_PROJECT_OUTPUT/" prefixes if they exist to make paths relative.
    # For now, keeping original logic but with a note:
    # This line is potentially problematic:
    # content = content.replace(template_dir_name_val, new_project_name)
    # A safer alternative if template_dir_name_val is a path segment to be removed:
    # content = content.replace(template_dir_name_val + os.sep, "") # If making relative
    # Or, if it's a placeholder for the project's root Python package if different from project name:
    # content = content.replace(template_dir_name_val, new_project_name_slugified) # Or specific placeholder

    return content

# In main loop for global content replacement:
# modified_content = replace_in_file_content(content, new_project_name, new_project_name_slugified, BASE_GIT_DIR, PLACEHOLDER_TEMPLATE_DIR_NAME)


### 1.4. Simplify path replacements in process_custom_modes_json


**Issue:**
Issue:
The current process_custom_modes_json has complex logic to replace parts of absolute paths:
original_template_output_in_guardianroute_path = os.path.join(BASE_GIT_DIR, PLACEHOLDER_PROJECT_NAME_GENERIC, PLACEHOLDER_TEMPLATE_DIR_NAME) + os.sep
original_management_portal_in_guardianroute_path = os.path.join(BASE_GIT_DIR, PLACEHOLDER_PROJECT_NAME_GENERIC, "management-portal") + os.sep
# ...
text_content = text_content.replace(original_template_output_in_guardianroute_path, "")
text_content = text_content.replace(original_management_portal_in_guardianroute_path, new_management_portal_path)


**Recommendation:**
Simplify the text content processing within process_custom_modes_json. The primary goal is to replace the placeholder project name (e.g., "GuardianRoute") in textual descriptions, names, and slugs. The paths within the custom_modes.json (to docs, style guides, scripts) should already be authored as project-relative in the template.
# In process_custom_modes_json
# ...
        # Step 1: Handle text content fields (roleDefinition, whenToUse, customInstructions)
        for key in ['roleDefinition', 'whenToUse', 'customInstructions']:
            if key in new_mode and isinstance(new_mode[key], str):
                text_content = new_mode[key]

                # Only replace the generic project name placeholder.
                # Paths within these texts should already be project-relative from the template.
                text_content = text_content.replace(PLACEHOLDER_PROJECT_NAME_GENERIC, new_project_name)
                
                # If there was a specific need to adjust a path prefix related to the template's *own structure*,
                # for example, if paths were like "TEMPLATE_PROJECT_OUTPUT/docs/...", you might add:
                # text_content = text_content.replace(PLACEHOLDER_TEMPLATE_DIR_NAME + "/", "") # To remove prefix
                # However, your example custom_modes.json doesn't show paths like this.

                new_mode[key] = text_content
# ... rest of the function (slug, name, source replacements) is likely fine.
