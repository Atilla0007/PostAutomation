# Quick Start Guide

## Running the Django Server

After the project reorganization, use the following commands:

### From the project root directory:

```bash
# Activate virtual environment (if not already activated)
.venv\Scripts\activate

# Run migrations (if needed)
python backend\manage.py migrate

# Start the development server
python backend\manage.py runserver
```

### Important Notes:

1. **Always use `backend\manage.py`** - The old `manage.py` in the root has been removed
2. **Use the virtual environment** - Make sure `.venv` is activated
3. **Install dependencies** - Run `pip install -r requirements.txt` in the virtual environment if needed

## Common Issues Fixed:

- ✅ `corsheaders` module not found → Install in venv: `.venv\Scripts\python.exe -m pip install django-cors-headers`
- ✅ Wrong manage.py → Use `backend\manage.py` instead of root `manage.py`
- ✅ Migration errors → Fixed migration dependencies after app rename

## Server URL:

Once running, the server will be available at:
- http://127.0.0.1:8000/
- http://localhost:8000/

## API Endpoints:

- Admin: http://127.0.0.1:8000/admin/
- Capabilities: http://127.0.0.1:8000/api/capabilities/
- Posts: http://127.0.0.1:8000/api/posts/

