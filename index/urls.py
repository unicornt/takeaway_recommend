from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_index, name='login_index'),
    path('register', views.register_index, name='register_index'),
    path('confirm', views.confirm_index, name='confirm_index'),
    path('upload_pic', views.upload_pic, name='upload_pic'),
]

