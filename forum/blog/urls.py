from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.MyScriptsListView.as_view(), name='list_of_scripts'),
    path('<slug:slug>/', views.script_detail, name='script_detail'),
    path('<slug>/edit/', views.myscript_edit, name='script_edit'),
    # path('group/<slug:slug>/', views.group_posts, name='group_list'),
    # path('profile/<str:username>/', views.profile, name='profile'),
    # path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    # path('create/', views.post_create, name='post_create'),
    # path('posts/<post_id>/edit/', views.post_edit, name='post_edit'),
    path('<slug>/comment/',
          views.add_comment, name='add_comment'),
    # path('follow/', views.follow_index, name='follow_index'),
    # path(
    #     'profile/<str:username>/follow/',
    #     views.profile_follow,
    #     name='profile_follow'
    # ),
    # path(
    #     'profile/<str:username>/unfollow/',
    #     views.profile_unfollow,
    #     name='profile_unfollow'
    # ),
]