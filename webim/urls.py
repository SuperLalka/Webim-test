from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from login_app import views
from webim import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
