from django.conf.urls.static import static
from django.urls import path
from django.views.generic import RedirectView

from login_app import views
from django.conf import settings


urlpatterns = [
    path('', RedirectView.as_view(url='index', permanent=True)),
    path('index', views.index, name="index"),
    path('callback', views.callback, name="callback"),
    path('logout', views.logout, name="logout"),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
