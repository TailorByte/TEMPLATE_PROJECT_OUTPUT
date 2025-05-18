#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Validates a DBML.txt file against project conventions.
"""
import argparse
import re
import os

DEFAULT_DBML_FILE = os.path.join("management-portal", "src", "docs", "DBML.txt")

# --- DBML Convention Constants (from template) ---
PASCAL_CASE_PATTERN = r"^[A-Z][a-zA-Z0-9]*$"
SNAKE_CASE_PATTERN = r"^[a-z0-9_]+$"
PK_NAME_PATTERN_ID_SPECIFIC = r"^[a-z0-9_]+_id$" # e.g. user_id, product_item_id
PK_TYPE_PATTERN_BIGINT = r"^bigint\s*\[pk\s*,\s*increment\]$"
PK_TYPE_PATTERN_UUID = r"^uuid\s*\[pk(,\s*default:\s*`uuid_generate_v4\(\)`)?\]$" # Allow optional default for UUID
FK_NAME_PATTERN = r"^[a-z0-9_]+_id$"
FK_REF_PATTERN = r"ref:\s*>\s*[A-Za-z0-9_]+\.[a-z0-9_]+"
TIMESTAMP_PATTERN_CREATED_AT = r"^created_at\s+timestamp\s*\[default:\s*`now\(\)`\s*,\s*not null\]$"
TIMESTAMP_PATTERN_UPDATED_AT = r"^updated_at\s+timestamp\s*\[default:\s*`now\(\)`\s*,\s*not null\]$"

def validate_dbml(dbml_filepath):
    """
    Validates the DBML file.
    Returns a tuple of (errors_list, warnings_list).
    """
    errors = []
    warnings = []
    
    try:
        with open(dbml_filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        errors.append(f"Error: DBML file not found at {dbml_filepath}")
        return errors, warnings

    defined_enums = set()
    current_table_name = None
    is_in_table_block = False
    has_version_comment = False
    has_changelog_indications = False
    # Check first few lines for version and changelog
    for i, line_content in enumerate(lines[:15]): # Check roughly first 15 lines
        stripped_line_for_header = line_content.strip()
        if re.search(r"//.*DBML\s*-\s*v\d+", stripped_line_for_header, re.IGNORECASE):
            has_version_comment = True
        if stripped_line_for_header.startswith("// -") or \
           stripped_line_for_header.lower().startswith("// previous changes:") or \
           stripped_line_for_header.lower().startswith("// changelog:"):
            has_changelog_indications = True
        if has_version_comment and has_changelog_indications:
            break
            
    if not has_version_comment:
        warnings.append("DBML file does not appear to have a version comment (e.g., '// Transport Management System DBML - v1') in the header.")
    if not has_changelog_indications:
        warnings.append("DBML file does not appear to have a changelog section (e.g., lines starting with '// -' or '// Previous changes:') in the header.")

    is_in_indexes_block = False

    for line_num_0based, line_content in enumerate(lines):
        line_num = line_num_0based + 1
        stripped_line = line_content.strip()

        if not stripped_line or stripped_line.startswith("//") or stripped_line.startswith("/*") or stripped_line.endswith("*/"):
            continue # Skip empty lines and comments

        # Project Definition
        if stripped_line.startswith("Project "):
            if "database_type: 'PostgreSQL'" not in stripped_line and "database_type: 'PostgreSQL'" not in lines[line_num_0based+1].strip(): # check next line too
                warnings.append(f"Line {line_num}: Project definition found, but 'database_type: PostgreSQL' is recommended.")
        
        # Enum Definitions
        enum_match = re.match(r"Enum\s+([A-Za-z0-9_]+)\s*\{", stripped_line)
        if enum_match:
            enum_name = enum_match.group(1)
            if not re.match(PASCAL_CASE_PATTERN, enum_name): # Enums often PascalCase
                 warnings.append(f"Line {line_num}: Enum name '{enum_name}' is not in PascalCase (e.g., UserStatus).")
            defined_enums.add(enum_name)
            continue
        
        # Table Definitions
        table_match = re.match(r"Table\s+([A-Za-z0-9_]+)\s*\{", stripped_line)
        if table_match:
            current_table_name = table_match.group(1)
            is_in_table_block = True
            is_in_indexes_block = False # Reset when new table starts
            if not re.match(PASCAL_CASE_PATTERN, current_table_name):
                errors.append(f"Line {line_num}: Table name '{current_table_name}' is not in PascalCase (e.g., Users, ProductItems).")
            
            # Check for Django User model specifics if table is "Users"
            if current_table_name == "Users":
                # This would require looking ahead or storing table content, complex for simple line-by-line
                # For now, this is a placeholder for a more advanced check
                pass 
            continue

        if stripped_line == "}": # End of a block (Table, Enum, Indexes, Project)
            if is_in_indexes_block:
                is_in_indexes_block = False
            elif is_in_table_block:
                is_in_table_block = False
                current_table_name = None
            # Could also be end of Enum or Project, no special state needed for those after parsing name
            continue
            
        if is_in_table_block:
            if stripped_line.lower() == "indexes {":
                is_in_indexes_block = True
                continue
            
            if is_in_indexes_block:
                # Enhanced check for various valid index formats
                # Pattern 1: (col1, col2, ...) [props] or (expression) [props] or (col1, col2)
                # Covers (col1,col2), (col1,col2)[unique], (name)[name:'foo'], (`lower(name)`)
                pat_composite_or_expr = r"^\s*\([^)]+\)\s*(\[.*\])?\s*$"

                # Pattern 2: col_name [props] or col_name (simple identifier)
                pat_single_col = r"^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*(\[.*\])?\s*$"

                # Pattern 3: Primary Key (cols) declaration
                pat_primary_key_decl = r"Primary Key\s*\([a-zA-Z0-9_,\s]+\)"

                is_valid_index_format = False
                if re.match(pat_composite_or_expr, stripped_line):
                    is_valid_index_format = True
                elif re.match(pat_single_col, stripped_line):
                    is_valid_index_format = True
                elif re.match(pat_primary_key_decl, stripped_line, re.IGNORECASE):
                    is_valid_index_format = True

                if not is_valid_index_format:
                     warnings.append(f"Line {line_num} (Table: {current_table_name}, Index): Index definition '{stripped_line}' seems malformed or uses an unsupported syntax.")
                continue

            # Column Definitions (inside a table, not in an indexes block)

            # Skip "Note:" lines from column parsing and validation
            if stripped_line.startswith("Note:"):
                continue

            # Example: user_id bigint [pk, increment]
            # Example: status UserStatus [default: 'PENDING_VERIFICATION']
            # Example: name varchar(150) [unique, not null]
            column_parts = stripped_line.split(maxsplit=2) # name, type, constraints
            if len(column_parts) < 2:
                # "Note:" lines are now skipped by the check above.
                # "Indexes {" should be caught by the logic at line 109 if it's a standalone `indexes {` line.
                # This warning is for other short/malformed lines.
                if not stripped_line.startswith("Indexes {"): # Check for "Indexes {" just in case
                    warnings.append(f"Line {line_num} (Table: {current_table_name}): Line '{stripped_line}' does not look like a valid column definition or Indexes block start.")
                continue

            col_name = column_parts[0]
            col_type = column_parts[1]
            col_constraints_str = column_parts[2] if len(column_parts) > 2 else ""

            if not re.match(SNAKE_CASE_PATTERN, col_name):
                errors.append(f"Line {line_num} (Table: {current_table_name}): Column name '{col_name}' is not in snake_case (e.g., user_id, first_name).")

            # Primary Key Checks
            is_pk = "[pk" in col_constraints_str.lower()
            if is_pk:
                table_singular_name = current_table_name[:-1].lower() if current_table_name.endswith('s') else current_table_name.lower()
                expected_pk_name = f"{table_singular_name}_id"
                if col_name != "id" and col_name != expected_pk_name:
                    warnings.append(f"Line {line_num} (Table: {current_table_name}): Primary key name '{col_name}' is not 'id' or '{expected_pk_name}'.")
                
                if not (re.match(PK_TYPE_PATTERN_BIGINT, f"{col_type} {col_constraints_str}") or \
                        re.match(PK_TYPE_PATTERN_UUID, f"{col_type} {col_constraints_str}")):
                    errors.append(f"Line {line_num} (Table: {current_table_name}, PK: {col_name}): Type definition '{col_type} {col_constraints_str}' does not match expected PK patterns (bigint [pk, increment] or uuid [pk...]).")
            
            # Foreign Key Checks
            if "ref:" in col_constraints_str:
                if not re.match(FK_NAME_PATTERN, col_name):
                     warnings.append(f"Line {line_num} (Table: {current_table_name}): Foreign key name '{col_name}' does not seem to follow convention (e.g., referenced_table_singular_id).")
                if not re.search(FK_REF_PATTERN, col_constraints_str): # Search because ref can be part of larger constraint string
                    errors.append(f"Line {line_num} (Table: {current_table_name}, FK: {col_name}): Foreign key reference 'ref: > ReferencedTable.column' seems malformed in '{col_constraints_str}'.")

            # Timestamp Checks
            if col_name == "created_at":
                if not re.match(TIMESTAMP_PATTERN_CREATED_AT, f"{col_name} {col_type} {col_constraints_str}"):
                    errors.append(f"Line {line_num} (Table: {current_table_name}): Column 'created_at' definition does not match convention 'created_at timestamp [default: `now()`, not null]'. Found: '{stripped_line}'")
            elif col_name == "updated_at":
                if not re.match(TIMESTAMP_PATTERN_UPDATED_AT, f"{col_name} {col_type} {col_constraints_str}"):
                     errors.append(f"Line {line_num} (Table: {current_table_name}): Column 'updated_at' definition does not match convention 'updated_at timestamp [default: `now()`, not null]'. Found: '{stripped_line}'")
            
            # Enum Usage Check
            if col_type in defined_enums:
                # This is a basic check; DBML syntax allows `MyEnum` as a type.
                pass # Correctly identified
            elif col_type[0].isupper() and col_type not in ["Table", "Enum", "Project", "Ref"] and col_type not in defined_enums: # Heuristic for potential undefined enum
                 warnings.append(f"Line {line_num} (Table: {current_table_name}): Column '{col_name}' uses type '{col_type}' which looks like an Enum but is not defined.")


    return errors, warnings

def main():
    """Main function to parse arguments and run validation."""
    parser = argparse.ArgumentParser(description="Validate a DBML.txt file against project conventions.")
    parser.add_argument(
        "filepath",
        nargs="?",
        default=DEFAULT_DBML_FILE,
        help=f"Path to the DBML.txt file. Defaults to '{DEFAULT_DBML_FILE}'"
    )
    args = parser.parse_args()

    filepath_to_check = args.filepath
    if not os.path.isabs(filepath_to_check):
        filepath_to_check = os.path.join(os.getcwd(), filepath_to_check)

    print(f"Validating DBML file: {filepath_to_check}\n")
    errors, warnings = validate_dbml(filepath_to_check)

    if warnings:
        print("--- Warnings ---")
        for warning in warnings:
            print(f"- {warning}")
        print("\n")
    
    if errors:
        print("--- Errors ---")
        for error in errors:
            print(f"- {error}")
        print(f"\nValidation FAILED with {len(errors)} error(s).")
        exit(1)
    else:
        print("Validation SUCCESSFUL! No critical errors found.")

if __name__ == "__main__":
    main()