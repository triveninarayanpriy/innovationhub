import os
import sys
import django
from pathlib import Path

# Vercel sets /var/task as the application root
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR / "innovationhubnitp"

# Ensure project is in path for imports
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Ensure base dir is in path too
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "innovationhubnitp.settings")

# Setup Django
django.setup()

# Get WSGI application
from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()

# Export for Vercel
application = app
