# WorkFrame API Documentation

## Overview

WorkFrame is a Flask-based framework designed for rapidly building business applications. This documentation covers all public classes, methods, and functions available in the WorkFrame framework.

## Installation

```bash
pip install workframe
```

## Quick Start

```python
from workframe import WorkFrame, crud

app = WorkFrame(__name__)
contacts = crud('contacts', ['name', 'email', 'phone'])
app.register_module('/contacts', contacts, menu_title='Contacts')
app.run(debug=True)
```

---

## Core Classes

### WorkFrame

The main application class that wraps Flask and provides business application functionality.

#### Constructor

```python
WorkFrame(import_name, app_name=None, app_description=None, 
          secret_key=None, database_url=None, **kwargs)
```

**Parameters:**
- `import_name` (str): The name of the application package (usually `__name__`)
- `app_name` (str, optional): Display name for the application. Defaults to import_name
- `app_description` (str, optional): Description shown in the UI. Defaults to "Business Application"
- `secret_key` (str, optional): Flask secret key. Auto-generated if not provided
- `database_url` (str, optional): Database connection URL. Defaults to SQLite
- `**kwargs`: Additional Flask configuration options

**Example:**
```python
app = WorkFrame(__name__, 
                app_name="My Business App",
                app_description="Customer Management System",
                database_url="postgresql://user:pass@localhost/mydb")
```

#### Methods

##### `register_module(url_prefix, module, menu_title=None, admin_required=False)`

Register a module (blueprint) with the application.

**Parameters:**
- `url_prefix` (str): URL prefix for the module (e.g., '/contacts')
- `module` (Module): WorkFrame module to register
- `menu_title` (str, optional): Title displayed in navigation menu
- `admin_required` (bool): Whether admin privileges are required. Defaults to False

**Returns:** None

**Example:**
```python
contacts = crud('contacts', ['name', 'email'])
app.register_module('/contacts', contacts, menu_title='Contacts')
```

##### `run(host='127.0.0.1', port=5000, debug=False, **options)`

Run the application server.

**Parameters:**
- `host` (str): Hostname to listen on. Defaults to '127.0.0.1'
- `port` (int): Port to listen on. Defaults to 5000
- `debug` (bool): Enable debug mode. Defaults to False
- `**options`: Additional Flask run options

**Returns:** None

---

## CRUD System

### crud() Function

High-level convenience function for creating CRUD modules.

```python
crud(table_name, fields, many_to_one=None, many_to_many=None, 
     page_size=20, search_fields=None)
```

**Parameters:**
- `table_name` (str): Name of the database table
- `fields` (list): List of field definitions (strings or Field objects)
- `many_to_one` (str, optional): Name of master table for linked table view
- `many_to_many` (str, optional): Name of related table for many-to-many relationships
- `page_size` (int): Number of records per page. Defaults to 20
- `search_fields` (list, optional): Fields to include in search. Defaults to text fields

**Returns:** Module object ready for registration

**Examples:**

**Simple CRUD:**
```python
contacts = crud('contacts', ['name', 'email', 'phone'])
```

**Advanced CRUD with field customization:**
```python
from workframe import crud, Field

contacts = crud('contacts', [
    'name',
    'email', 
    Field('company', lookup='companies', display='name'),
    Field('status', enum=['Active', 'Inactive']),
    Field('notes', type='textarea', optional=True)
])
```

**Linked Tables (Many-to-One):**
```python
contacts = crud('contacts', ['name', 'email', 'company_id'], 
                many_to_one='companies')
```

**Many-to-Many Relationships:**
```python
user_roles = crud('users', ['username', 'email'], 
                  many_to_many='roles')
```

---

### Field Class

Represents a database field with validation and display options.

#### Constructor

```python
Field(name, type='text', required=True, readonly=False, hidden=False,
      hidden_in_form=False, hidden_in_list=False, optional=False,
      placeholder=None, default=None, validation=None, enum=None,
      lookup=None, display=None, value=None, allow_new=False,
      rows=None, format=None)
```

