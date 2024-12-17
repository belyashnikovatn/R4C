from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api import views

app_name = 'customers'

urlpatterns = [
    path('', views.CustomerList.as_view(), name='list'),
    # path('', views.CustomerAdd.as_view(), name='add'),
    path('<int:pk>/', views.CustomerDetail.as_view(), name='detail'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
