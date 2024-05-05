"""sample URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from sample.views import my_view, hello_view, to_swot, add_swot, idea_detail


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', my_view, name='wowwow'), 
    path('hello/', hello_view, name='hello'),
    path('hello/swot/', to_swot, name='swot'),
    path('hello/swot/post', add_swot, name='addswot'),
    path('hello/swot/idea_detail/<int:id>', idea_detail, name='idea_detail')
]


