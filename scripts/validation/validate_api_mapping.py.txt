#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Validates an API_Mapping.txt file against project conventions.
"""
import argparse
import re
import json
import os

# Constants for file paths (can be overridden by args)
# Assumes script is run from the project root c:/git/ExcursionBooking
DEFAULT_API_MAPPING_FILE = os.path.join("management-portal", "src", "docs", "API_Mapping.txt")

def validate_json_block(json_string, line_number_start, errors_list, context):
    """Attempts to parse a JSON block and adds an error if it fails."""
    try:
        json.loads(json_string)
    except json.JSONDecodeError as e:
        errors_list.append(f"{context} - Invalid JSON: {e.message} (near content starting line {line_number_start})")

def validate_iso_8601_format(date_string, line_number, errors_list, context, field_name):
    """Validates if a string is in ISO 8601 format (simplified check)."""
    iso_8601_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,6})?Z$"
    if not re.match(iso_8601_pattern, date_string):
        errors_list.append(f"{context} - Field '{field_name}' (line {line_number}): '{date_string}' is not in expected ISO 8601 format (YYYY-MM-DDTHH:MM:SS[.ffffff]Z).")

def get_line_number_of_match(text_lines, block_start_line, pattern_to_find, occurrence=0):
    """Helper to find line number of a pattern within a block of lines."""
    current_occurrence = 0
    for i, line in enumerate(text_lines):
        if pattern_to_find in line:
            if current_occurrence == occurrence:
                return block_start_line + i
            current_occurrence += 1
    return block_start_line # Fallback

def validate_api_mapping(api_mapping_filepath):
    """
    Validates the API mapping file.
    Returns a tuple of (errors_list, warnings_list).
    """
    errors = []
    warnings = []
    full_file_lines = []

    try:
        with open(api_mapping_filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            full_file_lines = content.splitlines()
    except FileNotFoundError:
        errors.append(f"Error: API Mapping file not found at {api_mapping_filepath}")
        return errors, warnings

    # Split content into resource blocks using '---' as a separator
    # We need to handle line numbers carefully.
    # Let's find the line numbers of '---' separators first.
    separator_line_numbers = [i for i, line in enumerate(full_file_lines) if line.strip() == "---"]
    
    resource_block_definitions = []
    start_idx = 0
    for sep_line_num in separator_line_numbers:
        resource_block_definitions.append({
            "start_line": start_idx + 1, # 1-based
            "lines": full_file_lines[start_idx:sep_line_num]
        })
        start_idx = sep_line_num + 1
    # Add the last block
    if start_idx < len(full_file_lines):
         resource_block_definitions.append({
            "start_line": start_idx + 1,
            "lines": full_file_lines[start_idx:]
        })

    if not resource_block_definitions or not any(b['lines'] for b in resource_block_definitions):
        errors.append("No resource blocks found or file is empty. Expected '---' separators between resources.")
        return errors, warnings

    for i, res_block_def in enumerate(resource_block_definitions):
        block_lines = [line.strip() for line in res_block_def['lines'] if line.strip()] # Ignore empty lines within block for parsing
        if not block_lines:
            continue

        block_start_line_in_file = res_block_def['start_line']
        resource_context = f"Resource Block {i+1} (starts line ~{block_start_line_in_file})"

        resource_header_match = re.match(r"### Resource: (.*)", block_lines[0])
        if not resource_header_match:
            # If it's the first block (i=0), it might be a preamble. Skip if it doesn't look like a resource.
            if i == 0 and not block_lines[0].startswith("### Resource:"):
                # Check if any line in this first block looks like a resource header,
                # if not, it's likely a preamble.
                is_preamble = True
                for line_in_block in block_lines:
                    if line_in_block.startswith("### Resource:"):
                        is_preamble = False # Found a resource header, so not a preamble block
                        resource_header_match = re.match(r"### Resource: (.*)", line_in_block)
                        # Adjust block_lines to start from this actual resource header
                        try:
                            actual_header_idx = block_lines.index(line_in_block)
                            block_lines = block_lines[actual_header_idx:]
                        except ValueError:
                            pass # Should not happen if line_in_block is from block_lines
                        break
                if is_preamble:
                    # It's likely a preamble, let's see if the *next* block is a resource
                    # This logic is getting complex for a simple diff.
                    # A simpler approach for now: if it's the first block and doesn't start with ### Resource,
                    # and the file is not *only* this block, assume it's a preamble and skip.
                    if i == 0 and len(resource_block_definitions) > 1 : # if it's the first block AND there are other blocks
                         warnings.append(f"{resource_context}: Assuming this is a preamble as it does not start with '### Resource:'. Skipping this block for resource validation.")
                         continue
            
            errors.append(f"{resource_context}: Does not start with '### Resource: [Resource Name]'. Found: '{block_lines[0]}'")
            continue
        
        resource_name = resource_header_match.group(1).strip()
        if not resource_name or "[" in resource_name or "]" in resource_name:
            warnings.append(f"{resource_context}: Resource name '{resource_name}' seems to be a placeholder or empty.")
        resource_context = f"Resource '{resource_name}' (Block {i+1}, starts line ~{block_start_line_in_file})"

        # For main resource blocks, we expect ViewSet and Serializer info
        # Let's check for these specifically if it's not a special block like JWT
        is_special_block = "jwt token endpoints" in resource_name.lower() or "authentication endpoints" in resource_name.lower() or "report endpoints" in resource_name.lower()

        # General expected fields for all blocks (can be refined)
        # Description is good to have. Base Path is usually global.
        # Model/ViewSet/Serializer are critical for standard resources.
        expected_header_fields = {
             "Description:": None, # General description for the resource
        }
        # Fields specific to standard DRF resources
        expected_drf_resource_fields = {
            "ViewSet:": None,
            "Serializer:": None,
            "Permissions:": None # Permissions are also key
        }

        endpoints_header_found_at_line = -1
        
        for line_idx, line_content_stripped in enumerate(block_lines):
            actual_line_num = get_line_number_of_match(res_block_def['lines'], block_start_line_in_file, line_content_stripped)
            
            matched_field = False
            # Check for general header fields
            for field_key in expected_header_fields:
                if line_content_stripped.startswith(field_key):
                    expected_header_fields[field_key] = line_content_stripped.split(field_key, 1)[1].strip()
                    if not expected_header_fields[field_key] or ("[" in expected_header_fields[field_key] and "]" in expected_header_fields[field_key]):
                        warnings.append(f"{resource_context} - Field '{field_key.strip(':')}' (line {actual_line_num}): Value '{expected_header_fields[field_key]}' seems to be a placeholder or empty.")
                    matched_field = True
                    break
            
            if not is_special_block:
                # Check for DRF resource specific fields (ViewSet, Serializer, Permissions)
                for field_key in expected_drf_resource_fields:
                    # These often appear as markdown list items, e.g., "*   **ViewSet:** ..."
                    # So, we check if the line *contains* the key, not just starts with it, after stripping leading '* '
                    # For unbolded keys, direct startswith is fine.
                    if line_content_stripped.startswith(field_key): # field_key is now "ViewSet:", "Serializer:", "Permissions:"
                        expected_drf_resource_fields[field_key] = line_content_stripped.split(field_key, 1)[1].strip()
                        value_to_check = expected_drf_resource_fields[field_key]
                        is_link = re.match(r"`\[.*?\]\(.*?\)`", value_to_check) # Matches `[Text](link)`
                        
                        if not value_to_check or \
                           ( ("[" in value_to_check and "]" in value_to_check) and not is_link ) or \
                           value_to_check.lower() == "none specified." or \
                           value_to_check.lower() == "none":
                            # For Permissions, "Defined per endpoint" is acceptable.
                            if field_key == "Permissions:" and "defined per endpoint" in value_to_check.lower():
                                pass # This is an acceptable placeholder for resource-level permissions
                            else:
                                warnings.append(f"{resource_context} - Field '{field_key.strip(':')}' (line {actual_line_num}): Value '{value_to_check}' seems to be a placeholder, empty, or 'None'.")
                        
                        # Validate link format for ViewSet and Serializer if present
                        if (field_key == "ViewSet:" or field_key == "Serializer:") and is_link:
                            link_path_match = re.search(r"\(([^)]+)\)", value_to_check)
                            if link_path_match:
                                link_path = link_path_match.group(1)
                                if not re.match(r"(\.\./|./)[\w/.-]+(:#L?\d+)?", link_path): # Basic check for relative path + optional line
                                     warnings.append(f"{resource_context} - Field '{field_key.strip(':')}' (line {actual_line_num}): Link path '{link_path}' does not look like a valid relative code link.")
                            else:
                                warnings.append(f"{resource_context} - Field '{field_key.strip(':')}' (line {actual_line_num}): Malformed markdown link '{value_to_check}'.")
                        
                        matched_field = True
                        break
            
            if matched_field:
                continue

            if line_content_stripped == "#### Endpoints:":
                endpoints_header_found_at_line = actual_line_num
                endpoint_definitions_start_block_line_idx = line_idx + 1
                break
        
        # Validate presence of general header fields
        for field, value in expected_header_fields.items():
            if value is None:
                errors.append(f"{resource_context}: Missing expected field '{field.strip(':')}' in resource header.")

        # Validate presence of DRF specific fields for non-special blocks
        if not is_special_block:
            for field, value in expected_drf_resource_fields.items():
                if value is None:
                    errors.append(f"{resource_context}: Missing expected field '{field.strip(':*')}' (e.g., ViewSet, Serializer, Permissions) for standard resource.")
        
        if endpoints_header_found_at_line == -1:
            errors.append(f"{resource_context}: Missing '#### Endpoints:' header.")
            continue

        # Endpoint Block Validation
        if endpoint_definitions_start_block_line_idx < len(block_lines):
            endpoint_text_lines = block_lines[endpoint_definitions_start_block_line_idx:]
            
            # Find start of each endpoint (e.g., "1. List Users")
            current_endpoint_lines = []
            current_endpoint_start_line_in_block = -1

            for ep_line_idx, ep_line_content_stripped in enumerate(endpoint_text_lines):
                actual_ep_line_num_in_file = get_line_number_of_match(
                    res_block_def['lines'], block_start_line_in_file, ep_line_content_stripped, 
                    occurrence=res_block_def['lines'].count(ep_line_content_stripped)-1 # try to get the specific one
                ) if ep_line_content_stripped else block_start_line_in_file + endpoint_definitions_start_block_line_idx + ep_line_idx


                is_new_endpoint_start = re.match(r"(\d+)\.\s+(.*)", ep_line_content_stripped)
                if is_new_endpoint_start:
                    if current_endpoint_lines: # Process previous endpoint
                        _validate_single_endpoint(current_endpoint_lines, current_endpoint_start_line_in_block, resource_context, errors, warnings, res_block_def, block_start_line_in_file)
                    current_endpoint_lines = [ep_line_content_stripped]
                    current_endpoint_start_line_in_block = actual_ep_line_num_in_file
                elif current_endpoint_start_line_in_block != -1 : # if we are inside an endpoint block
                    current_endpoint_lines.append(ep_line_content_stripped)
            
            if current_endpoint_lines: # Process the last endpoint
                _validate_single_endpoint(current_endpoint_lines, current_endpoint_start_line_in_block, resource_context, errors, warnings, res_block_def, block_start_line_in_file)
    return errors, warnings

def _validate_single_endpoint(endpoint_lines, endpoint_start_line_in_file, resource_context, errors, warnings, original_resource_block_def, original_block_start_line_in_file):
    """Helper to validate a single endpoint's text block."""
    if not endpoint_lines:
        return

    first_line_stripped = endpoint_lines[0]
    endpoint_title_match = re.match(r"(\d+)\.\s+(.*)", first_line_stripped)
    if not endpoint_title_match: # Should have been caught by caller logic, but double check
        errors.append(f"{resource_context} - Endpoint definition (near line {endpoint_start_line_in_file}): Does not start with 'N. [Endpoint Name]'. Found: '{first_line_stripped}'")
        return
    
    endpoint_num = endpoint_title_match.group(1)
    endpoint_name_from_title = endpoint_title_match.group(2).strip()
    endpoint_context = f"{resource_context} - Endpoint {endpoint_num} ('{endpoint_name_from_title}', starts line ~{endpoint_start_line_in_file})"

    endpoint_fields_expected = {
        "Method:": None, "Endpoint:": None, "Description:": None,
        "Permissions:": None, "Success Response:": None, "Error Responses:": None
    }
    # Optional: "Query Parameters:", "Request Body:", "Path Parameters:"

    json_block_content = ""
    in_json_block = False
    json_block_start_line_approx = -1
    json_block_context_prefix = ""

    for e_line_idx, e_line_content_stripped in enumerate(endpoint_lines):
        # More accurate line number for current line within endpoint
        actual_line_num = get_line_number_of_match(original_resource_block_def['lines'], original_block_start_line_in_file, e_line_content_stripped) if e_line_content_stripped else endpoint_start_line_in_file + e_line_idx

        if e_line_content_stripped == "```json":
            in_json_block = True
            json_block_content = ""
            json_block_start_line_approx = actual_line_num
            # Determine context for this JSON block
            if e_line_idx > 0:
                prev_line = endpoint_lines[e_line_idx-1].strip()
                if prev_line.lower().startswith("request body:"): json_block_context_prefix = "Request Body"
                elif prev_line.lower().startswith("body:"):
                    # Look further back
                    for k_idx in range(e_line_idx - 2, -1, -1):
                        look_back_line = endpoint_lines[k_idx].strip()
                        if look_back_line.lower().startswith("success response:"): json_block_context_prefix = "Success Response Body"; break
                        elif look_back_line.lower().startswith("error responses:"): json_block_context_prefix = "Error Response Example"; break
                if not json_block_context_prefix: json_block_context_prefix = "Unidentified"
            else: json_block_context_prefix = "Unidentified"
            continue
        elif e_line_content_stripped == "```" and in_json_block:
            in_json_block = False
            current_json_context = f"{endpoint_context} - {json_block_context_prefix} JSON"
            if json_block_content:
                validate_json_block(json_block_content, json_block_start_line_approx, errors, current_json_context)
                try:
                    parsed_json = json.loads(json_block_content)
                    items_to_check = []
                    if isinstance(parsed_json, dict) and "results" in parsed_json and isinstance(parsed_json["results"], list):
                        items_to_check.extend(parsed_json["results"])
                    elif isinstance(parsed_json, list): # For cases where the root is a list
                        items_to_check.extend(parsed_json)
                    elif isinstance(parsed_json, dict):
                         items_to_check.append(parsed_json)
                    
                    for item_idx, item in enumerate(items_to_check):
                        if isinstance(item, dict):
                            for ts_field in ["created_at", "updated_at", "timestamp", "date_joined", "last_login"]:
                                if ts_field in item and isinstance(item[ts_field], str):
                                    # Try to find the line of this field in the json_block_content
                                    field_line_in_json_block = -1
                                    for json_line_idx, json_line_str in enumerate(json_block_content.splitlines()):
                                        if f'"{ts_field}"' in json_line_str: # Basic check
                                            field_line_in_json_block = json_line_idx
                                            break
                                    field_line_approx_in_file = json_block_start_line_approx + field_line_in_json_block +1 if field_line_in_json_block !=-1 else json_block_start_line_approx
                                    
                                    item_context_suffix = f" (item {item_idx})" if len(items_to_check) > 1 else ""
                                    validate_iso_8601_format(item[ts_field], field_line_approx_in_file, errors, f"{current_json_context}{item_context_suffix}", ts_field)
                except json.JSONDecodeError: pass # Already handled
            json_block_content = ""; json_block_start_line_approx = -1; json_block_context_prefix = ""
            continue
        
        if in_json_block:
            json_block_content += e_line_content_stripped + "\n" # Use stripped to avoid mixed indentation issues in parser
            continue

        matched_field_in_endpoint = False
        for e_field_key in endpoint_fields_expected:
            if e_line_content_stripped.startswith(e_field_key):
                endpoint_fields_expected[e_field_key] = e_line_content_stripped.split(e_field_key, 1)[1].strip()
                if not endpoint_fields_expected[e_field_key] or \
                   ("[" in endpoint_fields_expected[e_field_key] and "]" in endpoint_fields_expected[e_field_key] and e_field_key != "Permissions:"):
                    warnings.append(f"{endpoint_context} - Field '{e_field_key.strip(':')}' (line {actual_line_num}): Value '{endpoint_fields_expected[e_field_key]}' seems to be a placeholder or empty.")
                
                if e_field_key == "Method:":
                    valid_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
                    if endpoint_fields_expected[e_field_key] not in valid_methods:
                        errors.append(f"{endpoint_context} - Invalid HTTP Method '{endpoint_fields_expected[e_field_key]}' (line {actual_line_num}). Expected one of {valid_methods}.")
                matched_field_in_endpoint = True
                break
        # if matched_field_in_endpoint: continue # No, other logic might apply to same line

    if in_json_block:
        errors.append(f"{endpoint_context} - {json_block_context_prefix} JSON: Unclosed JSON block (```) at the end of the endpoint definition.")

    for e_field, e_value in endpoint_fields_expected.items():
        if e_value is None:
            errors.append(f"{endpoint_context}: Missing expected field '{e_field.strip(':')}' in endpoint definition.")


def main():
    """Main function to parse arguments and run validation."""
    parser = argparse.ArgumentParser(description="Validate an API_Mapping.txt file against project conventions.")
    parser.add_argument(
        "filepath",
        nargs="?",
        default=DEFAULT_API_MAPPING_FILE,
        help=f"Path to the API_Mapping.txt file. Defaults to '{DEFAULT_API_MAPPING_FILE}'"
    )
    args = parser.parse_args()

    # Ensure the path is absolute or correctly relative to CWD (project root)
    filepath_to_check = args.filepath
    if not os.path.isabs(filepath_to_check):
        filepath_to_check = os.path.join(os.getcwd(), filepath_to_check) # Should be c:/git/ExcursionBooking

    print(f"Validating API mapping file: {filepath_to_check}\n")
    errors, warnings = validate_api_mapping(filepath_to_check)

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