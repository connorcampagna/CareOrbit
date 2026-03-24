import os
import sys

# Path to your project folder
path = '/home/careOrbit/CareOrbit/careOrbitMain'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'careOrbitMain.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
