from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def login_index(request):
    return render(request, 'login.html', {})

def register_index(request):
    return render(request, 'register.html', {})