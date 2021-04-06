from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def login_index(request):
    return render(request, 'login.html', {})

def register_index(request):
    return render(request, 'register.html', {})

def confirm_index(request):
    return render(request, 'confirm.html', {})

def upload_pic(request):
    return render(request, 'upload_pic.html', {})

