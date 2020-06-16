import os
import django
from django.conf import settings

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mapa_covid.settings')
# django.setup()

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


