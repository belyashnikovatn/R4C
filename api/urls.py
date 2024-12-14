from django.urls import include, path
from rest_framework import routers

from api.views import (
    CustomerViewSet,
    RobotViewSet
)


v1_router = routers.DefaultRouter()

v1_router.register('robots', RobotViewSet)
v1_router.register('customers', CustomerViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
