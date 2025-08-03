"""
PostgreSQL Database Example - WorkFrame

This example demonstrates how to configure WorkFrame to use PostgreSQL
instead of the default SQLite database.

Prerequisites:
1. Install psycopg2: pip install psycopg2-binary
2. Create a PostgreSQL database
3. Set environment variables or modify the config below

Run with: python postgres_example.py
Visit: http://localhost:5000
Login: admin/admin
"""

import os
import sys
# Add the parent directory to the path to use local workframe
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from workframe import WorkFrame, crud, Field

# Create the WorkFrame application
app = WorkFrame(__name__, 
               app_name="PostgreSQL Example", 
               app_description="WorkFrame with PostgreSQL database")

# === DATABASE CONFIGURATION ===

# Method 1: Environment Variables (Recommended for production)
# Set these environment variables:
# export POSTGRES_HOST=localhost
# export POSTGRES_PORT=5432
# export POSTGRES_USER=your_username
# export POSTGRES_PASSWORD=your_password
# export POSTGRES_DB=workframe_db

if os.environ.get('POSTGRES_HOST'):
    # Build PostgreSQL connection string from environment variables
    db_url = (
        f"postgresql://"
        f"{os.environ.get('POSTGRES_USER')}:"
        f"{os.environ.get('POSTGRES_PASSWORD')}@"
        f"{os.environ.get('POSTGRES_HOST')}:"
        f"{os.environ.get('POSTGRES_PORT', '5432')}/"
        f"{os.environ.get('POSTGRES_DB')}"
    )
    app.app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    print(f"Using PostgreSQL database: {os.environ.get('POSTGRES_HOST')}/{os.environ.get('POSTGRES_DB')}")

# Method 2: Direct configuration (for development/testing)
elif os.environ.get('USE_POSTGRES') == '1':
    # Modify these settings for your PostgreSQL instance
    POSTGRES_CONFIG = {
        'host': 'localhost',
        'port': '5432', 
        'user': 'postgres',
        'password': 'your_password',
        'database': 'workframe_db'
    }
    
    db_url = (
        f"postgresql://"
        f"{POSTGRES_CONFIG['user']}:"
        f"{POSTGRES_CONFIG['password']}@"
        f"{POSTGRES_CONFIG['host']}:"
        f"{POSTGRES_CONFIG['port']}/"
        f"{POSTGRES_CONFIG['database']}"
    )
    app.app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    print(f"Using PostgreSQL database: {POSTGRES_CONFIG['host']}/{POSTGRES_CONFIG['database']}")

# Method 3: Heroku/Production DATABASE_URL
elif os.environ.get('DATABASE_URL'):
    app.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    print("Using DATABASE_URL from environment")

else:
    # Default to SQLite for development
    print("Using default SQLite database (workframe.db)")
    print("To use PostgreSQL:")
    print("  Method 1: Set POSTGRES_* environment variables")
    print("  Method 2: Set USE_POSTGRES=1 and modify POSTGRES_CONFIG above")
    print("  Method 3: Set DATABASE_URL environment variable")

# === SAMPLE BUSINESS MODULES ===

# Create a simple contact management system
contacts = crud('contacts', [
    Field('name', required=True),
    Field('email', type='email', required=True),
    Field('phone', type='phone', optional=True),
    Field('company', optional=True),
    Field('notes', type='textarea', optional=True),
    Field('is_active', type='boolean', default=True)
])

# Create a companies module
companies = crud('companies', [
    Field('name', required=True),
    Field('industry', enum=['Technology', 'Healthcare', 'Finance', 'Manufacturing', 'Other']),
    Field('website', placeholder='https://example.com', optional=True),
    Field('employee_count', default=0),
    Field('is_client', type='boolean', default=False)
])

# Register modules
app.register_module('/contacts', contacts, menu_title='Contacts', icon='bi-people')
app.register_module('/companies', companies, menu_title='Companies', icon='bi-building')

if __name__ == '__main__':
    print("=" * 60)
    print("WorkFrame PostgreSQL Database Example")
    print("=" * 60)
    print("Visit: http://localhost:5000")
    print("Login with: admin/admin")
    print("")
    print("Database configuration methods:")
    print("1. Environment variables (recommended):")
    print("   export POSTGRES_HOST=localhost")
    print("   export POSTGRES_USER=your_username") 
    print("   export POSTGRES_PASSWORD=your_password")
    print("   export POSTGRES_DB=workframe_db")
    print("")
    print("2. Direct configuration:")
    print("   export USE_POSTGRES=1")
    print("   (modify POSTGRES_CONFIG in the script)")
    print("")
    print("3. Heroku-style DATABASE_URL:")
    print("   export DATABASE_URL=postgresql://user:pass@host:port/db")
    print("")
    print("Prerequisites:")
    print("- Install: pip install psycopg2-binary")
    print("- Create PostgreSQL database")
    print("- Set connection parameters")
    print("=" * 60)
    
    app.run(debug=True)