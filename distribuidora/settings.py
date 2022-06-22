import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True  
# In production, DEBUG = False is preferred. 

ALLOWED_HOSTS = ['*']

# DATABASES = {
#     'default': {
#         'ENGINE': 'config.py',
#         'NAME': 'u276789818_distribuidora',
#         'USER': 'u276789818_distHostinger',
#         'PASSWORD': 'HostCami2021',
#         'HOST': 'localhost' #  // in Development.
#     }
# }
SECRET_KEY = 'dev'

ROOT_URLCONF = ''

MEDIA_URL= '/media/'

MEDIA_ROOT= os.path.join(BASE_DIR, 'media')

STATIC_ROOT= os.path.join(BASE_DIR, 'static')
