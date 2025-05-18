# Project Initialization Script Plan

**1. Goal of the Script:**
To create a Python script that automates the setup of a new project by:
*   Prompting the user for a new project name.
*   Copying the entire structure from `C:\git\TEMPLATE_PROJECT_OUTPUT`.
*   Renaming files and updating content by replacing placeholders like "GuardianRoute" and "TEMPLATE_PROJECT_OUTPUT" with the new project name.
*   Specifically configuring a new `custom_modes.json` file in the new project with four project-specific modes (Backend, Frontend, Database, Orchestrator), ensuring that paths to internal project documents within these mode definitions are relative.

**2. Script Details:**
*   **Language:** Python
*   **Location:** The script will be created at `C:\git\TEMPLATE_PROJECT_OUTPUT\scripts\initialize_new_project.py`. This way, it's part of the template and gets copied to new projects, though it's primarily used from the template directory to *create* new projects.

**3. Core Script Logic (Flowchart):**

```mermaid
graph TD
    A[Start] --> B{Prompt for Project Name};
    B --> C{Validate Project Name};
    C -- Invalid --> B;
    C -- Valid --> D[Define Source & Target Dirs];
    D --> E{Create Target Directory};
    E -- Error --> F[Handle Error: Target Exists/Create Fails];
    E -- Success --> G[Copy Files & Dirs from Source to Target];
    G --> H[Global Content Replacement in Copied Files (excluding custom_modes.json initially)];
    H --> I[Process custom_modes.json for New Project];
    I --> J[Write Final custom_modes.json];
    J --> K[End: Success Message];
    F --> Z[End: Error];
    G -- Error --> Z;
    H -- Error --> Z;
    I -- Error --> Z;
    J -- Error --> Z;
```

**4. Detailed Steps for `initialize_new_project.py`:**

*   **Step 1: User Input & Validation**
    *   Prompt the user to enter the `new_project_name`.
    *   Validate the input:
        *   Ensure it's not empty.
        *   Ensure it doesn't contain spaces or characters invalid for directory names.
        *   Check if the target directory `C:\git\[new_project_name]` already exists. If so, ask the user if they want to overwrite or exit. (For simplicity in this plan, we'll assume exit if exists, or ask for a different name).

*   **Step 2: Define Directories**
    *   `source_dir = r"C:\git\TEMPLATE_PROJECT_OUTPUT"`
    *   `target_dir = rf"C:\git\{new_project_name}"` (using an f-string for the new project name)

*   **Step 3: Create Target Directory**
    *   Use `os.makedirs(target_dir, exist_ok=False)`. If `exist_ok=True` is preferred, the validation step should align. For now, assume `exist_ok=False` and rely on prior validation.

*   **Step 4: Copy Files and Directories**
    *   Use `shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)` (Python 3.8+) or a custom recursive copy function to duplicate the entire content of `source_dir` into `target_dir`.
        *   The script `initialize_new_project.py` itself will be copied.

*   **Step 5: Global Content Replacement (All files *except* `custom_modes.json`)**
    *   Iterate through all files in the `target_dir` recursively.
    *   For each file:
        *   If the file is `custom_modes.json`, skip it in this step (it will be handled specifically).
        *   Attempt to read as a text file. If it's a binary file (e.g., images), skip content replacement for it.
        *   Perform the following string replacements in its content:
            1.  `GuardianRoute` -> `[new_project_name]`
            2.  `C:/git/TEMPLATE_PROJECT_OUTPUT` -> `C:/git/[new_project_name]` (adjust slashes based on OS or normalize)
            3.  `TEMPLATE_PROJECT_OUTPUT` (as a standalone string) -> `[new_project_name]`
        *   Write the modified content back to the file.

*   **Step 6: `custom_modes.json` Processing for the New Project**
    *   This step creates a new `custom_modes.json` in the `target_dir` tailored for the new project, containing only the 4 specified modes with relative internal paths.
    *   Define `new_project_name_slugified` (e.g., project name lowercased, spaces replaced with hyphens).
    *   Load the *original* `custom_modes.json` content from `os.path.join(source_dir, 'custom_modes.json')`. (Important: use the pristine template).
    *   Parse this JSON into a Python dictionary. Let `template_modes_list` be the array under the `"customModes"` key.
    *   Initialize `final_project_modes = []`.
    *   Define the slugs of the template modes to use as bases:
        *   `backend_template_slug = "backend-api-django-development"`
        *   `frontend_template_slug = "frontend-react-development"`
        *   `db_template_slug = "database-schema-migration-development"`
        *   `orchestrator_template_slug = "orchestrator-guardianroute"`
    *   For each of these (e.g., `backend_template_slug`):
        *   Find the corresponding `source_mode_dict` from `template_modes_list`.
        *   Create `new_mode = copy.deepcopy(source_mode_dict)`.
        *   **Update `new_mode['name']`**: Replace "GuardianRoute" with `new_project_name`.
            *   Example: "Backend API & Framework Development (GuardianRoute)" -> "Backend API & Framework Development ([new_project_name])"
        *   **Update `new_mode['slug']`**: Append `new_project_name_slugified`.
            *   Example: "backend-api-django-development" -> `backend-api-django-development-[new_project_name_slugified]`
        *   **Update text content (`roleDefinition`, `whenToUse`, `customInstructions`):**
            *   For each of these string fields in `new_mode`:
                1.  Replace all occurrences of "GuardianRoute" with `new_project_name`.
                2.  Replace path prefix `C:/git/GuardianRoute/TEMPLATE_PROJECT_OUTPUT/` with an empty string (``). This makes paths like `docs/01_Coding_Standards/Python_Django_StyleGuide.md` relative to the project root.
                3.  Replace path prefix `C:/git/GuardianRoute/management-portal/` with `C:/git/[new_project_name]/management-portal/`. (This assumes `management-portal` is an external but related directory structure whose root reference changes from "GuardianRoute" to the `new_project_name`).
        *   Add the fully processed `new_mode` to `final_project_modes`.
    *   Create the final JSON structure: `output_json = {"customModes": final_project_modes}`.
    *   Write `output_json` to `os.path.join(target_dir, 'custom_modes.json')`, overwriting the copied one.

*   **Step 7: Completion Message**
    *   Print a success message to the user, indicating the new project has been created at `C:\git\[new_project_name]`.

**5. Error Handling:**
*   Implement `try-except` blocks for file operations (directory creation, copying, reading/writing files) to catch potential `IOError`, `OSError`, etc.
*   Provide informative error messages to the user.

**6. Considerations:**
*   **Path Separators:** Be mindful of Windows (`\`) vs. POSIX (`/`) path separators. `os.path.join` and raw string literals (`r"path"`) help. Python's string replace is literal, so ensure the source strings match what's in the files. The `custom_modes.json` provided uses `\` in paths. The plan uses `/` for `C:/git/...` for consistency with how it might be written in cross-platform contexts, but the script should match the actual strings in the files. I'll assume the script will handle the actual separators found.
*   **File Encoding:** Assume UTF-8 for reading/writing text files, but this could be made configurable if necessary.
*   **Case Sensitivity:** String replacements are case-sensitive. Ensure the casing of "GuardianRoute", "TEMPLATE_PROJECT_OUTPUT" matches the source files.
*   **Idempotency:** Consider if the script needs to be runnable multiple times. The current plan (exiting if target exists) prevents accidental overwrites.