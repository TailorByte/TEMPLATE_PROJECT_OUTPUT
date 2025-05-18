# API Design and Mapping Template

This document serves as a template and guide for designing and documenting APIs within this project. Consistent API design is crucial for maintainability, usability, and integration.

## 1. General Principles

*   **RESTful Design:** Adhere to REST principles where appropriate. Use standard HTTP methods, status codes, and resource-oriented URLs.
*   **Statelessness:** APIs should be stateless. Each request from a client should contain all the information needed to understand and process the request.
*   **Clear Naming Conventions:** Use clear, consistent, and predictable names for resources, endpoints, and parameters. Prefer plural nouns for resource collections (e.g., `/users`, `/products`).
*   **Versioning:** Implement API versioning from the start to manage changes without breaking existing clients. URL-based versioning is common (e.g., `/api/v1/resource`).
*   **Security:**
    *   Use HTTPS for all API communication.
    *   Implement robust authentication (see [`Authentication_Guide.md`](../02_Architecture/Authentication_Guide.md) or the project's equivalent).
    *   Implement proper authorization/permission checks for all endpoints. Permissions are often handled by a combination of base authentication (e.g., `IsAuthenticated`) and a more granular system (e.g., module-based permissions like `[CustomPermission (ViewResource)]` or `[CustomPermission (EditResource)]`).
*   **Idempotency:** Ensure that unsafe methods (POST, PUT, PATCH, DELETE) are handled correctly, especially PUT and DELETE which should be idempotent.
*   **Filtering, Sorting, Pagination:** Provide mechanisms for clients to filter, sort, and paginate collections of resources.
*   **Error Handling:** Return meaningful error messages and appropriate HTTP status codes (see [`Error_Handling_Guide.md`](../02_Architecture/Error_Handling_Guide.md) or the project's equivalent).

## 2. API Versioning

**Strategy:** URL Path Versioning
**Example:** `/api/v1/users`, `/api/v2/users`

New versions should be introduced for breaking changes. Non-breaking changes (e.g., adding new optional fields to a response) can typically be made to the current version.

## 3. Request and Response Formats

*   **Data Format:** Use JSON for request and response bodies.
*   **Headers:**
    *   `Content-Type: application/json` for requests with a JSON body.
    *   `Accept: application/json` for clients expecting a JSON response.
    *   `Authorization: Bearer <access_token>` for authenticated requests.
*   **Date/Time Format:** Use ISO 8601 format for dates and times (e.g., `YYYY-MM-DDTHH:mm:ss.sssZ`).

## 4. Standard HTTP Methods

*   **`GET`**: Retrieve a resource or a collection of resources. (Safe, Idempotent)
*   **`POST`**: Create a new resource. (Not Idempotent)
*   **`PUT`**: Update an existing resource completely. (Idempotent)
*   **`PATCH`**: Partially update an existing resource. (Not necessarily Idempotent, but often implemented as such)
*   **`DELETE`**: Delete a resource. (Idempotent)

## 5. Common HTTP Status Codes

*   **2xx Success:**
    *   `200 OK`: Standard response for successful GET, PUT, PATCH.
    *   `201 Created`: Resource successfully created (typically for POST). Response should include a `Location` header pointing to the new resource.
    *   `202 Accepted`: Request accepted for processing, but processing not complete (e.g., for asynchronous tasks).
    *   `204 No Content`: Request successful, but no data to return (e.g., for DELETE, or PUT/PATCH if no content is returned).
*   **3xx Redirection:**
    *   `301 Moved Permanently`
    *   `302 Found`
*   **4xx Client Errors:**
    *   `400 Bad Request`: Generic client error (e.g., malformed request syntax, invalid request message framing). Often used for validation errors.
    *   `401 Unauthorized`: Authentication is required and has failed or has not yet been provided.
    *   `403 Forbidden`: Authenticated user does not have permission to access the resource.
    *   `404 Not Found`: The requested resource could not be found.
    *   `405 Method Not Allowed`: The HTTP method used is not supported for this resource.
    *   `409 Conflict`: Request conflicts with the current state of the resource (e.g., trying to create a duplicate resource with a unique constraint).
    *   `422 Unprocessable Entity`: The server understands the content type of the request entity, and the syntax of the request entity is correct, but it was unable to process the contained instructions (often used for semantic validation errors not covered by 400).
*   **5xx Server Errors:**
    *   `500 Internal Server Error`: A generic error message, given when an unexpected condition was encountered.
    *   `502 Bad Gateway`: Server, while acting as a gateway or proxy, received an invalid response from an inbound server.
    *   `503 Service Unavailable`: The server is currently unable to handle the request due to temporary overloading or maintenance.

## 6. API Endpoint Documentation Template

Use the following template to document each resource and its endpoints.

---

### Resource: [Resource Name - e.g., User, Product, Order]

**Base Path:** `/api/v[version]/[resource-plural-name]` (e.g., `/api/v1/users`)

Description: A brief description of what this resource represents and its role in the system.

Module (for Permissions): `[e.g., User Management, Product Catalog, Order Processing]` (Specify the logical module this resource belongs to for permission checking)

Associated Model (Django): `[app_name.models.ModelName]`
ViewSet: `[app_name.views.ViewSetOrViewName]`
Serializer: `[app_name.serializers.SerializerName]`
Permissions: `[General permissions for the resource, e.g., IsAuthenticated. Endpoint specific permissions are detailed below.]`

#### Endpoints:

**1. List [Resource Plural Name]**

*   **Method:** `GET`
*   **Endpoint:** `/api/v[version]/[resource-plural-name]/`
*   **Description:** Retrieves a list of [resource plural name]. Supports filtering, sorting, and pagination.
*   **Permissions:** `IsAuthenticated`, `[CustomPermission (View[ResourceNamePlural])]` (e.g., `ViewUsers`)
*   **Query Parameters:**
    *   `page` (integer, optional): Page number for pagination. Default: `1`.
    *   `page_size` (integer, optional): Number of items per page. Default: `[default_page_size, e.g., 25]`.
    *   `search` (string, optional): Search term to filter results by [relevant_fields_for_search].
    *   `ordering` (string, optional): Field to sort by (e.g., `name`, `-created_at`). Prefix with `-` for descending order.
    *   `[filter_field_1]` ([type], optional): Filter by [description_of_filter_field_1] (e.g., `status (string, optional): Filter by UserStatus enum value.`).
    *   `[filter_field_2]` ([type], optional): Filter by [description_of_filter_field_2].
*   **Request Body:** None
*   **Success Response:**
    *   **Code:** `200 OK`
    *   **Body:**
        ```json
        {
          "count": 120, // Total number of items matching filter criteria
          "next": "/api/v1/[resource-plural-name]/?page=2&page_size=[default_page_size]", // URL for next page, or null
          "previous": null, // URL for previous page, or null
          "results": [
            {
              "id": "[uuid/integer]",
              "[field1]": "[value1]",
              "[field2]": "[value2]",
              // ... other fields as defined in the serializer
              "created_at": "YYYY-MM-DDTHH:mm:ss.sssZ",
              "updated_at": "YYYY-MM-DDTHH:mm:ss.sssZ"
            }
            // ... more resource objects
          ]
        }
        ```
*   **Error Responses:**
    *   `401 Unauthorized`: If authentication is missing or invalid.
    *   `403 Forbidden`: If user lacks permission to view the resource list.

**2. Create [Resource Singular Name]**

*   **Method:** `POST`
*   **Endpoint:** `/api/v[version]/[resource-plural-name]/`
*   **Description:** Creates a new [resource singular name].
*   **Permissions:** `IsAuthenticated`, `[CustomPermission (Create[ResourceSingularName])]` (e.g., `CreateUser`)
*   **Request Body:** `application/json`
    ```json
    {
      "[field1_required]": "[value1]",
      "[field2_optional]": "[value2]",
      // ... other creatable fields
    }
    ```
    *(Refer to the associated Serializer for detailed field validation rules, choices, and constraints.)*
    *   **Field Descriptions:**
        *   `field1_required` (`string`, required): Description of this field. Example: `username`.
        *   `field2_optional` (`integer`, optional): Description of this field. Example: `age`. Default: `null`.
*   **Success Response:**
    *   **Code:** `201 Created`
    *   **Headers:** `Location: /api/v[version]/[resource-plural-name]/[new_resource_id]/`
    *   **Body:** (The newly created resource object)
        ```json
        {
          "id": "[new_resource_id]",
          "[field1_required]": "[value1]",
          "[field2_optional]": "[value2]",
          // ... all fields of the created resource as per serializer
          "created_at": "YYYY-MM-DDTHH:mm:ss.sssZ",
          "updated_at": "YYYY-MM-DDTHH:mm:ss.sssZ"
        }
        ```
*   **Error Responses:**
    *   `400 Bad Request`: If validation fails. The response body should detail the errors.
        ```json
        // Example Validation Error
        {
          "detail": "Validation Failed.", // General error message
          "code": "validation_error",    // Optional application-specific error code
          "errors": { // Field-specific errors
            "field1_required": ["This field may not be blank."],
            "field2_optional": ["Ensure this value is greater than 18."]
          }
        }
        ```
    *   `401 Unauthorized`
    *   `403 Forbidden`: If user lacks permission to create the resource.
    *   `409 Conflict`: If creating the resource would conflict with an existing one (e.g., unique constraint violation like duplicate email).

**3. Retrieve [Resource Singular Name]**

*   **Method:** `GET`
*   **Endpoint:** `/api/v[version]/[resource-plural-name]/{id}/`
*   **Description:** Retrieves a specific [resource singular name] by its ID.
*   **Permissions:** `IsAuthenticated`, `[CustomPermission (View[ResourceSingularName])]` (e.g., `ViewUser`), or object-level permission (e.g., `IsOwnerOrAdmin`)
*   **Path Parameters:**
    *   `id` ([uuid/integer], required): The ID of the [resource singular name].
*   **Request Body:** None
*   **Success Response:**
    *   **Code:** `200 OK`
    *   **Body:** (The requested resource object)
        ```json
        {
          "id": "[resource_id]",
          "[field1]": "[value1]",
          "[field2]": "[value2]",
          // ... all fields of the resource as per serializer
          "created_at": "YYYY-MM-DDTHH:mm:ss.sssZ",
          "updated_at": "YYYY-MM-DDTHH:mm:ss.sssZ"
        }
        ```
*   **Error Responses:**
    *   `401 Unauthorized`
    *   `403 Forbidden`: If user lacks permission to view this specific resource.
    *   `404 Not Found`: If the resource with the given ID does not exist.

**4. Update [Resource Singular Name] (Full Update)**

*   **Method:** `PUT`
*   **Endpoint:** `/api/v[version]/[resource-plural-name]/{id}/`
*   **Description:** Fully updates an existing [resource singular name]. All required fields for the resource must be provided in the request body.
*   **Permissions:** `IsAuthenticated`, `[CustomPermission (Edit[ResourceSingularName])]` (e.g., `EditUser`), or object-level permission
*   **Path Parameters:**
    *   `id` ([uuid/integer], required): The ID of the [resource singular name] to update.
*   **Request Body:** `application/json` (All mutable fields of the resource, ensuring all required fields are present)
    ```json
    {
      "[field1_required]": "[new_value1]",
      "[field2_mutable]": "[new_value2]",
      // ... other fields to update
    }
    ```
    *(Refer to the associated Serializer for detailed field validation rules, choices, and constraints.)*
*   **Success Response:**
    *   **Code:** `200 OK`
    *   **Body:** (The updated resource object, same format as GET single)
*   **Error Responses:**
    *   `400 Bad Request` (Validation errors, format as above)
    *   `401 Unauthorized`
    *   `403 Forbidden`
    *   `404 Not Found`

**5. Partially Update [Resource Singular Name]**

*   **Method:** `PATCH`
*   **Endpoint:** `/api/v[version]/[resource-plural-name]/{id}/`
*   **Description:** Partially updates an existing [resource singular name]. Only include fields to be updated in the request body.
*   **Permissions:** `IsAuthenticated`, `[CustomPermission (Edit[ResourceSingularName])]` (e.g., `EditUser`), or object-level permission
*   **Path Parameters:**
    *   `id` ([uuid/integer], required): The ID of the [resource singular name] to update.
*   **Request Body:** `application/json` (Only fields to be updated)
    ```json
    {
      "[field_to_update1]": "[new_value1]",
      "[field_to_update2]": "[new_value2]"
    }
    ```
    *(Refer to the associated Serializer for detailed field validation rules, choices, and constraints.)*
*   **Success Response:**
    *   **Code:** `200 OK`
    *   **Body:** (The updated resource object, same format as GET single)
*   **Error Responses:**
    *   `400 Bad Request` (Validation errors, format as above)
    *   `401 Unauthorized`
    *   `403 Forbidden`
    *   `404 Not Found`

**6. Delete [Resource Singular Name]**

*   **Method:** `DELETE`
*   **Endpoint:** `/api/v[version]/[resource-plural-name]/{id}/`
*   **Description:** Deletes a specific [resource singular name].
*   **Permissions:** `IsAuthenticated`, `[CustomPermission (Delete[ResourceSingularName])]` (e.g., `DeleteUser`), or object-level permission
*   **Path Parameters:**
    *   `id` ([uuid/integer], required): The ID of the [resource singular name] to delete.
*   **Request Body:** None
*   **Success Response:**
    *   **Code:** `204 No Content`
    *   **Body:** None
*   **Error Responses:**
    *   `401 Unauthorized`
    *   `403 Forbidden`
    *   `404 Not Found`

**7. Custom Action: [Action Name]** (If applicable, e.g., for DRF ViewSet `@action` decorator)

*   **Method:** `[POST/GET/PUT/etc.]` (Choose the most appropriate HTTP method)
*   **Endpoint:** `/api/v[version]/[resource-plural-name]/{id}/[action_name]/` (or `/api/v[version]/[resource-plural-name]/[action_name]/` if not instance-specific)
*   **Description:** [Clear description of what the custom action does, its purpose, and any side effects].
*   **Permissions:** `IsAuthenticated`, `[CustomPermission (Perform[ActionNameResourceSingularName])]` (e.g., `PerformResetPasswordUser`)
*   **Path Parameters (if instance-specific):**
    *   `id` ([uuid/integer], required): The ID of the parent [resource singular name].
*   **Query Parameters (if any):**
    *   `[param_name]` ([type], optional/required): [Description].
*   **Request Body (if any):** `application/json`
    ```json
    {
      "[param1]": "[value1]",
      "[param2]": "[value2]"
    }
    ```
    *(Clearly document the expected request body structure and field validations.)*
*   **Success Response:**
    *   **Code:** `[e.g., 200 OK, 202 Accepted]`
    *   **Body:** [Description of response body. Clearly document the structure.]
        ```json
        {
          "status": "action_completed_successfully", // Or other relevant status message
          "details": {
            // ... action-specific details ...
          }
        }
        ```
*   **Error Responses:** [List relevant error responses, including `400`, `401`, `403`, `404`, and any action-specific errors.]

---

*(Repeat the above "Resource" section for each resource in your API)*

## 7. API Documentation Tools

Consider using tools like **Swagger/OpenAPI** to generate interactive API documentation from your code (e.g., using `drf-spectacular` or `drf-yasg` for Django Rest Framework). This document can serve as the source of truth or a supplement to auto-generated documentation, especially for design discussions and high-level overviews.

---
*This template should be filled out for each new API or significant modification. Keep it updated as the API evolves.*