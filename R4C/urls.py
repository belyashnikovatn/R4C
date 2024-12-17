from django.contrib import admin
from django.urls import include, path

from api.views import RobotList, RobotDetail

app_name = 'r4c'

urlpatterns = [
    path('robots/', include('robots.urls')),
    path('customers/', include('customers.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
