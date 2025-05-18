# Plan to Refactor `initialize_new_project.py` (v2 - Updated for custom_modes.json Path Correction)

**1. Introduction**
This plan updates the previous refactoring plan for `scripts/initialize_new_project.py`. The primary goal remains to improve path handling. This version specifically focuses on correcting the path references within the generated `custom_modes.json` file. Key documents (like `API_Mapping.txt`, `DBML.txt`) are confirmed to be located in `TEMPLATE_PROJECT_OUTPUT/docs/` and are copied correctly by the script to `NewProjectName/docs/`. The main task for this update is to ensure references within the generated `custom_modes.json` point to this correct `docs/` location instead of the erroneous `management-portal/src/docs/` prefix.

**2. Proposed Changes to `initialize_new_project.py`**

*   **2.1. Configuration for Base and Source Directories**
    *   **(No change from original plan)** Implement `argparse` to allow command-line configuration for base and source directories.
    *   **Details:**
        *   Arguments: `--source-dir-path` (default: script's parent dir), `--base-git-dir` (default: parent of `source-dir-path`).
        *   Script uses parsed values instead of hardcoded `SOURCE_DIR_PATH` and `BASE_GIT_DIR`.

*   **2.2. Locating Source `custom_modes.json`**
    *   **(No change from original plan)** Robustly locate `custom_modes.json` using `os.path.join(resolved_source_dir_path, "custom_modes.json")`.

*   **2.3. Refining `replace_in_file_content` Function**
    *   **(No change from original plan)** Modify the function for more precise replacements.
    *   **Details:**
        *   Signature: `def replace_in_file_content(content, new_project_name, new_project_name_slugified, base_git_dir_val, source_project_root_val, placeholder_template_dir_name_val):`
        *   Replacements: `PLACEHOLDER_PROJECT_NAME_GENERIC`, `DJANGO_CORE_PLACEHOLDER_NAME`, full absolute template path.
        *   **Critical:** Remove broad `content = content.replace(PLACEHOLDER_TEMPLATE_DIR_NAME, new_project_name)` replacement.

*   **2.4. Correcting Path References in `process_custom_modes_json` (UPDATED)**
    *   **Action:** Modify the `process_custom_modes_json` function to specifically remove the `management-portal/src/` prefix from relevant document paths found in text fields like `customInstructions`.
    *   **Details:**
        *   Within the loop that processes `roleDefinition`, `whenToUse`, and `customInstructions`:
            ```python
            # ... existing code ...
            text_content = new_mode[key]
            text_content = text_content.replace(PLACEHOLDER_PROJECT_NAME_GENERIC, new_project_name)

            # NEW: Correct the document path prefixes
            text_content = text_content.replace("management-portal/src/docs/", "docs/")
            # Add similar replacements if other incorrect prefixes exist for other files.
            # Example: text_content = text_content.replace("management-portal/src/scripts/", "scripts/")
            # (This should be verified against the actual content of custom_modes.json to ensure all such incorrect prefixes are handled)

            new_mode[key] = text_content
            # ... rest of the loop ...
            ```
        *   This targeted string replacement will correct paths like `management-portal/src/docs/API_Mapping.txt` to `docs/API_Mapping.txt`.
        *   The previous simplification of removing `original_template_output_in_guardianroute_path` etc. remains valid.

**3. Mermaid Diagram of Initialization Flow (Highlighting Changes - v2)**

```mermaid
graph TD
    A[Start: Run initialize_new_project.py] --> B{Parse Args};
    B --> C[Get New Project Name & Target Path];
    C --> D[Copy Template Files (docs/ location is correct in source)];
    D --> E[Rename backend_template & frontend_template dirs];
    E --> F[Rename Django core project dir];
    F --> G[Global Content Replacement Loop];
    G --> H{Call replace_in_file_content (Refined)};
    H --> I[Replace: PLACEHOLDER_PROJECT_NAME_GENERIC];
    H --> J[Replace: DJANGO_CORE_PLACEHOLDER_NAME];
    H --> K[Replace: Full Absolute Template Path];
    H --> L[REMOVED: Broad 'PLACEHOLDER_TEMPLATE_DIR_NAME' replacement];
    G --> M[Update frontend/package.json name];
    M --> N[Process custom_modes.json];
    N --> O{Call process_custom_modes_json (Path Correction Logic - UPDATED)};
    O --> P[Replace: PLACEHOLDER_PROJECT_NAME_GENERIC in text fields];
    O --> P_NEW[REFINED: Replace "management-portal/src/docs/" with "docs/" in text fields];
    O --> R[Retain: Slug & Name updates];
    N --> S[Create .env file];
    S --> T[Optional: Git Init, Install Deps];
    T --> U[End: Project Initialized];

    style P_NEW fill:#f9f,stroke:#333,stroke-width:2px
```

**4. Confirmation Points**
*   Dynamic defaults for paths are suitable.
*   Removing broad `PLACEHOLDER_TEMPLATE_DIR_NAME` replacement is correct.
*   Key documents (`API_Mapping.txt`, `DBML.txt`, etc.) are sourced from `TEMPLATE_PROJECT_OUTPUT/docs/` and correctly copied to `NewProjectName/docs/`.
*   The only required change for these document paths is to update string references within `custom_modes.json` by removing the `management-portal/src/` prefix.
*   No file system operations (moving files, deleting directories like `management-portal`) are needed for this specific path correction.