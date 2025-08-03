# WorkFrame Database Configuration Guide

WorkFrame supports multiple database backends through SQLAlchemy. By default, it uses SQLite for development, but you can easily configure it to use PostgreSQL, MySQL, or other databases for production.

## Default Configuration (SQLite)

WorkFrame automatically creates a SQLite database (`workframe.db`) in your current working directory if no database configuration is provided.

```python
from workframe import WorkFrame

app = WorkFrame(__name__)
# Uses SQLite by default (workframe.db)
app.run()
```

## PostgreSQL Configuration

### Prerequisites
```bash
pip install psycopg2-binary
```

### Method 1: Environment Variables (Recommended)
```bash
# Set environment variables
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_USER=your_username
export POSTGRES_PASSWORD=your_password
export POSTGRES_DB=workframe_db

# Run your application
python your_app.py
```

### Method 2: Direct Configuration
```python
from workframe import WorkFrame

app = WorkFrame(__name__)

# Configure PostgreSQL
app.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:5432/workframe_db'

app.run()
```

### Method 3: Environment-based Configuration
```python
import os
from workframe import WorkFrame

app = WorkFrame(__name__)

# Flexible configuration
if os.environ.get('POSTGRES_HOST'):
    db_url = (
        f"postgresql://"
        f"{os.environ.get('POSTGRES_USER')}:"
        f"{os.environ.get('POSTGRES_PASSWORD')}@"
        f"{os.environ.get('POSTGRES_HOST')}:"
        f"{os.environ.get('POSTGRES_PORT', '5432')}/"
        f"{os.environ.get('POSTGRES_DB')}"
    )
    app.app.config['SQLALCHEMY_DATABASE_URI'] = db_url

app.run()
```

## MySQL Configuration

### Prerequisites
```bash
pip install PyMySQL
```

### Configuration
```python
from workframe import WorkFrame

app = WorkFrame(__name__)

# MySQL configuration
app.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost:3306/workframe_db'

app.run()
```

## Production Deployment

### Heroku
Heroku automatically provides a `DATABASE_URL` environment variable:

```python
import os
from workframe import WorkFrame

app = WorkFrame(__name__)

# Heroku automatically sets DATABASE_URL
if os.environ.get('DATABASE_URL'):
    app.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

app.run()
```

### Docker with PostgreSQL
```yaml
# docker-compose.yml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: workframe_db
      POSTGRES_USER: workframe_user
      POSTGRES_PASSWORD: your_secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  app:
    build: .
    environment:
      POSTGRES_HOST: db
      POSTGRES_PORT: 5432
      POSTGRES_USER: workframe_user
      POSTGRES_PASSWORD: your_secure_password
      POSTGRES_DB: workframe_db
    ports:
      - "5000:5000"
    depends_on:
      - db

volumes:
  postgres_data:
```

## Database Migrations

WorkFrame automatically creates tables when the application starts. For production deployments:

1. **Initial Setup**: Tables are created automatically on first run
2. **Schema Changes**: Currently, you need to manually handle schema updates
3. **Data Migration**: Consider using SQLAlchemy-Migrate or Alembic for complex migrations

## Security Best Practices

### 1. Environment Variables
Never hardcode database credentials in your source code:

```python
# ❌ Bad - credentials in source code
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password123@localhost/db'

# ✅ Good - use environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
```

### 2. Connection Pooling
For production, configure connection pooling:

```python
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True
}
```

### 3. SSL Connections
For production PostgreSQL:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@host/db?sslmode=require'
```

## Testing with Different Databases

### Test Configuration
```python
import os
from workframe import WorkFrame

app = WorkFrame(__name__)

if os.environ.get('TESTING'):
    # Use in-memory SQLite for tests
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
elif os.environ.get('DATABASE_URL'):
    # Production database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# Otherwise uses default SQLite file

app.run()
```

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Check database server is running
   - Verify host/port settings
   - Check firewall settings

2. **Authentication Failed**
   - Verify username/password
   - Check user permissions
   - Ensure database exists

3. **Import Errors**
   - Install required database driver (`psycopg2-binary`, `PyMySQL`, etc.)
   - Check Python environment

4. **Performance Issues**
   - Configure connection pooling
   - Add database indexes
   - Monitor query performance

### Debug Mode
Enable SQLAlchemy echo to see SQL queries:

```python
app.config['SQLALCHEMY_ECHO'] = True  # Only for development
```

## Examples

See the `examples/` directory for complete working examples:
- `postgres_example.py` - Complete PostgreSQL configuration example
- `basic_contact_manager.py` - Simple SQLite example
- `intermediate_business_app.py` - Multi-table relationships

## Support

For database-specific questions:
- PostgreSQL: https://www.postgresql.org/docs/
- MySQL: https://dev.mysql.com/doc/
- SQLAlchemy: https://docs.sqlalchemy.org/