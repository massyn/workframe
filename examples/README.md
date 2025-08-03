# WorkFrame Example Applications

This directory contains example applications that demonstrate WorkFrame's capabilities from basic to advanced use cases.

## Examples Overview

### 1. Basic Contact Manager (`basic_contact_manager.py`)
**Complexity**: Beginner  
**Features**: Basic CRUD, simple fields, auto-detection

A minimal WorkFrame application showing:
- Simple field definitions using strings
- Auto field type detection (email validation)
- Basic CRUD operations
- Mobile-responsive interface

**Run**: `python basic_contact_manager.py`

### 2. Intermediate Business App (`intermediate_business_app.py`)
**Complexity**: Intermediate  
**Features**: Custom fields, lookups, enums, validation

A more comprehensive business application demonstrating:
- Custom field types (currency, date, textarea, boolean)
- Enum fields with dropdown selections  
- Lookup fields (foreign key relationships)
- Field validation and requirements
- Multiple related business modules
- Field visibility controls

**Run**: `python intermediate_business_app.py`

### 3. Advanced ERP System (`advanced_erp_system.py`)
**Complexity**: Advanced  
**Features**: Many-to-many, linked tables, complex workflows

A full-featured ERP system showcasing:
- Many-to-one linked table views
- Many-to-many relationships with junction tables
- Complex business workflows
- Advanced field customization
- Multi-level module organization
- Enterprise-level data relationships

**Run**: `python advanced_erp_system.py`

## Getting Started

1. **Install WorkFrame**:
   ```bash
   pip install workframe
   ```

2. **Run any example**:
   ```bash
   cd examples
   python basic_contact_manager.py
   ```

3. **Access the application**:
   - Visit: http://localhost:5000
   - Login: admin/admin

## Common Features

All examples include:
- ✅ Built-in authentication system
- ✅ Admin user management interface
- ✅ Mobile-responsive design
- ✅ Search and filtering
- ✅ Pagination
- ✅ CSV export
- ✅ Bulk operations
- ✅ Form validation
- ✅ Flash messaging

## Learning Path

1. **Start with Basic** - Learn fundamental WorkFrame concepts
2. **Progress to Intermediate** - Explore advanced field types and relationships
3. **Study Advanced** - Understand complex business application patterns

## Customization

Each example can be customized by:
- Adding new fields to existing modules
- Creating additional modules
- Modifying field types and validation
- Changing navigation and icons
- Adjusting application settings

## Production Deployment

These examples use SQLite for simplicity. For production:
- Configure PostgreSQL or MySQL
- Set up proper environment variables
- Configure logging and monitoring
- Implement backup strategies

## Support

For questions about these examples:
- Check the main WorkFrame documentation
- Review the CLAUDE.md file in the root directory
- Examine the source code for implementation details