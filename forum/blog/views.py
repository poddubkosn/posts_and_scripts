from django.shortcuts import render, get_object_or_404
from .models import MyScripts
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import User
from .forms import MyscriptsForm, CommentForm
from django.shortcuts import redirect
from forum.settings import EMAIL_HOST_USER
from django.views import generic
from django.core.mail import send_mass_mail


# def index(request):
#     post_list = Post.objects.all()
#     paginator = Paginator(post_list, number_of_elements_in_page)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {'page_obj': page_obj}
#     return render(request, 'blog/index.html', context)
class MyScriptsListView(generic.ListView):
    model = MyScripts
    # context_object_name = 'group_list'
    template_name = 'blog/scripts_name_list.html'
    # queryset = Group.objects.all()[:3]
    # queryset = Group.objects.filter(slug__icontains='cats')

    def get_queryset(self):
        # sreturn Group.objects.filter(title__icontains='my')[:5]
        return MyScripts.objects.all()

    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super().get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым
        #  значением

        context['some_data'] = 'Список моих скриптов написанных на питоне'
        return context


def script_detail(request, slug):
    form = CommentForm()
    myscript = get_object_or_404(MyScripts, slug=slug)
    comments = myscript.comments_blog.all()
    myscript_title = myscript.text
    owner_of_post = request.user == myscript.author
    context = {'myscript': myscript, 'myscript_title': myscript_title,
               'owner_of_post': owner_of_post, 'form': form,
               'comments': comments, }
    return render(request, 'blog/script_detail.html', context)


@login_required
def myscript_edit(request, slug):
    myscript = get_object_or_404(MyScripts, slug=slug)
    if myscript.author != request.user:
        return redirect('blog:script_detail', slug)
    if request.method != 'POST':
        form = MyscriptsForm(instance=myscript)
        return render(request, 'blog/create_post.html',
                               {'form': form, 'is_edit': True})
    form = MyscriptsForm(request.POST, files=request.FILES or None,
                         instance=myscript)
    if not form.is_valid():
        return render(request, 'blog/create_post.html',
                               {'form': form, 'is_edit': True})
    form.save()
    return redirect('blog:script_detail', slug)


@login_required
def add_comment(request, slug):
    post = get_object_or_404(MyScripts, slug=slug)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.myscripts = post
        comment.save()
        list_of_recipients = [recipient.author.email for recipient in
                              post.comments_blog.select_related('author').
                              all()]
        author_email = post.author.email
        list_of_recipients.append(author_email)
        emails = list(set(list_of_recipients))
        subject = 'Новый комментарий'
        messages = []
        for email in emails:
            if email == request.user.email:
                continue
            if email == author_email:
                message_for_author = ('Привет! На твой пост пришел '
                                      'новый комментарий от пользователя '
                                      f'{request.user}.')
                message = (subject, message_for_author, EMAIL_HOST_USER,
                           [author_email, ])
                messages.append(message)
            else:
                full_name = f'{post.author.first_name} {post.author.last_name}'
                message_for_other = (f'Привет! На пост "{post}........" '
                                     f'пользователя {full_name} пришел '
                                     'новый комментарий от '
                                     f'пользователя {request.user}.')
                message = (subject, message_for_other, EMAIL_HOST_USER,
                           [email, ])
                messages.append(message)
        if len(messages) > 0:
            send_mass_mail((messages), fail_silently=False)
    return redirect('blog:script_detail', slug=slug)
