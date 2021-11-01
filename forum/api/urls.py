from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .views import PostViewSet, GroupViewSet, CommentViewSet, UserViewSet

app_name = 'api'


router = DefaultRouter()
router.register('groups', GroupViewSet)
router.register('users', UserViewSet)
router.register('posts', PostViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                basename='comments')


urlpatterns = [

    path('v1/', include(router.urls)),
    #path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),

]
