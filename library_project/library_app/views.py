from django.shortcuts import render
from library_app import views

# Create your views here.
def index(request):
    return render(request, 'index.html')