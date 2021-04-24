"""takeaway_pj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
import login_module.views
import recommend_app.views

urlpatterns = [
    path('', include('index.urls')),
    path('admin/', admin.site.urls),

    path('login/log_in', login_module.views.log_in),
    path('login/log_out', login_module.views.log_out),
    path('login/register', login_module.views.register),
    path('login/email_validate', login_module.views.email_validate),
    path('login/change_pwd', login_module.views.change_pwd),
    path('login/reset_pwd', login_module.views.reset_pwd),
    path('login/upload_pic', login_module.views.upload_pic),
    path('login/download_pic', login_module.views.download_pic),
    path('login/confirm', login_module.views.user_confirm),
    path('login/upload_text', login_module.views.upload_text, name='upload_text'),

    path('get/user', login_module.views.get_current_user),
    path('recommend/new_recommend', recommend_app.views.create_recommend_0),
    path('recommend/recommend_addpic', recommend_app.views.recommend_addpic),
    path('recommend/recommend_delpic', recommend_app.views.recommend_delpic),
    path('recommend/upload_recommend', recommend_app.views.upload_recommend),
    path('recommend/delete_recommend', recommend_app.views.delete_recommend),
    path('recommend/download_pic', recommend_app.views.download_pic),
    path('recommend/user_recommend', recommend_app.views.user_recommend),
    path('recommend/all_recommend', recommend_app.views.all_recommend),
    path('recommend/show_recommend/?<id>', recommend_app.views.show_recommend)

]
