from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_index, name='login_index'),
    path('register', views.register_index, name='register_index'),
    path('confirm', views.confirm_index, name='confirm_index'),
    path('test', views.test, name='upload_pic'),
    path('new_recommend', views.new_recommend, name='new_recommend'),
    path('login_fail', views.login_fail, name='login_fail'),
    path('user_index', views.user_index, name='user_index'),
    path('show_recommend', views.show_recommend, name='show_recommend'),
    path('finish_register', views.finish_register, name='finish_register'),
    path('email_sent', views.email_sent, name='email_sent')
]

