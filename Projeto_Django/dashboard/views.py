from django.shortcuts import render
import os

# Create your views here.

def site_view(request):
    env = os.environ
    GOOGLE_API_KEY = env.get('GOOGLE_API_KEY')
    context = {
        'google_api_key': GOOGLE_API_KEY
    }
    return render(request, 'dashboard/index.html', context)

