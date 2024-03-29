from django.shortcuts import render, get_object_or_404
from .models import Post, Group, Follow, Comment
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import User
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from forum.settings import number_of_elements_in_page
from forum.settings import EMAIL_HOST_USER, TOKEN_TELEGRAMM, CHAT_ID
from django.core.mail import send_mass_mail
from operator import itemgetter
from telegram import Bot


def index(request, author_comment=None):
    if author_comment:
        comments_list = Comment.objects.select_related('post').filter(
                        author__username=author_comment).all()
        post_list = list(set([el.post for el in comments_list]))
    else:
        post_list = Post.objects.all()
    users = [(user, user.posts.count()) for user in
             User.objects.all() if user.posts.count() > 0]
    sort_user_list = reversed(sorted(users, key=itemgetter(1)))
    author_comments = [(user, user.comments.count()) for user in
                       User.objects.all() if user.comments.count() > 0]
    sort_author_comments_list = reversed(sorted(author_comments,
                                         key=itemgetter(1)))
    group_list = Group.objects.all()
    last_post_list = (post_list[:15])
    paginator = Paginator(post_list, number_of_elements_in_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'post_list': last_post_list,
               'group_list': group_list, 'sort_user_list': sort_user_list,
               'sort_author_comments_list': sort_author_comments_list}
    if author_comment:
        return render(request, 'home/postcomments.html', context)
    if request.user.username not in ('admin', 'asd'):
        chat_id = CHAT_ID
        text = 'Зашли на твой сайт!'
        bot = Bot(token=TOKEN_TELEGRAMM)
        bot.send_message(chat_id, text)
    return render(request, 'home/index.html', context)


def group_posts(request, slug):
    author_comments = [(user, user.comments.count()) for user in
                       User.objects.all() if user.comments.count() > 0]
    sort_author_comments_list = reversed(sorted(author_comments,
                                         key=itemgetter(1)))
    
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    post_list_all = Post.objects.all()
    users = [(user, user.posts.count()) for user in
             User.objects.all() if user.posts.count() > 0]
    sort_user_list = reversed(sorted(users, key=itemgetter(1)))
    group_list = Group.objects.all()
    last_post_list = (post_list_all[:15])
    paginator = Paginator(posts, number_of_elements_in_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group, 'sort_user_list': sort_user_list,
        'page_obj': page_obj, 'group_list': group_list,
        'sort_author_comments_list': sort_author_comments_list,
        'post_list': last_post_list
    }
    return render(request, 'home/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    following = Follow.objects.filter(
        author__username=username,
        user__username=request.user.username).exists()
    post_list = author.posts.all()
    users = [(user, user.posts.count()) for user in
             User.objects.all() if user.posts.count() > 0]
    sort_user_list = reversed(sorted(users, key=itemgetter(1)))
    group_list = Group.objects.all()
    last_post_list = (post_list[:15])
    posts_count = post_list.count()
    paginator = Paginator(post_list, number_of_elements_in_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'author': author, 'page_obj': page_obj,
               'posts_count': posts_count, 'following': following,
               'post_list': last_post_list, 'group_list': group_list,
               'sort_user_list': sort_user_list}
    return render(request, 'home/profile.html', context)


def post_detail(request, post_id):
    form = CommentForm()
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    post_title = post.text
    owner_of_post = request.user == post.author
    context = {'post': post, 'post_title': post_title,
               'owner_of_post': owner_of_post,
               'form': form,
               'comments': comments, }
    return render(request, 'home/post_detail.html', context)


@login_required
def post_create(request):
    if request.method != 'POST':
        form = PostForm()
        return render(request, 'home/create_post.html', {'form': form})

    form = PostForm(request.POST, files=request.FILES or None,)
    if not form.is_valid():
        return render(request, 'home/create_post.html', {'form': form})
    post = form.save(False)
    post.author = request.user
    post.save()
    return redirect('home:profile', request.user.username)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('home:post_detail', post_id)
    if request.method != 'POST':
        form = PostForm(instance=post)
        return render(request, 'home/create_post.html',
                               {'form': form, 'is_edit': True})
    form = PostForm(request.POST, files=request.FILES or None, instance=post)
    if not form.is_valid():
        return render(request, 'home/create_post.html',
                               {'form': form, 'is_edit': True})
    form.save()
    return redirect('home:post_detail', post_id)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        list_of_recipients = [recipient.author.email for recipient in
                              post.comments.select_related('author').all()]
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
    return redirect('home:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user)
    users = [(user, user.posts.count()) for user in
             User.objects.all() if user.posts.count() > 0]
    sort_user_list = reversed(sorted(users, key=itemgetter(1)))
    group_list = Group.objects.all()
    last_post_list = (post_list[:15])
    author_comments = [(user, user.comments.count()) for user in
                       User.objects.all() if user.comments.count() > 0]
    sort_author_comments_list = reversed(sorted(author_comments,
                                         key=itemgetter(1)))
    paginator = Paginator(post_list, number_of_elements_in_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'post_list': last_post_list,
               'group_list': group_list, 'sort_user_list': sort_user_list,
               'sort_author_comments_list': sort_author_comments_list}
    return render(request, 'home/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if username != request.user.username:
        Follow.objects.filter(
            author__username=username,
            user__username=request.user.username).get_or_create(
            user=request.user, author=author)
    return redirect('home:profile', username)


@login_required
def profile_unfollow(request, username):
    follow = Follow.objects.filter(author__username=username,
                                   user__username=request.user.username)
    if follow.exists():
        follow.delete()
    return redirect('home:profile', username)
