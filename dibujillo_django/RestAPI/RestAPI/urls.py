"""RestAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from webserviceapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('guest', views.invitado),
    path('session', views.login),
    path('game', views.join_game),
    path('game/<str:cod>/player/<str:name>/drawing', views.get_drawing),
    path('game/<str:cod>/share', views.share_drawing),
    path('user/<str:name>', views.profile),

]
