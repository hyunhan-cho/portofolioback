"""
URL configuration for config project.

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
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # 홈 페이지 (간단한 랜딩 페이지)
    path('', csrf_exempt(TemplateView.as_view(template_name='index.html')), name='home'),

    # 헬스 체크 엔드포인트
    path('healthz/', lambda request: HttpResponse('ok'), name='healthz'),

    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/chatbot/', include('chatbot.urls')),
]
