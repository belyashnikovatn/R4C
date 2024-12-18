from django.contrib import admin
from django.urls import include, path

from robots.views import Home

app_name = 'r4c'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('robots/', include('robots.urls')),
    path('customers/', include('customers.urls')),
    path('orders/', include('orders.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
