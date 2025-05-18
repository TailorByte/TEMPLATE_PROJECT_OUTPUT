#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generates boilerplate DBML for new tables or enums.
"""
import argparse
import re
import os

def to_snake_case_for_pk(name):
    """Converts PascalCase to snake_case for PK, e.g., UserProfile -> user_profile_id."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def generate_dbml_table_markdown(table_name_pascal_case, pk_type="bigint_increment"):
    """
    Generates the DBML markdown string for a new table.
    pk_type can be "bigint_increment" or "uuid".
    """
    if not table_name_pascal_case or not table_name_pascal_case[0].isupper():
        raise ValueError("Table name should be in PascalCase (e.g., UserProfiles, ProductItems).")

    # For display names, try to be a bit smarter with spaces
    table_display_name_singular = re.sub(r'(?<!^)(?=[A-Z])', ' ', table_name_pascal_case) # UserProfile -> User Profile
    if table_name_pascal_case.endswith('s'): # If it's already plural like "Users"
        table_display_name_singular = table_display_name_singular[:-1]


    pk_col_name = "id" # Default to simple 'id'
    # Alternative: to_snake_case_for_pk(table_display_name_singular.replace(" ", "")) + "_id"
    
    if pk_type == "uuid":
        pk_definition = f"{pk_col_name} uuid [pk, default: `uuid_generate_v4()`]"
    else: # Default to bigint_increment
        pk_definition = f"{pk_col_name} bigint [pk, increment]"

    template = f"""
Table {table_name_pascal_case} {{
  {pk_definition}
  // TODO: Add other columns for {table_name_pascal_case}
  // Example: name varchar(255) [not null]
  // Example: description text
  // Example: status [SomeStatusEnum]
  // Example: parent_id bigint [ref: > ParentTable.id]

  created_at timestamp [default: `now()`, not null]
  updated_at timestamp [default: `now()`, not null]

  Indexes {{
    // TODO: Add relevant indexes
    // Example: (name)
  }}
  Note: 'Stores information about {table_display_name_singular.lower()}s.'
}}
"""
    return template.strip()

def generate_dbml_enum_markdown(enum_name_pascal_case):
    """
    Generates the DBML markdown string for a new enum.
    """
    if not enum_name_pascal_case or not enum_name_pascal_case[0].isupper():
        raise ValueError("Enum name should be in PascalCase (e.g., UserStatus, OrderType).")

    template = f"""
Enum {enum_name_pascal_case} {{
  // TODO: Add enum values (typically uppercase)
  VALUE_1
  VALUE_2
  VALUE_3
}}
"""
    return template.strip()

def main():
    """Main function to parse arguments and print generated DBML."""
    parser = argparse.ArgumentParser(description="Generate boilerplate DBML for a new table or enum.")
    parser.add_argument(
        "element_type",
        choices=["table", "enum"],
        help="The type of DBML element to generate ('table' or 'enum')."
    )
    parser.add_argument(
        "element_name",
        help="The name of the table or enum in PascalCase (e.g., UserProfile, OrderStatus)."
    )
    parser.add_argument(
        "--pk_type",
        choices=["bigint_increment", "uuid"],
        default="bigint_increment",
        help="For tables only: the type of primary key ('bigint_increment' or 'uuid'). Default: bigint_increment."
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Optional: Filepath to append the generated DBML to. If not provided, prints to stdout."
    )
    args = parser.parse_args()

    try:
        dbml_output = ""
        if args.element_type == "table":
            dbml_output = generate_dbml_table_markdown(args.element_name, args.pk_type)
        elif args.element_type == "enum":
            dbml_output = generate_dbml_enum_markdown(args.element_name)
        
        if args.output:
            mode = 'a' if os.path.exists(args.output) else 'w'
            with open(args.output, mode, encoding='utf-8') as f:
                if mode == 'a': # Add a newline if appending to an existing file
                    f.write("\n\n") # Add two newlines for better separation
                f.write(dbml_output)
            print(f"DBML for {args.element_type} '{args.element_name}' has been appended to {args.output}")
        else:
            print(dbml_output)

    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()