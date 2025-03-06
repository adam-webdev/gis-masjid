"""
URL configuration for mosque_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static
class CustomAdminLoginView(LoginView):
    def get_success_url(self):
        return '/dashboard/'  # Redirect ke dashboard setelah login

urlpatterns = [
    # path('admin/login/', CustomAdminLoginView.as_view(), name='admin_login'),
    path('admin/', admin.site.urls),
    path('', include('mosque.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)