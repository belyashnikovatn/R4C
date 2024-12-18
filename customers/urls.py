from django.urls import path

from customers import views

app_name = 'customers'

urlpatterns = [
    path('', views.CustomerRead.as_view(), name='read'),
    path('create/', views.CustomerCreate.as_view(), name='create'),
    path('<int:pk>/', views.CustomerEdit.as_view(), name='edit'),
    path('<int:pk>/delete/', views.CustomerDelete.as_view(), name='delete'),
]
