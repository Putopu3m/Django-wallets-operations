from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/wallets/', include('wallets.urls')),
    path('auth/', include('users.urls')),
]
