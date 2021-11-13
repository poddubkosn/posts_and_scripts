from rest_framework import viewsets, mixins
from home.models import Comment
from home.models import Post, User, Group
from .serializers import PostSerializer, UserSerializer, FollowSerializer
from .serializers import GroupSerializer, CommentSerializer
from .permission import OwnerOrReadOnly, CustomerAccessPermissionFollow
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from django.views.generic.base import TemplateView


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (OwnerOrReadOnly, )


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (OwnerOrReadOnly, )
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (OwnerOrReadOnly, )


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (OwnerOrReadOnly, )
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        new_queryset = post.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(post=post, author=self.request.user)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    # permission_classes = (CustomerAccessPermissionFollow, )
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('author__username',)

    def get_queryset(self):
        user = self.request.user
        return user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AboutAPIView(TemplateView):
    template_name = 'api/aboutapi.html'
