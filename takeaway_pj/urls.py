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

    path('get/user', login_module.views.get_current_user),

]