**Parameters:**
- `name` (str): Field name in database
- `type` (str): Field type ('text', 'email', 'phone', 'date', 'datetime', 'currency', 'textarea', 'boolean')
- `required` (bool): Whether field is required. Defaults to True
- `readonly` (bool): Whether field is read-only. Defaults to False
- `hidden` (bool): Whether field is hidden everywhere. Defaults to False
- `hidden_in_form` (bool): Whether field is hidden in forms only. Defaults to False
- `hidden_in_list` (bool): Whether field is hidden in list views only. Defaults to False
- `optional` (bool): Alias for required=False. Defaults to False
- `placeholder` (str, optional): Placeholder text for form inputs
- `default` (any, optional): Default value (can be callable)
- `validation` (callable, optional): Custom validation function
- `enum` (list, optional): List of allowed values for dropdown
- `lookup` (str, optional): Foreign key table name
- `display` (str, optional): Display field for lookups. Defaults to 'name'
- `value` (str, optional): Value field for lookups. Defaults to 'id'
- `allow_new` (bool): Allow creating new lookup records. Defaults to False
- `rows` (int, optional): Number of rows for textarea fields
- `format` (str, optional): Display format string

**Field Type Auto-Detection:**
- Fields named 'email' automatically get email validation
- Fields named 'phone' get `type="tel"` input
- Fields ending with '_date' get date picker
- Fields ending with '_at' get datetime picker
- Fields with 'price', 'cost', 'amount', 'salary' get currency formatting
- Fields starting with 'is_' or 'has_' become boolean fields

**Examples:**

```python
# Simple text field
Field('name')

# Email field with validation
Field('email', type='email', placeholder='user@example.com')

# Optional textarea
Field('notes', type='textarea', optional=True, rows=5)

# Dropdown with predefined options
Field('status', enum=['Active', 'Inactive', 'Pending'])

# Foreign key lookup
Field('company', lookup='companies', display='name', allow_new=True)

# Currency field with formatting
Field('salary', type='currency', format='${:,.2f}')

# Read-only field with default value
Field('created_at', type='datetime', readonly=True, 
      default=lambda: datetime.now())
```

---

## Module Classes

### Module

Base class for creating custom modules.

#### Constructor

```python
Module(name, url_prefix='')
```

**Parameters:**
- `name` (str): Module name
- `url_prefix` (str): URL prefix for routes

#### Methods

##### `add_route(rule, endpoint, view_func, methods=['GET'])`

Add a route to the module.

**Parameters:**
- `rule` (str): URL rule
- `endpoint` (str): Endpoint name
- `view_func` (callable): View function
- `methods` (list): HTTP methods. Defaults to ['GET']

### LinkedTableModule

Module for many-to-one relationships showing master and detail tables.

**Automatically created by:** `crud(table_name, fields, many_to_one='master_table')`

**Features:**
- Shows master table and detail table on same page
- Clicking master row filters detail table
- Contextual "Add Detail" button pre-fills foreign key
- Mobile-responsive design

### ManyToManyModule

Module for many-to-many relationships with assignment management.

**Automatically created by:** `crud(table_name, fields, many_to_many='related_table')`

**Features:**
- Auto-creates junction table
- Assignment management interface
- Bulk assignment operations
- Prevents duplicate assignments

---

## Database Models

### User

Built-in user model for authentication.

#### Fields

- `id` (int): Primary key
- `username` (str): Unique username
- `email` (str): User email address
- `password_hash` (str): Hashed password
- `is_admin` (bool): Admin privileges flag
- `is_active` (bool): Account active status
- `created_at` (datetime): Account creation timestamp

#### Relationships

- `groups` (many-to-many): User groups via UserGroup junction table

### Group

Built-in group model for role-based access.

#### Fields

- `id` (int): Primary key
- `name` (str): Unique group name
- `description` (str): Group description
- `created_at` (datetime): Group creation timestamp

#### Relationships

- `users` (many-to-many): Group members via UserGroup junction table

#### Default Groups

- **Administrators**: Full system access
- **Users**: Standard user access

---

## Authentication & Authorization

### Login Requirements

All CRUD operations require authentication. Use the built-in decorators:

```python
from workframe.views.auth import login_required, admin_required

@login_required
def protected_view():
    pass

@admin_required  
def admin_only_view():
    pass
```

### Default Admin User

On first startup, WorkFrame creates:
- Username: `admin`
- Password: `admin`
- Assigned to: `Administrators` group

**Security Note:** Change the default admin password in production!

---

## Database Configuration

### SQLite (Default)

```python
app = WorkFrame(__name__)  # Uses SQLite by default
```

### PostgreSQL

```python
app = WorkFrame(__name__, 
                database_url="postgresql://user:password@localhost/dbname")
```

### Environment Variables

```bash
export DATABASE_URL="postgresql://user:password@localhost/dbname"
export SECRET_KEY="your-secret-key"
```

