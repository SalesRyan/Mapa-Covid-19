from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'dashboard'

urlpatterns = [
    path('', site_view, name='site'),
    path('detalhes/<str:nome>', detalhes_view, name='detalhes')
]
