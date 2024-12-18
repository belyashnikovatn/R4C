from django.urls import path

from api.views import download_summary
from robots import views

app_name = 'robots'

urlpatterns = [
    path('', views.RobotRead.as_view(), name='read'),
    path('create/', views.RobotCreate.as_view(), name='create'),
    path('<int:pk>/', views.RobotEdit.as_view(), name='edit'),
    path('<int:pk>/delete/', views.RobotDelete.as_view(), name='delete'),
    path('home/', views.Home.as_view(), name='home'),
    path('download_summary/', download_summary, name='summary'),
]
