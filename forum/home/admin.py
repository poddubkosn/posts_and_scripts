from django.contrib import admin
from .models import Post
from .models import Group
from .models import Follow
from .models import Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'pub_date', 'author', 'group',)
    search_fields = ('title', 'text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
    list_editable = ('group', 'title')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'description',)
    search_fields = ('title', 'slug',)
    empty_value_display = '-пусто-'
    list_editable = ('title', 'description')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    search_fields = ('user', 'author',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'text', 'created',)
    search_fields = ('post',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'
    list_editable = ('text',)


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Comment, CommentAdmin)
