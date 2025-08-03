# WorkFrame Documentation

Welcome to WorkFrame documentation! This directory contains comprehensive guides for using the WorkFrame business application framework.

## Documentation Index

### 📚 [API Reference](API.md)
Complete API documentation covering all classes, methods, and functions in WorkFrame.

**What's inside:**
- WorkFrame class reference
- CRUD system documentation
- Field types and options
- Module classes
- Database models
- Authentication & authorization
- Template customization
- Security features
- Performance considerations
- Troubleshooting guide

### 🎓 [Tutorial](TUTORIAL.md)
Step-by-step tutorial for building business applications with WorkFrame.

**What you'll learn:**
- Getting started with your first app
- Understanding field types and validation
- Working with relationships (many-to-one, many-to-many)
- Authentication and security
- Advanced features and customization
- Real-world examples
- Database configuration
- Deployment strategies

## Quick Links

### For Beginners
Start with the **[Tutorial](TUTORIAL.md)** to learn WorkFrame through hands-on examples.

### For Developers
Jump to the **[API Reference](API.md)** for detailed technical documentation.

### Common Tasks

**Creating a CRUD module:**
```python
from workframe import crud
contacts = crud('contacts', ['name', 'email', 'phone'])
```

**Adding relationships:**
```python
contacts = crud('contacts', [
    'name', 'email', 
    Field('company', lookup='companies', display='name')
])
```

**Many-to-many relationships:**
```python
users = crud('users', ['username', 'email'], many_to_many='roles')
```

**Linked table views:**
```python
contacts = crud('contacts', ['name', 'email', 'company_id'], 
                many_to_one='companies')
```

## Getting Help

- **GitHub Issues**: [Report bugs or request features](https://github.com/massyn/workframe/issues)
- **Source Code**: [View on GitHub](https://github.com/massyn/workframe)
- **Examples**: Check the `examples/` directory for working applications

## Contributing

WorkFrame is open source and welcomes contributions! See the main repository for contribution guidelines.

---

## Documentation Organization

```
docs/
├── README.md     # This file - documentation index
├── API.md        # Complete API reference
└── TUTORIAL.md   # Step-by-step tutorial
```

Start your WorkFrame journey with the [Tutorial](TUTORIAL.md) and reference the [API documentation](API.md) as needed!