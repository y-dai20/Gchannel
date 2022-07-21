from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404

from base.forms import UserCreationForm
from base.models import FollowUser, BlockUser, User


class LoginView(LoginView):
    template_name = 'pages/login.html'

    def form_valid(self, form):
        messages.success(self.request, 'ログインしました．')
        return super().form_valid(form)
 
    def form_invalid(self, form):
        messages.error(self.request, 'ログインに失敗しました．')
        return super().form_invalid(form)

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = '/login/'
    template_name = 'pages/signup.html'
 
    def form_valid(self, form):
        messages.success(self.request, '新規登録が完了しました．続けてログインしてください．')
        return super().form_valid(form)

class UserDetailView(TemplateView):
    model = settings.AUTH_USER_MODEL
    template_name = 'pages/user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_user = get_object_or_404(User, username=kwargs['name'])
        context['target_user'] = target_user

        follow = FollowUser.objects.filter(user=self.request.user, followed_user=target_user)
        block = BlockUser.objects.filter(user=self.request.user, blocked_user=target_user)
        context['follow_user'] = follow
        context['block_user'] = block

        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    pass
