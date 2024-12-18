from django.urls import path

from robots import views

app_name = 'robots'

urlpatterns = [
    path('', views.RobotRead.as_view(), name='read'),
    path('create/', views.RobotCreate.as_view(), name='create'),
    path('<int:pk>/', views.RobotEdit.as_view(), name='edit'),
    path('<int:pk>/delete/', views.RobotDelete.as_view(), name='delete'),
]
