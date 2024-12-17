from django.urls import path

from api import views

app_name = 'robots'

urlpatterns = [
    path('', views.RobotList.as_view(), name='robot_list'),
    path('<int:pk>/', views.RobotDetail.as_view(), name='robot_detail'),
    path('<int:pk>/', views.RobotDetail.as_view(), name='robot_delete'),
    # path('robots/create/', RobotDetail.as_view(), name='robot'),
    # path('', RobotViewSet.as_view({'get': 'list'}), name='robot_list'),
    # path('', views.PostListView.as_view(), name='index'),
    # path('', views.PostListView.as_view(), name='index'),
    # path(
    #     'posts/create/',
    #     views.PostCreateView.as_view(),
    #     name='create_post'
    #  ),
    # path('posts/<int:pk>/',
    #      views.PostDetailView.as_view(),
    #      name='post_detail'),
]