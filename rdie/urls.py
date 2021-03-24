from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('accounting/', include('accounting.urls')),
    path('admin/', admin.site.urls),
]
