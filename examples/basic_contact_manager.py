"""
Basic Contact Manager Example - WorkFrame

This is the simplest possible WorkFrame application that demonstrates:
- Creating a basic CRUD module
- Using simple field definitions
- Registering modules with navigation

Run with: python basic_contact_manager.py
Visit: http://localhost:5000
Login: admin/admin
"""

import sys
import os
# Add the parent directory to the path to use local workframe
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from workframe import WorkFrame, crud

# Create the WorkFrame application
app = WorkFrame(__name__, 
               app_name="Contact Manager", 
               app_description="Simple contact management system")

# Create a basic contact CRUD with simple field definitions
contacts = crud('contacts', [
    'name',           # Simple text field
    'email',          # Auto-detected as email field with validation
    'phone',          # Simple text field
    'company'         # Simple text field
])

# Register the module with navigation
app.register_module('/contacts', contacts, menu_title='Contacts', icon='bi-person-lines-fill')

if __name__ == '__main__':
    print("=" * 50)
    print("WorkFrame Basic Contact Manager Example")
    print("=" * 50)
    print("Visit: http://localhost:5000")
    print("Login with: admin/admin")
    print("")
    print("Features demonstrated:")
    print("• Simple CRUD operations")
    print("• Auto field detection (email validation)")
    print("• Mobile-responsive interface") 
    print("• Built-in authentication")
    print("• Admin user management")
    print("=" * 50)
    
    app.run(debug=True)