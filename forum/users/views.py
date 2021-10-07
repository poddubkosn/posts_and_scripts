from django.views.generic import CreateView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from .forms import CreationForm, MyUserForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from .models import User


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('home:index')
    template_name = 'users/signup.html'


class MyPasswordChange(PasswordChangeView):
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('users:reset_complete')
    template_name = 'users/password_reset_confirm.html'


@login_required
def profile_change(request):
    # if username != request.user.username:
    #     return redirect('home:index')
    user = get_object_or_404(User, username=request.user.username)
    form = MyUserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('home:index')
    return render(request, 'users/profile_edit.html',
                  {'form': form, })
