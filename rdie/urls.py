from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic.base import TemplateView # new
urlpatterns = [
    # path('', include('accounting.urls')),
    # path('', TemplateView.as_view(template_name='home.html'), name='home'), # new
    path('', include('accounting.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
