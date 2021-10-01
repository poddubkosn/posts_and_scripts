from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class MyScripts(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Имя скрипта',
        help_text='Поле для ввода имени скрипта')
    slug = models.SlugField(
        max_length=200,
        unique=True,
        db_index=True,
        verbose_name='slug',
        help_text='Поле для ввода slug')
    text = models.TextField(
        verbose_name='техт скрипта',
        help_text='Поле для ввода техта скрипта')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации',
                                    help_text='Дата публикации')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='myscripts',
        verbose_name='Автор публикации',
        help_text='автор публикации')

    image = models.ImageField(
        'Картинка',
        upload_to='blog/',
        blank=True,
        null=True,
        help_text='Загрузите картинку'
    )
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of the model.
        """
        return reverse('blog:script_detail', args=[str(self.slug)])

    def __str__(self) -> str:
        return self.title


# class Post(models.Model):
#     text = models.TextField(
#         verbose_name='Пост',
#         help_text='Поле для ввода поста')
#     pub_date = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name='Дата публикации',
#         help_text='Дата публикации')
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='posts',
#         verbose_name='Автор публикации',
#         help_text='автор публикации')
#     group = models.ForeignKey(
#         Group,
#         on_delete=models.SET_NULL,
#         related_name='posts',
#         blank=True, null=True,
#         verbose_name='Группа постов',
#         help_text='Поле для ввода группы постов')
#     image = models.ImageField(
#         'Картинка',
#         upload_to='posts/',
#         blank=True,
#         null=True,
#         help_text='Загрузите картинку'
#     )

#     class Meta:
#         ordering = ('-pub_date',)
#         verbose_name = 'Пост'
#         verbose_name_plural = 'Посты'

#     def __str__(self) -> str:
#         return self.text[:15]


class Comment(models.Model):
    myscripts = models.ForeignKey(
        MyScripts,
        on_delete=models.CASCADE,
        related_name='comments_blog',
        blank=True, null=True,
        verbose_name='Пост',
        help_text='Выберите пост')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments_blog',
        verbose_name='Автор комментария',
        help_text='выберите автора')
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Поле для ввода комментария')
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария',
        help_text='Дата комментария')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.text


# class Follow(models.Model):
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE,
#         related_name='follower',
#         verbose_name='Подписчик',
#         help_text='выберите подписчика')
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE,
#         related_name='following',
#         verbose_name='Автор',
#         help_text='выберите автора')

#     class Meta:
#         ordering = ('-user',)
#         verbose_name = 'Фаловер'
#         verbose_name_plural = 'Фаловеры'
#         constraints = (
#             models.UniqueConstraint(fields=('user', 'author'),
#                                     name='unique'), )

#     def __str__(self) -> str:
#         return self.user.username
