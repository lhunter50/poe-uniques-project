import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "poe_unique_project.settings")
django.setup()

from uniques import BaseItem, UniqueItem

