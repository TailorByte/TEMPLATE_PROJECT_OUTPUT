# Database Design (DBML) Template

This document uses Database Markup Language (DBML) to define the database schema for this project. DBML provides a simple, human-readable way to describe database structures.

**DBML Resources:**
*   **Official Site:** [dbml.org](https://dbml.org/)
*   **Syntax Cheatsheet:** [DBML Cheatsheet](https://dbml.org/docs/cheatsheet)
*   **Online Editor/Visualizer:** [dbdiagram.io](https://dbdiagram.io/)

## 1. Versioning and Schema Management

### 1.1 Versioning and Changelog (DBML Document)

It's good practice to version your DBML document itself and maintain a brief changelog at the top, especially for significant schema design iterations.

```dbml
// MyProject DBML - v1.2
// Changelog:
// - (v1.2) Added OrderItems table and refined Product pricing.
// - (v1.1) Updated Users table for Django compatibility.
// - (v1.0) Initial version with Users, Products, Orders.

// --- Project Definition (Optional) ---
Project "[Your Project Name]" {
  database_type: 'PostgreSQL' // Or MySQL, SQLServer, etc.
  Note: 'High-level overview of the project database.'
}
```

### 1.2 General Conventions

*   **Table Names:** Plural, PascalCase (e.g., `Users`, `Products`, `OrderItems`). This often maps well to Django model names.
*   **Column Names:** snake_case (e.g., `user_id`, `first_name`, `created_at`, `product_sku`).
*   **Primary Keys (PKs):**
    *   Name: `id` (common for Django models) or `[table_singular_name]_id` (e.g., `user_id`, `product_id`).
    *   Type: `integer [pk, increment]` or `bigint [pk, increment]` for auto-incrementing integers. Use `uuid [pk, default: \`uuid_generate_v4()\`, not null]` for UUIDs (ensure your database supports UUID generation or handle it at the application layer).
*   **Foreign Keys (FKs):**
    *   Name: `[referenced_table_singular_name]_id` (e.g., `user_id` in `Orders` table referencing `Users.id`).
    *   Define relationships explicitly using `ref: > ReferencedTable.referenced_column_name`.
*   **Audit Columns (Timestamps):**
    *   Include `created_at timestamp [default: \`now()\`, not null]`
    *   Include `updated_at timestamp [default: \`now()\`, not null]` (Consider database triggers or application-level logic to automatically update this on modification).
*   **Enums:** Define enums separately using `Enum EnumName { VALUE1 VALUE2 }` and reference them in column definitions (e.g., `status OrderStatus`).
*   **Indexes:** Explicitly define indexes for frequently queried columns, foreign keys, or combinations of columns to optimize query performance. Use `Indexes { (column1) (column2, column3) [unique] }`.
*   **Notes/Comments:**
    *   Use `Note { 'Table-level detailed description or rationale.' }` for tables.
    *   Use inline comments for columns: `column_name varchar [note: 'Specific details about this column.']`.
    *   Use `// Single line comment` for general DBML comments.

## 2. Project Definition (Optional)

This section is already covered in the versioning example above but can be standalone if preferred.

```dbml
Project "[Your Project Name]" {
  database_type: 'PostgreSQL' // Or MySQL, SQLServer, etc.
  Note: 'High-level overview of the project database.'
}
```

## 3. Enum Definitions

Define all enumerations used in your table definitions here. This promotes consistency and reusability. Consider enums for statuses, types, categories, etc.

```dbml
// --- Enums ---

Enum UserStatus {
  ACTIVE
  INACTIVE
  PENDING_VERIFICATION
  SUSPENDED
  ARCHIVED
}

Enum OrderStatus {
  PENDING_PAYMENT
  PROCESSING
  SHIPPED
  DELIVERED
  CANCELLED
  RETURNED
  COMPLETED
}

Enum PaymentMethod {
  CREDIT_CARD
  PAYPAL
  BANK_TRANSFER
  ON_DELIVERY
}

// Add more domain-specific enums as needed for your project.
// Examples inspired by complex systems:
// Enum TaskPriority { HIGH MEDIUM LOW }
// Enum AccessLevel { ADMIN EDITOR CONTRIBUTOR VIEWER GUEST }
// Enum NotificationType { SYSTEM_ALERT USER_MESSAGE PROMOTION }
// Enum ProductCategory { ELECTRONICS BOOKS CLOTHING HOME_GOODS }
```

## 4. Table Definitions

Define each table with its columns, types, constraints, and relationships.

```dbml
// --- Core Tables ---

Table Users { // Example reflecting a Django-like User model
  id integer [pk, increment] // Django's default User model uses 'id'
  username varchar(150) [unique, not null, note: 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.']
  password varchar(128) [not null, note: 'Stores hashed password (e.g., PBKDF2). Never store plain text.']
  email varchar(254) [unique, not null, note: 'User_s email address, used for login and communication.']
  first_name varchar(150) [null]
  last_name varchar(150) [null]
  is_active boolean [default: true, not null, note: 'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.']
  is_staff boolean [default: false, not null, note: 'Designates whether the user can log into this admin site.']
  is_superuser boolean [default: false, not null, note: 'Designates that this user has all permissions without explicitly assigning them.']
  status UserStatus [default: 'PENDING_VERIFICATION', note: 'Custom application-specific status.']
  last_login timestamp [null, note: 'Timestamp of the user_s last login.']
  date_joined timestamp [default: `now()`, not null, note: 'Timestamp when the user account was created. Equivalent to created_at.']
  // created_at timestamp [default: `now()`, not null] // Redundant if date_joined is used and serves the same purpose.
  updated_at timestamp [default: `now()`, not null, note: 'Timestamp of the last update to the user record.']

  Note: 'Stores user account information, including credentials and profile data. Designed to be compatible with Django_s default User model structure.'
}

Table Roles {
  id int [pk, increment]
  name varchar(50) [unique, not null, note: 'e.g., ADMIN, EDITOR, VIEWER, CUSTOMER_SUPPORT']
  description text [null]
  created_at timestamp [default: `now()`, not null]
  updated_at timestamp [default: `now()`, not null]

  Note: 'Defines user roles within the system for role-based access control (RBAC).'
}

Table UserRoles { // Junction table for Many-to-Many between Users and Roles
  id bigint [pk, increment]
  user_id integer [ref: > Users.id, not null]
  role_id int [ref: > Roles.id, not null]
  created_at timestamp [default: `now()`, not null]
  // updated_at is typically not needed for simple junction records unless the association itself has properties that change.

  Indexes {
    (user_id, role_id) [unique, name: 'idx_user_roles_user_role_unique']
  }
  Note: 'Assigns roles to users. A user can have multiple roles, and a role can be assigned to multiple users.'
}

// Example: Products Table
Table Products {
  id uuid [pk, default: `uuid_generate_v4()`, not null] // Example using UUID
  name varchar(255) [not null]
  description text [null]
  sku varchar(100) [unique, not null, note: 'Stock Keeping Unit, unique product identifier.']
  price decimal(10, 2) [not null, note: 'Price with 2 decimal places.']
  // category ProductCategory [null] // Example using an Enum defined above
  stock_quantity int [default: 0, not null]
  is_available boolean [default: true, not null]
  created_at timestamp [default: `now()`, not null]
  updated_at timestamp [default: `now()`, not null]
  // created_by_user_id integer [ref: > Users.id, null] // Optional: Tracks who created the product

  Indexes {
    (sku)
    (name)
    // (category)
  }
  Note: 'Stores product information, including pricing, stock, and descriptive details.'
}

// Example: Orders Table
Table Orders {
  id bigint [pk, increment]
  user_id integer [ref: > Users.id, not null, note: 'Customer who placed the order.']
  order_date timestamp [default: `now()`, not null]
  status OrderStatus [not null, default: 'PENDING_PAYMENT']
  total_amount decimal(12, 2) [not null]
  shipping_address_line1 varchar [null]
  shipping_address_line2 varchar [null]
  shipping_city varchar [null]
  shipping_postal_code varchar [null]
  shipping_country varchar [null]
  payment_method PaymentMethod [null]
  payment_transaction_id varchar [null, note: 'Reference to payment gateway transaction.']
  created_at timestamp [default: `now()`, not null]
  updated_at timestamp [default: `now()`, not null]

  Note: 'Stores customer order information, including shipping and payment details.'
}

// Example: OrderItems Table (Junction table for Orders and Products)
Table OrderItems {
  id bigint [pk, increment]
  order_id bigint [ref: > Orders.id, not null]
  product_id uuid [ref: > Products.id, not null]
  quantity int [not null, note: 'Quantity of this product in the order. Must be > 0.']
  price_at_purchase decimal(10, 2) [not null, note: 'Price of the product at the time of order. Ensures historical accuracy if product price changes.']
  created_at timestamp [default: `now()`, not null]
  // updated_at is typically not needed here.

  Indexes {
    (order_id, product_id) [unique, name: 'idx_orderitems_order_product_unique'] // A product should appear once per order; quantity handles multiples.
  }
  Note: 'Links products to orders, specifying quantity and price at the time of purchase.'
}

// Example: Attachments Table (Illustrating Polymorphic-like Ownership)
Table Attachments {
  id bigint [pk, increment]
  file_name varchar(255) [not null]
  file_path varchar [not null, unique, note: 'Path to the file in storage (e.g., S3 URL or local path).']
  mime_type varchar(100) [null]
  file_size_bytes bigint [null]
  // Polymorphic "owner" fields: Only one of these should be non-null for a given record.
  task_id bigint [ref: > Tasks.id, null, note: 'If attachment belongs to a Task.'] // Assuming a Tasks table exists
  comment_id bigint [ref: > Comments.id, null, note: 'If attachment belongs to a Comment.'] // Assuming a Comments table exists
  uploaded_by_user_id integer [ref: > Users.id, null]
  created_at timestamp [default: `now()`, not null]
  updated_at timestamp [default: `now()`, not null]

  Note: 'Stores uploaded files. An attachment can belong to different types of parent entities (e.g., a Task OR a Comment). Application logic must ensure only one owner FK is set.'
}

// --- Add more table definitions below as needed for your project ---

/*
// Example: Categories Table
Table Categories {
  id int [pk, increment]
  name varchar(100) [unique, not null]
  description text [null]
  parent_category_id int [ref: > Categories.id, null, note: 'For hierarchical categories. Self-referencing FK.']
  created_at timestamp [default: `now()`, not null]
  updated_at timestamp [default: `now()`, not null]
}

// Example: ProductCategories (Junction table for Products and Categories if many-to-many)
Table ProductCategories {
  id bigint [pk, increment]
  product_id uuid [ref: > Products.id, not null]
  category_id int [ref: > Categories.id, not null]
  // No created_at/updated_at needed unless the association itself has attributes.
  Indexes {
    (product_id, category_id) [unique]
  }
}
*/
```

## 5. Relationship Definitions (Implicit and Explicit)

DBML infers relationships from foreign key definitions (`ref: > ...`). Explicit relationship definitions are usually only needed for clarity on complex diagrams or if the FK syntax isn't used.

*   **One-to-Many:** `Users` to `Orders` (One user can have many orders). Defined by `user_id integer [ref: > Users.id]` in the `Orders` table.
*   **Many-to-Many:** `Orders` to `Products` (via `OrderItems` junction table).
    *   `OrderItems.order_id` references `Orders.id`.
    *   `OrderItems.product_id` references `Products.id`.
*   **One-to-One:** (Example) If a `UserProfiles` table had a `user_id` that was both a `pk` and a `fk` to `Users.id` and marked `unique`.
    ```dbml
    // Table UserProfiles {
    //   user_id integer [pk, ref: > Users.id] // This creates a 1-to-1 relationship
    //   bio text [null]
    //   profile_picture_url varchar [null]
    //   // ... other profile-specific fields
    //   created_at timestamp [default: `now()`, not null]
    //   updated_at timestamp [default: `now()`, not null]
    // }
    ```

Explicit relationship syntax (less common if FKs are well-defined):
```dbml
// Ref: Users.id < Orders.user_id // One-to-Many (User has many Orders)
// Ref: Products.id - OrderItems.product_id // Many-to-Many (Product is in many OrderItems)
// Ref: Orders.id - OrderItems.order_id     // Many-to-Many (Order has many OrderItems)
```

## 6. Notes on Django Integration

*   **Source of Truth:** While this DBML serves as a crucial design and documentation tool, Django's ORM (`models.py`) is the ultimate source of truth for generating database migrations. Keep this DBML file in sync with your Django models.
*   **Django Model Field Mapping:**
    *   `AutoField` (default PK for models without explicit PK) -> `integer [pk, increment]`
    *   `BigAutoField` (default PK if `DEFAULT_AUTO_FIELD` is set) -> `bigint [pk, increment]`
    *   `CharField` -> `varchar(max_length)`
    *   `TextField` -> `text`
    *   `IntegerField` -> `int`
    *   `BooleanField` -> `boolean`
    *   `DateField` -> `date`
    *   `DateTimeField` -> `timestamp`
    *   `DecimalField` -> `decimal(max_digits, decimal_places)`
    *   `EmailField` -> `varchar(254)`
    *   `UUIDField` -> `uuid`
    *   `ForeignKey` -> Defines the `ref: > ReferencedTable.referenced_column` in DBML.
    *   `ManyToManyField`: **Crucially, these imply a junction table.** You *must* explicitly define this junction table in your DBML for clarity and completeness (e.g., `UserRoles` for `User.roles = ManyToManyField(Role)`). Django might create an implicit one if you don't specify a `through` model, but it's best practice to define it in DBML.
    *   `OneToOneField` -> Similar to `ForeignKey` but with a `unique` constraint on the FK column, often also making it the PK of the related table (as in the `UserProfiles` example).
*   **Django `User` Model:** If you are using Django's built-in `django.contrib.auth.models.User` or a custom user model inheriting from `AbstractUser` or `AbstractBaseUser`, ensure your `Users` table definition in DBML accurately reflects its fields (e.g., `id`, `username`, `password`, `email`, `is_staff`, `is_superuser`, `date_joined`, etc.). The example `Users` table above is tailored for this.

---
*This DBML file should be kept in sync with the actual database schema and Django models as the project evolves.*
*Use dbdiagram.io or a similar tool to visualize this schema and check for syntax errors.*