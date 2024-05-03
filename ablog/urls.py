"""
URL configuration for ablog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# Importarea funcțiilor 'path' și 'include' din modulul 'django.urls', utilizate pentru definirea
# rutelor URL în aplicația Django.
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls.static import settings


urlpatterns = [
    path('admin/', admin.site.urls),  # Definirea unei rute URL către panoul de administrare Django.
    path('', include('theblog.urls')),  # Definirea unei rute URL către aplicația 'theblog'.
    path('members/', include('django.contrib.auth.urls')),
    # Include rutări pentru autentificare, delogare, resetare a parolei etc.
    path('members/', include('members.urls')),  # Definirea unei rute URL către aplicația 'members'.

    # Definirea unei rute URL cu un parametru variabil numit 'uid', care trebuie să fie un întreg.
    # Acest parametru va fi capturat din URL și transmis către funcția sau view-ul asociat cu această rută.
    # Toate rutele definite în fișierul 'members.urls' vor fi incluse și tratate în această cale, cu 'uid'-ul capturat ca parametru.
    path('<int:uid>/', include('members.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


