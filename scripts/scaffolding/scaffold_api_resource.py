#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generates boilerplate markdown for a new API resource.
"""
import argparse
import re

def to_snake_case(name):
    """Converts PascalCase or CamelCase to snake_case."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def generate_resource_markdown(resource_name_pascal_case):
    """
    Generates the markdown string for a new API resource.
    """
    if not resource_name_pascal_case or not resource_name_pascal_case[0].isupper():
        raise ValueError("Resource name should be in PascalCase (e.g., UserProfile, ProductItem).")

    resource_plural_snake = to_snake_case(resource_name_pascal_case) + "s" # Simple pluralization
    resource_singular_snake = to_snake_case(resource_name_pascal_case)
    
    # Adjust for common "s" ending pluralization if original ends in "s"
    if resource_name_pascal_case.endswith('s'):
         resource_plural_snake = to_snake_case(resource_name_pascal_case) # e.g. Address -> addresses
    elif resource_name_pascal_case.endswith('y') and not resource_name_pascal_case.endswith(('ay', 'ey', 'iy', 'oy', 'uy')):
        resource_plural_snake = to_snake_case(resource_name_pascal_case[:-1]) + "ies" # e.g. Category -> categories
    
    # For display names, try to be a bit smarter with spaces
    resource_display_name_singular = re.sub(r'(?<!^)(?=[A-Z])', ' ', resource_name_pascal_case) # UserProfile -> User Profile
    resource_display_name_plural = resource_display_name_singular + "s"
    if resource_name_pascal_case.endswith('y') and not resource_name_pascal_case.endswith(('ay', 'ey', 'iy', 'oy', 'uy')):
        resource_display_name_plural = resource_display_name_singular[:-1] + "ies"


    template = f"""---

### Resource: {resource_display_name_singular}

**Base Path:** `/api/v1/{resource_plural_snake}`

**Description:** A brief description of what the {resource_display_name_singular} resource represents.

**Associated Model (Django):** `[app_name].models.{resource_name_pascal_case}`
**Associated ViewSet/View (Django):** `[app_name].views.{resource_name_pascal_case}ViewSet`
**Associated Serializer (Django):** `[app_name].serializers.{resource_name_pascal_case}Serializer`

#### Endpoints:

**1. List {resource_display_name_plural}**

*   **Method:** `GET`
*   **Endpoint:** `/api/v1/{resource_plural_snake}/`
*   **Description:** Retrieves a list of {resource_display_name_plural}. Supports filtering, sorting, and pagination.
*   **Permissions:** `[IsAuthenticated, CustomPermission(View{resource_name_pascal_case})]`
*   **Query Parameters:**
    *   `page` (integer, optional): Page number for pagination. Default: `1`.
    *   `page_size` (integer, optional): Number of items per page. Default: `[default_page_size]`.
    *   `search` (string, optional): Search term to filter results by [relevant_fields].
    *   `ordering` (string, optional): Field to sort by (e.g., `name`, `-created_at`).
    *   `[filter_field_1]` ([type], optional): Filter by [description_of_filter_field_1].
*   **Request Body:** None
*   **Success Response:**
    *   **Code:** `200 OK`
    *   **Body:**
        ```json
        {{
          "count": 0,
          "next": null,
          "previous": null,
          "results": [
            {{
              "id": "[uuid/integer]",
              "name": "[Example Name]", // Placeholder field
              // ... other fields as defined in the {resource_name_pascal_case}Serializer
              "created_at": "YYYY-MM-DDTHH:mm:ss.sssZ",
              "updated_at": "YYYY-MM-DDTHH:mm:ss.sssZ"
            }}
          ]
        }}
        ```
*   **Error Responses:**
    *   `401 Unauthorized`
    *   `403 Forbidden`

**2. Create {resource_display_name_singular}**

*   **Method:** `POST`
*   **Endpoint:** `/api/v1/{resource_plural_snake}/`
*   **Description:** Creates a new {resource_display_name_singular}.
*   **Permissions:** `[IsAuthenticated, CustomPermission(Create{resource_name_pascal_case})]`
*   **Request Body:** `application/json`
    ```json
    {{
      "name": "[Example Name]" // (string, required, Description of this field)
      // ... other creatable fields
    }}
    ```
    *   **Field Descriptions:**
        *   `name` (`string`, required): Example field description.
*   **Success Response:**
    *   **Code:** `201 Created`
    *   **Headers:** `Location: /api/v1/{resource_plural_snake}/[new_resource_id]/`
    *   **Body:**
        ```json
        {{
          "id": "[new_resource_id]",
          "name": "[Example Name]",
          // ... all fields of the created resource
          "created_at": "YYYY-MM-DDTHH:mm:ss.sssZ",
          "updated_at": "YYYY-MM-DDTHH:mm:ss.sssZ"
        }}
        ```
*   **Error Responses:**
    *   `400 Bad Request` (Validation errors)
    *   `401 Unauthorized`
    *   `403 Forbidden`

**3. Retrieve {resource_display_name_singular}**

*   **Method:** `GET`
*   **Endpoint:** `/api/v1/{resource_plural_snake}/{{id}}/`
*   **Description:** Retrieves a specific {resource_display_name_singular} by its ID.
*   **Permissions:** `[IsAuthenticated, CustomPermission(View{resource_name_pascal_case})]`
*   **Path Parameters:**
    *   `id` ([uuid/integer], required): The ID of the {resource_display_name_singular}.
*   **Request Body:** None
*   **Success Response:**
    *   **Code:** `200 OK`
    *   **Body:**
        ```json
        {{
          "id": "[resource_id]",
          "name": "[Example Name]",
          // ... all fields of the resource
          "created_at": "YYYY-MM-DDTHH:mm:ss.sssZ",
          "updated_at": "YYYY-MM-DDTHH:mm:ss.sssZ"
        }}
        ```
*   **Error Responses:**
    *   `401 Unauthorized`
    *   `403 Forbidden`
    *   `404 Not Found`

**4. Update {resource_display_name_singular} (Full Update)**

*   **Method:** `PUT`
*   **Endpoint:** `/api/v1/{resource_plural_snake}/{{id}}/`
*   **Description:** Fully updates an existing {resource_display_name_singular}.
*   **Permissions:** `[IsAuthenticated, CustomPermission(Edit{resource_name_pascal_case})]`
*   **Path Parameters:**
    *   `id` ([uuid/integer], required): The ID of the {resource_display_name_singular} to update.
*   **Request Body:** `application/json`
    ```json
    {{
      "name": "[New Example Name]"
      // ... all mutable required fields
    }}
    ```
*   **Success Response:**
    *   **Code:** `200 OK`
    *   **Body:** (The updated resource object, same format as GET single)
*   **Error Responses:**
    *   `400 Bad Request`
    *   `401 Unauthorized`
    *   `403 Forbidden`
    *   `404 Not Found`

**5. Partially Update {resource_display_name_singular}**

*   **Method:** `PATCH`
*   **Endpoint:** `/api/v1/{resource_plural_snake}/{{id}}/`
*   **Description:** Partially updates an existing {resource_display_name_singular}.
*   **Permissions:** `[IsAuthenticated, CustomPermission(Edit{resource_name_pascal_case})]`
*   **Path Parameters:**
    *   `id` ([uuid/integer], required): The ID of the {resource_display_name_singular} to update.
*   **Request Body:** `application/json`
    ```json
    {{
      "name": "[Updated Example Name]"
      // ... only fields to be updated
    }}
    ```
*   **Success Response:**
    *   **Code:** `200 OK`
    *   **Body:** (The updated resource object, same format as GET single)
*   **Error Responses:**
    *   `400 Bad Request`
    *   `401 Unauthorized`
    *   `403 Forbidden`
    *   `404 Not Found`

**6. Delete {resource_display_name_singular}**

*   **Method:** `DELETE`
*   **Endpoint:** `/api/v1/{resource_plural_snake}/{{id}}/`
*   **Description:** Deletes a specific {resource_display_name_singular}.
*   **Permissions:** `[IsAuthenticated, CustomPermission(Delete{resource_name_pascal_case})]`
*   **Path Parameters:**
    *   `id` ([uuid/integer], required): The ID of the {resource_display_name_singular} to delete.
*   **Request Body:** None
*   **Success Response:**
    *   **Code:** `204 No Content`
    *   **Body:** None
*   **Error Responses:**
    *   `401 Unauthorized`
    *   `403 Forbidden`
    *   `404 Not Found`

"""
    return template

def main():
    """Main function to parse arguments and print generated markdown."""
    parser = argparse.ArgumentParser(description="Generate boilerplate markdown for a new API resource.")
    parser.add_argument(
        "resource_name",
        help="The name of the resource in PascalCase (e.g., UserProfile, ProductItem)."
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Optional: Filepath to append the generated markdown to. If not provided, prints to stdout."
    )
    args = parser.parse_args()

    try:
        markdown_output = generate_resource_markdown(args.resource_name)
        if args.output:
            mode = 'a' if os.path.exists(args.output) else 'w'
            with open(args.output, mode, encoding='utf-8') as f:
                if mode == 'a': # Add a newline if appending to an existing file
                    f.write("\n") 
                f.write(markdown_output)
            print(f"Markdown for resource '{args.resource_name}' has been appended to {args.output}")
        else:
            print(markdown_output)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()