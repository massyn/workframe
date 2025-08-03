"""
Advanced ERP System Example - WorkFrame

This example demonstrates the most advanced WorkFrame features:
- Many-to-many relationships
- Linked table views
- Complex business workflows
- Advanced field customization
- Multi-level module organization

Run with: python advanced_erp_system.py
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
               app_name="ERP System", 
               app_description="Enterprise Resource Planning System")

# === MASTER DATA MODULES ===

# Customer management
customers = crud('customers', [
    Field('company_name', required=True),
    Field('contact_name', required=True),
    Field('email', type='email', required=True),
    Field('phone', type='phone', optional=True),
    Field('address', type='textarea', optional=True),
    Field('customer_type', enum=['Individual', 'Small Business', 'Enterprise'], default='Individual'),
    Field('credit_limit', type='currency', default=0),
    Field('payment_terms', enum=['Net 15', 'Net 30', 'Net 60', 'COD'], default='Net 30'),
    Field('is_active', type='boolean', default=True),
    Field('notes', type='textarea', optional=True)
])

# Supplier management
suppliers = crud('suppliers', [
    Field('company_name', required=True),
    Field('contact_name', required=True),
    Field('email', type='email', required=True),
    Field('phone', type='phone', optional=True),
    Field('address', type='textarea', optional=True),
    Field('supplier_type', enum=['Raw Materials', 'Services', 'Equipment', 'Software']),
    Field('payment_terms', enum=['Net 15', 'Net 30', 'Net 60', 'Prepaid'], default='Net 30'),
    Field('quality_rating', enum=['Excellent', 'Good', 'Fair', 'Poor'], optional=True),
    Field('is_preferred', type='boolean', default=False),
    Field('is_active', type='boolean', default=True)
])

# Product catalog with advanced features
products = crud('products', [
    Field('sku', required=True, placeholder='PROD-001'),
    Field('name', required=True),
    Field('description', type='textarea', optional=True),
    Field('category', enum=['Electronics', 'Clothing', 'Books', 'Home', 'Sports', 'Other']),
    Field('supplier', lookup='suppliers', display='company_name'),
    Field('cost_price', type='currency', required=True),
    Field('selling_price', type='currency', required=True),
    Field('stock_quantity', default=0),
    Field('reorder_level', default=10),
    Field('unit_of_measure', enum=['Each', 'Dozen', 'Case', 'Pound', 'Gallon'], default='Each'),
    Field('is_active', type='boolean', default=True),
    Field('is_taxable', type='boolean', default=True),
    Field('created_date', type='datetime', readonly=True, hidden_in_form=True)
])

# === OPERATIONAL MODULES ===

# Sales orders
sales_orders = crud('sales_orders', [
    Field('order_number', required=True, placeholder='SO-001'),
    Field('customer', lookup='customers', display='company_name'),
    Field('order_date', type='date', required=True),
    Field('required_date', type='date', optional=True),
    Field('status', enum=['Draft', 'Confirmed', 'In Progress', 'Shipped', 'Delivered', 'Cancelled'], default='Draft'),
    Field('priority', enum=['Low', 'Normal', 'High', 'Urgent'], default='Normal'),
    Field('subtotal', type='currency', readonly=True, hidden_in_form=True),
    Field('tax_amount', type='currency', readonly=True, hidden_in_form=True),
    Field('total_amount', type='currency', readonly=True, hidden_in_form=True),
    Field('notes', type='textarea', optional=True)
])

# Purchase orders
purchase_orders = crud('purchase_orders', [
    Field('po_number', required=True, placeholder='PO-001'),
    Field('supplier', lookup='suppliers', display='company_name'),
    Field('order_date', type='date', required=True),
    Field('expected_date', type='date', optional=True),
    Field('status', enum=['Draft', 'Sent', 'Acknowledged', 'Partial', 'Received', 'Cancelled'], default='Draft'),
    Field('priority', enum=['Low', 'Normal', 'High', 'Urgent'], default='Normal'),
    Field('subtotal', type='currency', readonly=True, hidden_in_form=True),
    Field('tax_amount', type='currency', readonly=True, hidden_in_form=True),
    Field('total_amount', type='currency', readonly=True, hidden_in_form=True),
    Field('notes', type='textarea', optional=True)
])

# === LINKED TABLE EXAMPLES ===

# Create customer-contact linked view (many-to-one relationship)
customer_contacts = crud('contacts', [
    Field('first_name', required=True),
    Field('last_name', required=True),
    Field('email', type='email', required=True),
    Field('phone', type='phone', optional=True),
    Field('position', optional=True),
    Field('is_primary', type='boolean', default=False),
    Field('notes', type='textarea', optional=True)
], many_to_one='customers')

# === EMPLOYEE AND ROLE MANAGEMENT ===

# Employee management
employees = crud('employees', [
    Field('employee_id', required=True, placeholder='EMP-001'),
    Field('first_name', required=True),
    Field('last_name', required=True),
    Field('email', type='email', required=True),
    Field('phone', type='phone', optional=True),
    Field('department', enum=['Sales', 'Marketing', 'Finance', 'Operations', 'IT', 'HR']),
    Field('position', required=True),
    Field('hire_date', type='date', required=True),
    Field('salary', type='currency', optional=True),
    Field('is_active', type='boolean', default=True),
    Field('manager', lookup='employees', display='first_name', optional=True),
    Field('notes', type='textarea', optional=True)
])

# Department roles
roles = crud('roles', [
    Field('role_name', required=True),
    Field('department', enum=['Sales', 'Marketing', 'Finance', 'Operations', 'IT', 'HR']),
    Field('description', type='textarea', optional=True),
    Field('is_management', type='boolean', default=False),
    Field('is_active', type='boolean', default=True)
])

# Employee-Role assignments (many-to-many)
employee_roles = crud('employee_roles', [], many_to_many=roles)

# === REGISTER MODULES WITH ORGANIZED NAVIGATION ===

# Master Data
app.register_module('/customers', customers, menu_title='Customers', icon='bi-people-fill')
app.register_module('/suppliers', suppliers, menu_title='Suppliers', icon='bi-truck')
app.register_module('/products', products, menu_title='Products', icon='bi-box-seam')

# Operations
app.register_module('/sales-orders', sales_orders, menu_title='Sales Orders', icon='bi-cart-check')
app.register_module('/purchase-orders', purchase_orders, menu_title='Purchase Orders', icon='bi-clipboard-check')

# Customer Management
app.register_module('/customer-contacts', customer_contacts, menu_title='Customer Contacts', icon='bi-person-vcard')

# Human Resources
app.register_module('/employees', employees, menu_title='Employees', icon='bi-person-badge')
app.register_module('/roles', roles, menu_title='Roles', icon='bi-diagram-3')
app.register_module('/employee-roles', employee_roles, menu_title='Employee Roles', icon='bi-person-gear')

if __name__ == '__main__':
    print("=" * 70)
    print("WorkFrame Advanced ERP System Example")
    print("=" * 70)
    print("Visit: http://localhost:5000")
    print("Login with: admin/admin")
    print("")
    print("Advanced features demonstrated:")
    print("• Complex business workflows and data relationships")
    print("• Many-to-one linked table views (Customer → Contacts)")
    print("• Many-to-many relationships (Employee ↔ Roles)")
    print("• Advanced field types and validation")
    print("• Lookup fields with foreign key relationships")
    print("• Calculated/readonly fields")
    print("• Complex enum selections")
    print("• Multi-level business module organization")
    print("")
    print("Business modules:")
    print("• Master Data: Customers, Suppliers, Products")
    print("• Operations: Sales Orders, Purchase Orders") 
    print("• Customer Management: Linked Customer-Contact views")
    print("• Human Resources: Employees, Roles, Assignments")
    print("• Admin: User Management, Groups (built-in)")
    print("")
    print("This demonstrates WorkFrame's capability to handle")
    print("enterprise-level business applications with complex")
    print("data relationships and workflows.")
    print("=" * 70)
    
    app.run(debug=True)