from rest_framework import serializers
from home.models import Comment, Post, User, Group, Follow
from rest_framework.validators import UniqueTogetherValidator


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'posts', 'comments')
        ref_name = 'ReadOnlyUsers'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    post = serializers.SlugRelatedField(slug_field='id',
                                        read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class PostSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(slug_field='id',
                                         required=False,
                                         queryset=Group.objects.all())

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    title = serializers.CharField(required=True)
    text = serializers.CharField(required=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'pub_date', 'author', 'image', 'group',
                  )


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(

        slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('user', 'following')

        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            ),
        )

    def create(self, validated_data):
        if validated_data.get('user') == validated_data.get('following'):
            raise serializers.ValidationError(
                  'Нельзя подписаться на самого себя!')
        return Follow.objects.create(**validated_data)
