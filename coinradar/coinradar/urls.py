"""
URL configuration for coinradar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include

from .yasg import urlpatterns as docs_urls

import coins.urls
import users.urls
import subscriptions.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path('coins/', include(coins.urls)),
        path('users/', include(users.urls)),
        path('subscriptions/', include(subscriptions.urls)),
    ])),
]

urlpatterns += docs_urls
