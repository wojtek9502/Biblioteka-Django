from django.shortcuts import render
from library_app import views
from django.views.generic import TemplateView

# Create your views here.
class HomePage(TemplateView):
    template_name = "index.html"