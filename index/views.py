from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def login_index(request):
    return render(request, 'login.html', {})

def register_index(request):
    return render(request, 'register.html', {})

def confirm_index(request):
    return render(request, 'Successfully_confirmed.html', {})

def upload_pic(request):
    return render(request, 'upload_pic.html', {})

def new_recommend(request):
    return render(request, 'new_recommend.html', {})

def login_fail(request):
    return render(request, 'login_fail.html', {})