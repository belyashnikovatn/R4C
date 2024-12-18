from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderRead.as_view(), name='read'),
    path('create/', views.OrderCreate.as_view(), name='create'),
    path('<int:pk>/', views.OrderEdit.as_view(), name='edit'),
    path('<int:pk>/delete/', views.OrderDelete.as_view(), name='delete'),
]
