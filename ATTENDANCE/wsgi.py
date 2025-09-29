import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ATTENDANCE.settings')

application = get_wsgi_application()

# For whitenoise in production
if not os.environ.get('DEBUG', 'False').lower() == 'true':
    from whitenoise import WhiteNoise
    application = WhiteNoise(application)