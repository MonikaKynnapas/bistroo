from urllib.request import urlopen
import json

from django.views.generic import TemplateView, ListView, DetailView
from django.conf import settings
from .models import *

# Create your views here.


class HomeView(TemplateView):
    template_name = 'app_public/index.html'