```python
import os
app = WorkFrame(__name__, 
                database_url=os.getenv('DATABASE_URL'),
                secret_key=os.getenv('SECRET_KEY'))
```

---

## Templates & Customization

### Template Structure

WorkFrame uses Jinja2 templates with Bootstrap 5:

```
templates/
├── base.html              # Base template
├── dashboard.html         # Home page
├── auth/
│   ├── login.html        # Login page
│   └── register.html     # Registration page
└── crud/
    ├── list.html         # List view
    ├── detail.html       # Detail view
    ├── form.html         # Form view
    ├── linked.html       # Linked tables view
    └── manytomany.html   # Many-to-many view
```

### Custom Templates

Override templates by creating files with the same names in your application's `templates/` directory.

### CSS Customization

WorkFrame includes Bootstrap 5 dark theme by default. Customize by overriding:

```html
<!-- In your base template -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/custom.css') }}">
```

---

## Error Handling

### Built-in Error Pages

WorkFrame provides Bootstrap-styled error pages:

- **404 Not Found**: Styled with navigation and helpful links
- **500 Server Error**: User-friendly error message with admin contact info

### Custom Error Handling

```python
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404
```

---

## Security Features

### CSRF Protection

All forms automatically include CSRF tokens.

### Password Security

- Passwords hashed using Werkzeug's security utilities
- Salted hashes prevent rainbow table attacks

### SQL Injection Prevention

- All database queries use SQLAlchemy ORM
- Parameterized queries prevent injection attacks

### XSS Prevention

- All user input escaped in templates
- Content Security Policy headers recommended

---

## Performance Considerations

### Database Optimization

- Lazy loading for relationships
- Pagination for large datasets
- Foreign key indexes automatically created

### Frontend Optimization

- Minimal JavaScript dependencies
- Mobile-first responsive design
- Efficient template rendering

---

## Development & Testing

### Development Mode

```python
app.run(debug=True)  # Enable debug mode
```

### Database Migrations

```python
# Create all tables
app.create_all()

# Drop all tables (development only)
app.drop_all()
```

### Logging

WorkFrame includes colored logging for better development experience:

```python
import logging
logging.getLogger('workframe').setLevel(logging.DEBUG)
```

---

## Extension Points

### Custom Views

```python
from workframe.views.base import BaseView

class CustomView(BaseView):
    def get(self):
        return self.render('custom_template.html')

module.add_route('/custom', 'custom', CustomView.as_view('custom'))
```

### Custom Field Types

```python
class CustomField(Field):
    def __init__(self, name, **kwargs):
        super().__init__(name, type='custom', **kwargs)
    
    def render_input(self):
        return f'<input type="text" name="{self.name}" class="custom-field">'
```

### Custom Validation

```python
def validate_email_domain(value):
    if not value.endswith('@company.com'):
        raise ValueError('Must use company email')

Field('email', validation=validate_email_domain)
```

---

## Best Practices

### Database Design

1. Use meaningful field names
2. Include audit fields (created_at, updated_at)
3. Use foreign keys for relationships
4. Add indexes for frequently searched fields

### Security

1. Change default admin credentials
2. Use environment variables for secrets
3. Enable HTTPS in production
4. Regular security updates

### Performance

1. Use pagination for large datasets
2. Optimize database queries
3. Cache static content
4. Monitor application performance

### Code Organization

1. Group related functionality in modules
2. Use descriptive names for tables and fields
3. Document custom validation rules
4. Keep business logic separate from presentation

---

## Troubleshooting

### Common Issues

**Import Errors:**
```bash
pip install -r requirements.txt
```

**Database Connection:**
```python
# Check database URL format
app = WorkFrame(__name__, database_url="sqlite:///app.db")
```

**Template Not Found:**
```
Ensure templates are in the correct directory structure
```

**CSS Not Loading:**
```
Check static file configuration and URL routing
```

### Debug Mode

Enable debug mode for detailed error messages:

```python
app.run(debug=True)
```

### Logging

Increase logging verbosity:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## Version History

### 0.1.0 (Current)

- Initial release
- Core CRUD functionality
- Authentication system
- Many-to-one and many-to-many relationships
- Mobile-first responsive design
- PostgreSQL and SQLite support

---

## Support

- **Documentation**: [GitHub Repository](https://github.com/massyn/workframe)
- **Issues**: [Bug Tracker](https://github.com/massyn/workframe/issues)
- **Source Code**: [GitHub](https://github.com/massyn/workframe)

---

## License

WorkFrame is released under the MIT License. See LICENSE file for details.