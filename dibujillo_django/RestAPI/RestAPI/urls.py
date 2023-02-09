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
<<<<<<< HEAD
=======

from webserviceapp import views
>>>>>>> 93baa5d103d89714ce1dd0c3a9a90806f272acb4

urlpatterns = [
    path('admin/', admin.site.urls),
    path('guest', views.invitado),
<<<<<<< HEAD
    path('session', views.login),
    path('game/<str:cod>', views.join_game),
    path('game/<str:cod>/player/<str:name>/drawing', views.get_drawing),
    path('game/<str:cod>/share', views.share_drawing),
    path('user/<str:name>', views.profile),

=======
    path('users/', views.registrarUsuario),
    path('game/', views.crearPartida),
    path('game/<int:cod>', views.subirDibujo),
    path('game/<int:cod>', views.podio),
    path('drawings/<int:id>/comments', views.comentar)
>>>>>>> 93baa5d103d89714ce1dd0c3a9a90806f272acb4
]
