"""src URL Configuration

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
from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from src.app.views import index, user_profile, hello_view, to_swot, add_swot, idea_detail
from src.app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # APIエンドポイントは/api/以下で提供する
    path('api/', include('src.app.api_urls')),  # API用のURL設定（DRFなど）
    path('', views.index, name='index'),  # ログイン前のトップページ
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', user_profile, name='profile'),
    path('hello/', hello_view, name='hello'),
    path('hello/swot/', to_swot, name='swot'),
    path('hello/swot/post', add_swot, name='addswot'),
    path('hello/swot/idea_detail/<int:id>', idea_detail, name='idea_detail'),
    path('swot/<int:id>/delete/', views.delete_swot, name='delete_swot'),
    path('hello/four-p/', views.four_p, name='four_p_display'), 
    # Reactアプリケーションのエントリーポイント
    re_path(r'^(?:.*)/?$', TemplateView.as_view(template_name="index.html")),
]


