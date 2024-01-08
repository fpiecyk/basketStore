from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('basket.urls')),
    path('authManager/', include('authManager.urls')),
]


