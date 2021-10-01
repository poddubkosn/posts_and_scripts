from django.contrib import admin
from .models import MyScripts
from .models import Comment


class MyScriptsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'text', 'pub_date', 'author',)
    search_fields = ('title',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
    list_editable = ('text',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('myscripts', 'author', 'text', 'created',)
    search_fields = ('myscripts',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'
    list_editable = ('text',)


admin.site.register(MyScripts, MyScriptsAdmin)
admin.site.register(Comment, CommentAdmin)
