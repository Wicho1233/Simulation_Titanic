import os
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'titanic_predictor.settings')

application = get_wsgi_application()