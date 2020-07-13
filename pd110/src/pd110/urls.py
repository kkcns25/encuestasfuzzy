"""pd110 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from base110 import views
from .views import about
from .views import sure
from .views import slider
from .views import profile
from .views import slider_q
from .views import start_q
from .views import read_r
from .views import read_r_uploaded
from .views import start_r
from .views import delete
from .views import deleted
from .views import download
from .views import upload
from .views import viewresult
from .views import created
from .views import finished
from .views import warning
from .views import introduccion

urlpatterns = [
    url(r'^admin/', admin.site.urls), #para cambiar la url basta con cambiar el nombre de r^, el nombre de los botnoes seguira siendo el mismo
    url(r'^contact/', views.contact, name='contact'),
    url(r'^$', views.inicio, name='inicio'),
    url(r'^about/', about, name='about'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^slider/', views.slider_q, name='slider'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^start_q/', views.start_q, name='start_q'),
    url(r'^start_r/', views.start_r, name='start_r'),
    url(r'^read_r/', views.read_r, name='read_r'),
    url(r'^read_r_uploaded/', views.read_r_uploaded, name='read_r_uploaded'),
    url(r'^download/', views.download, name='download'),
    url(r'^upload/', views.upload, name='upload'),
    url(r'^create/', views.create, name='create'),
    url(r'^warning/', views.warning, name='warning'),
    url(r'^viewresult/', views.viewresult, name='viewresult'),
    url(r'^delete/', views.delete, name='delete'),
    url(r'^deleted/', views.deleted, name='deleted'),
    url(r'^sure/', views.sure, name='sure'),
    url(r'^created/', created, name='created'),
    url(r'^finished/', views.finished, name='finished'),
    url(r'^introduccion/', introduccion, name='introduccion'),
]

if settings.DEBUG: #Para asegurar que estamos en desarrollo, ya que si estamos en produccion no podemos usarlo
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



