
from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('biblioteka.urls')),
    path('', include('django.contrib.auth.urls')),
]
