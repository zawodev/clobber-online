"""
URL configuration for backend project.

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
from django.urls import path
from django.urls import include

from django.urls import path, include
from django.http import JsonResponse

from django.conf import settings
from django.conf.urls.static import static


def health_check(request):
    return JsonResponse({"status": "ok1"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('health/', health_check, name="health_check"),

    path('api/v1/users/', include(('users.urls', 'users'), namespace='v1')),
    path('api/v2/users/', include(('users.urls', 'users'), namespace='v2')),

    path('api/v1/rooms/', include(('rooms.urls', 'rooms'), namespace='v1')),
    path('api/v2/rooms/', include(('rooms.urls', 'rooms'), namespace='v2')),

    path('api/v1/game/', include(('game.urls', 'game'), namespace='v1')),
    path('api/v2/game/', include(('game.urls', 'game'), namespace='v2')),

    path('api/v1/', include(('challenges.urls', 'challenges'), namespace='v1')),
    path('api/v2/', include(('challenges.urls', 'challenges'), namespace='v2')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

