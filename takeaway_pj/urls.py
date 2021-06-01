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
from django.urls import path,re_path,include
import takeaway_pj.settings
import login_module.views
import recommend_app.views
from django.views.static import serve

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
    path('recommend/new_recommend', recommend_app.views.create_recommend),
    # path('recommend/recommend_addpic', recommend_app.views.recommend_addpic),
    # path('recommend/recommend_delpic', recommend_app.views.recommend_delpic),
    # path('recommend/upload_recommend', recommend_app.views.upload_recommend),
    path('recommend/download_pic', recommend_app.views.download_pic),
    path('recommend/user_recommend', recommend_app.views.user_recommend),
    path('recommend/all_recommend', recommend_app.views.all_recommend),
    path('recommend/update_recommend', recommend_app.views.update_recommend),
    path('recommend/sort', recommend_app.views.get_recommend_for_range_and_order),

    re_path(r'^recommend/like/$', recommend_app.views.like),
    re_path(r'^recommend/edit_recommend/$', recommend_app.views.edit_index),
    re_path(r'^recommend/get_recommend/$', recommend_app.views.get_recommend),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': takeaway_pj.settings.MEDIA_ROOT}),
    re_path(r'^recommend/delete_recommend/$', recommend_app.views.delete_recommend),
    re_path(r'^recommend/click/$', recommend_app.views.click),
    path('recommend/type_recommend', recommend_app.views.get_recommend_for_type),
    path('recommend/input_recommend', recommend_app.views.input_recommend),
]
