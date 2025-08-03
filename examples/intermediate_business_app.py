"""
Intermediate Business Application Example - WorkFrame

This example demonstrates more advanced WorkFrame features:
- Custom field types and validation
- Lookup fields (foreign keys)
- Enum fields with dropdowns
- Field customization options
- Multiple related modules

Run with: python intermediate_business_app.py
Visit: http://localhost:5000
Login: admin/admin
"""

import sys
import os
# Add the parent directory to the path to use local workframe
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from workframe import WorkFrame, crud, Field

# Create the WorkFrame application
app = WorkFrame(__name__, 
               app_name="Business Manager", 
               app_description="Comprehensive business management system")

# Create companies module first (will be referenced by contacts)
companies = crud('companies', [
    Field('name', required=True),
    Field('industry', enum=['Technology', 'Healthcare', 'Finance', 'Manufacturing', 'Retail', 'Other']),
    Field('website', placeholder='https://example.com', optional=True),
    Field('description', type='textarea', optional=True),
    Field('is_active', type='boolean', default=True)
])

# Create products module with advanced field types
products = crud('products', [
    Field('name', required=True),
    Field('price', type='currency', required=True),
    Field('category', enum=['Software', 'Hardware', 'Service', 'Consulting']),
    Field('description', type='textarea', optional=True),
    Field('launch_date', type='date', optional=True),
    Field('is_featured', type='boolean', default=False),
    Field('stock_quantity', default=0),
    Field('sku', placeholder='ABC-123', optional=True)
])

# Create contacts module with lookup field to companies
contacts = crud('contacts', [
    Field('first_name', required=True),
    Field('last_name', required=True),
    Field('email', type='email', required=True),
    Field('phone', type='phone', optional=True),
    Field('company', lookup='companies', display='name'),  # Foreign key to companies
    Field('position', optional=True),
    Field('status', enum=['Active', 'Inactive', 'Prospect'], default='Active'),
    Field('notes', type='textarea', optional=True),
    Field('created_date', type='datetime', readonly=True, hidden_in_form=True)
])

# Create projects module linking to contacts and companies
projects = crud('projects', [
    Field('name', required=True),
    Field('client_company', lookup='companies', display='name'),
    Field('contact_person', lookup='contacts', display='first_name'),
    Field('status', enum=['Planning', 'In Progress', 'On Hold', 'Completed', 'Cancelled'], default='Planning'),
    Field('start_date', type='date', required=True),
    Field('end_date', type='date', optional=True),
    Field('budget', type='currency', optional=True),
    Field('description', type='textarea', optional=True),
    Field('is_priority', type='boolean', default=False)
])

# Register modules with navigation and icons
app.register_module('/companies', companies, menu_title='Companies', icon='bi-building')
app.register_module('/contacts', contacts, menu_title='Contacts', icon='bi-people')
app.register_module('/products', products, menu_title='Products', icon='bi-box')
app.register_module('/projects', projects, menu_title='Projects', icon='bi-kanban')

if __name__ == '__main__':
    print("=" * 60)
    print("WorkFrame Intermediate Business Application Example")
    print("=" * 60)
    print("Visit: http://localhost:5000")
    print("Login with: admin/admin")
    print("")
    print("Features demonstrated:")
    print("• Custom field types (currency, date, textarea, boolean)")
    print("• Enum fields with dropdown selections")
    print("• Lookup fields (foreign key relationships)")
    print("• Field validation and requirements")
    print("• Multiple related business modules")
    print("• Field visibility controls")
    print("• Default values and placeholders")
    print("• Mobile-responsive design")
    print("")
    print("Business modules:")
    print("• Companies - Manage business clients and partners")
    print("• Contacts - Track people at companies")
    print("• Products - Manage product catalog")
    print("• Projects - Track client projects")
    print("=" * 60)
    
    app.run(debug=True)