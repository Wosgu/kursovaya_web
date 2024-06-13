from django.test import TestCase

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mess.settings')
django.setup()

print("Django settings are properly configured.")
