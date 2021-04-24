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

def test(request):
    return render(request, 'test.html', {})

def new_recommend(request):
    return render(request, 'new_recommend.html', {})

def login_fail(request):
    return render(request, 'login_fail.html', {})

def user_index(request):
    return render(request, 'user_index.html', {})

def show_recommend(request):
    return render(request, 'show_recommend.html', {})