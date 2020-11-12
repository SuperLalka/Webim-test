from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from login_app import views
from django.conf import settings

import oauth2_provider.views as oauth2_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('', RedirectView.as_view(url='index', permanent=True)),
    path('index', views.index, name="index"),
    path('callback', views.callback, name="callback"),
]


oauth2_endpoint_views = [
    path('authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path('token/', oauth2_views.TokenView.as_view(), name="token"),
    path('revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
