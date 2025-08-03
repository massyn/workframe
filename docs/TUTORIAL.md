# WorkFrame Tutorial: Building Business Applications

## Table of Contents

1. [Getting Started](#getting-started)
2. [Your First Application](#your-first-application)
3. [Understanding Fields](#understanding-fields)
4. [Working with Relationships](#working-with-relationships)
5. [Authentication and Security](#authentication-and-security)
6. [Advanced Features](#advanced-features)
7. [Deployment](#deployment)

---

## Getting Started

### Installation

First, install WorkFrame using pip:

```bash
pip install workframe
```

### Prerequisites

- Python 3.9 or higher
- Basic understanding of web applications
- Familiarity with databases (helpful but not required)

### Your Development Environment

Create a new directory for your project:

```bash
mkdir my-business-app
cd my-business-app
```

---

## Your First Application

Let's build a simple contact management system to understand WorkFrame basics.

### Step 1: Create the Basic App

Create a file called `app.py`:

```python
from workframe import WorkFrame, crud

# Create the WorkFrame application
app = WorkFrame(__name__, 
                app_name="Contact Manager",
                app_description="Simple contact management system")

# Create a contacts module using the crud() convenience function
contacts = crud('contacts', ['name', 'email', 'phone', 'company'])

# Register the module with the app
app.register_module('/contacts', contacts, menu_title='Contacts')

if __name__ == '__main__':
    app.run(debug=True)
```

### Step 2: Run Your Application

```bash
python app.py
```

Open your browser and go to `http://localhost:5000`

### Step 3: First Login

WorkFrame creates a default admin user:
- **Username**: `admin`
- **Password**: `admin`

**Important**: Change this password in production!

### Step 4: Explore Your App

After logging in, you'll see:
- A navigation menu with "Contacts"
- An empty contacts list with an "Add Contact" button
- Clean, professional Bootstrap styling

Try adding a few contacts to see the CRUD functionality in action.

---

## Understanding Fields

WorkFrame provides flexible field definitions. Let's enhance our contact manager with better field types.

### Basic Field Types

```python
from workframe import WorkFrame, crud, Field

app = WorkFrame(__name__)

# Enhanced contacts with different field types
contacts = crud('contacts', [
    'name',                                    # Simple text field
    Field('email', type='email'),              # Email field with validation
    Field('phone', type='phone'),              # Phone number field
    Field('website', type='url', optional=True), # Optional URL field
    Field('birthday', type='date', optional=True), # Date picker
    Field('notes', type='textarea', rows=4, optional=True), # Text area
])

app.register_module('/contacts', contacts, menu_title='Contacts')
app.run(debug=True)
```

### Field Options

Every field can be customized with these options:

```python
Field('field_name',
    type='text',           # Field type (text, email, phone, date, etc.)
    required=True,         # Is this field required?
    readonly=False,        # Can users edit this field?
    hidden=False,          # Hide field everywhere
    hidden_in_form=False,  # Hide only in forms
    hidden_in_list=False,  # Hide only in list views
    placeholder='Enter...', # Placeholder text
    default='value',       # Default value
)
```

### Auto-Detection Magic

WorkFrame automatically detects field types based on names:

```python
contacts = crud('contacts', [
    'name',           # Detected as text
    'email',          # Detected as email (with validation)
    'phone',          # Detected as phone (tel input type)
    'created_date',   # Detected as date (date picker)
    'updated_at',     # Detected as datetime (datetime picker)
    'is_active',      # Detected as boolean (checkbox)
    'salary',         # Detected as currency (formatted)
])
```

### Dropdown Fields (Enums)

Create dropdown selections:

```python
contacts = crud('contacts', [
    'name',
    'email',
    Field('status', enum=['Active', 'Inactive', 'Pending']),
    Field('priority', enum=['Low', 'Medium', 'High'], default='Medium'),
])
```

---

## Working with Relationships

Real business applications need relationships between data. WorkFrame makes this simple.

### Foreign Key Relationships (Many-to-One)

Let's add companies and link contacts to them:

```python
from workframe import WorkFrame, crud, Field

app = WorkFrame(__name__)

# First, create the companies module
companies = crud('companies', [
    'name',
    'industry',
    Field('employee_count', type='number'),
    Field('website', type='url', optional=True),
])

# Then create contacts with a company lookup
contacts = crud('contacts', [
    'name',
    'email',
    'phone',
    Field('company', lookup='companies', display='name'),  # Foreign key
    Field('position', optional=True),
])

# Register both modules
app.register_module('/companies', companies, menu_title='Companies')
app.register_module('/contacts', contacts, menu_title='Contacts')

app.run(debug=True)
```

### Linked Table View

For a better user experience, show companies and their contacts together:

```python
# Create a linked view showing companies and their contacts
contacts_by_company = crud('contacts', [
    'name', 'email', 'phone', 'position', 'company_id'
], many_to_one='companies')

app.register_module('/contacts-by-company', contacts_by_company, 
                   menu_title='Contacts by Company')
```

This creates a two-table view where:
- Top table shows all companies
- Bottom table shows contacts for the selected company
- Clicking a company filters the contacts automatically

### Many-to-Many Relationships

For complex relationships like users and roles:

```python
# Create roles
roles = crud('roles', ['name', 'description'])

# Create users with many-to-many role assignment
users = crud('users', [
    'username',
    'email', 
    Field('is_active', type='boolean', default=True),
], many_to_many='roles')

app.register_module('/roles', roles, menu_title='Roles')
app.register_module('/user-roles', users, menu_title='User Roles')
```

This automatically:
- Creates a junction table (`user_roles`)
- Provides an assignment management interface
- Handles adding/removing role assignments
- Prevents duplicate assignments

---

## Authentication and Security

### User Management

WorkFrame includes built-in user management accessible to admin users:

```python
app = WorkFrame(__name__)

# Admin modules are automatically available at:
# /admin/users - User management
# /admin/groups - Group management

# Regular business modules
contacts = crud('contacts', ['name', 'email', 'phone'])
app.register_module('/contacts', contacts, menu_title='Contacts')

app.run(debug=True)
```

### Access Control

Control who can access modules:

```python
# Admin-only module
admin_settings = crud('settings', ['key', 'value', 'description'])
app.register_module('/settings', admin_settings, 
                   menu_title='Settings', admin_required=True)

# Regular module (login required, but not admin)
contacts = crud('contacts', ['name', 'email'])
app.register_module('/contacts', contacts, menu_title='Contacts')
```

### Custom User Fields

Extend the user model for your business needs:

```python
# Note: This requires custom module development
# See Advanced Features section for details
```

### Password Security

WorkFrame automatically:
- Hashes passwords with salt
- Provides secure session management
- Includes CSRF protection on all forms

---

## Advanced Features

### Custom Validation

Add business rules to your fields:

```python
def validate_email_domain(email):
    """Ensure email is from company domain"""
    if not email.endswith('@company.com'):
        raise ValueError('Must use company email address')

def validate_phone_format(phone):
    """Ensure phone follows company format"""
    import re
    if not re.match(r'^\+1-\d{3}-\d{3}-\d{4}$', phone):
        raise ValueError('Phone must be in format: +1-XXX-XXX-XXXX')

contacts = crud('contacts', [
    'name',
    Field('email', validation=validate_email_domain),
    Field('phone', validation=validate_phone_format),
])
```

### Calculated Fields

Add fields that calculate their values:

```python
from datetime import datetime, timedelta

def default_expiry():
    """Set expiry to 1 year from now"""
    return datetime.now() + timedelta(days=365)

contracts = crud('contracts', [
    'client_name',
    Field('start_date', type='date'),
    Field('expiry_date', type='date', default=default_expiry),
    Field('created_at', type='datetime', readonly=True, 
          default=datetime.now, hidden_in_form=True),
])
```

### Search Configuration

Control which fields are searchable:

```python
contacts = crud('contacts', [
    'name', 'email', 'phone', 'company', 'notes'
], search_fields=['name', 'email', 'company'])  # Only search these fields
```

### Pagination

Control how many records appear per page:

```python
contacts = crud('contacts', [
    'name', 'email', 'phone'
], page_size=50)  # Show 50 records per page
```

### Custom CSS and Branding

Override the default styling:

Create `static/css/custom.css`:

```css
/* Custom company branding */
.navbar-brand {
    color: #your-brand-color !important;
}

/* Custom button colors */
.btn-primary {
    background-color: #your-primary-color;
    border-color: #your-primary-color;
}
```

Include in your templates by creating `templates/base.html`:

```html
{% extends "workframe/base.html" %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/custom.css') }}">
{% endblock %}
```

---

## Real-World Example: Small Business ERP

Let's build a comprehensive example that demonstrates multiple WorkFrame features:

```python
from workframe import WorkFrame, crud, Field
from datetime import datetime

app = WorkFrame(__name__, 
                app_name="Small Business ERP",
                app_description="Complete business management system")

# Core business entities
companies = crud('companies', [
    'name',
    'industry',
    Field('phone', type='phone'),
    Field('email', type='email'),
    Field('website', type='url', optional=True),
    Field('employee_count', type='number', optional=True),
    Field('annual_revenue', type='currency', optional=True),
])

contacts = crud('contacts', [
    'name',
    Field('email', type='email'),
    Field('phone', type='phone'),
    Field('company', lookup='companies', display='name'),
    Field('position', optional=True),
    Field('is_primary', type='boolean', default=False),
    Field('notes', type='textarea', optional=True, rows=3),
])

# Products and inventory
products = crud('products', [
    'name',
    'sku',
    Field('category', enum=['Hardware', 'Software', 'Service']),
    Field('price', type='currency'),
    Field('cost', type='currency'),
    Field('stock_quantity', type='number', default=0),
    Field('reorder_level', type='number', default=10),
    Field('is_active', type='boolean', default=True),
    Field('description', type='textarea', optional=True),
])

# Sales opportunities
opportunities = crud('opportunities', [
    'title',
    Field('company', lookup='companies', display='name'),
    Field('contact', lookup='contacts', display='name'),
    Field('value', type='currency'),
    Field('stage', enum=['Lead', 'Qualified', 'Proposal', 'Negotiation', 'Won', 'Lost']),
    Field('close_date', type='date'),
    Field('probability', type='number', default=50),
    Field('notes', type='textarea', optional=True),
])

# Invoices
invoices = crud('invoices', [
    Field('invoice_number', readonly=True),
    Field('company', lookup='companies', display='name'),
    Field('issue_date', type='date', default=datetime.now),
    Field('due_date', type='date'),
    Field('subtotal', type='currency'),
    Field('tax_amount', type='currency'),
    Field('total', type='currency'),
    Field('status', enum=['Draft', 'Sent', 'Paid', 'Overdue'], default='Draft'),
])

# Register all modules
app.register_module('/companies', companies, menu_title='Companies')
app.register_module('/contacts', contacts, menu_title='Contacts')
app.register_module('/products', products, menu_title='Products')
app.register_module('/opportunities', opportunities, menu_title='Sales')
app.register_module('/invoices', invoices, menu_title='Invoices')

# Linked views for better UX
contacts_by_company = crud('contacts', [
    'name', 'email', 'phone', 'position', 'company_id'
], many_to_one='companies')

app.register_module('/company-contacts', contacts_by_company, 
                   menu_title='Contacts by Company')

if __name__ == '__main__':
    app.run(debug=True)
```

This example demonstrates:
- Multiple related entities
- Different field types and validation
- Lookup relationships
- Enums for controlled values
- Currency and date handling
- Linked table views
- Professional business application structure

---

## Database Configuration

### SQLite (Development)

SQLite is the default and requires no configuration:

```python
app = WorkFrame(__name__)  # Uses SQLite automatically
```

### PostgreSQL (Production)

For production applications, use PostgreSQL:

```python
# Direct configuration
app = WorkFrame(__name__, 
                database_url="postgresql://user:password@localhost/myapp")

# Environment variable (recommended)
import os
app = WorkFrame(__name__, 
                database_url=os.getenv('DATABASE_URL'))
```

Set the environment variable:

```bash
export DATABASE_URL="postgresql://user:password@localhost/myapp"
```

### Database Initialization

WorkFrame automatically creates tables on first run. For production:

```python
# In your app startup
app = WorkFrame(__name__)
# ... define your modules ...

# Create tables (safe to call multiple times)
with app.app_context():
    app.db.create_all()
```

---

## Deployment

### Preparation

1. **Change default admin password**:
   - Log in as admin/admin
   - Go to user management
   - Change the password

2. **Set environment variables**:
   ```bash
   export SECRET_KEY="your-secret-key-here"
   export DATABASE_URL="postgresql://..."
   export FLASK_ENV="production"
   ```

3. **Create requirements.txt**:
   ```bash
   pip freeze > requirements.txt
   ```

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:password@db/myapp
      - SECRET_KEY=your-secret-key
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Deploy:

```bash
docker-compose up -d
```

### Cloud Deployment (Heroku)

1. **Install Heroku CLI**
2. **Create Heroku app**:
   ```bash
   heroku create my-business-app
   ```

3. **Add PostgreSQL**:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Set environment variables**:
   ```bash
   heroku config:set SECRET_KEY="your-secret-key"
   ```

5. **Deploy**:
   ```bash
   git push heroku main
   ```

### Production Considerations

1. **Use a production WSGI server**:
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```

2. **Enable HTTPS**
3. **Set up monitoring**
4. **Configure backups**
5. **Use environment variables for all secrets**

---

## Troubleshooting

### Common Issues

**Application won't start**:
- Check Python version (3.9+ required)
- Verify all dependencies installed: `pip install -r requirements.txt`

**Database connection errors**:
- Verify database URL format
- Check database server is running
- Ensure database user has proper permissions

**Templates not found**:
- Check template directory structure
- Verify template inheritance is correct

**CSS not loading**:
- Check static file configuration
- Verify CSS file paths
- Clear browser cache

### Debug Mode

Enable debug mode for detailed error messages:

```python
app.run(debug=True)
```

### Getting Help

- **Documentation**: [API Reference](API.md)
- **Issues**: [GitHub Issues](https://github.com/massyn/workframe/issues)
- **Source Code**: [GitHub Repository](https://github.com/massyn/workframe)

---

## Next Steps

Congratulations! You now have a solid understanding of WorkFrame. Here are some next steps:

1. **Build Your First Real Application**: Start with a simple business need
2. **Explore Advanced Features**: Custom validation, calculated fields, etc.
3. **Deploy to Production**: Use PostgreSQL and proper hosting
4. **Contribute**: Help improve WorkFrame by reporting issues or contributing code

Remember: WorkFrame is designed to make business application development feel effortless while maintaining the power and flexibility you need for real-world requirements.

Happy coding! 🚀