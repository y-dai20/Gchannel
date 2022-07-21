from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from base.models import FollowUser, User, BlockUser


class FollowView(LoginRequiredMixin, DetailView):
    model = FollowUser
    template_name = 'pages/user.html'

    def get(self, request, *args, **kwargs):
        if request.user.username == kwargs['name']:
            return redirect("/")    

        follow_user = get_object_or_404(User, username=kwargs['name'])
        follow = FollowUser.objects.filter(user=request.user, followed_user=follow_user)
        
        is_done = True
        if follow.exists():
            follow.delete()
            is_done = False
        else:
            follow.create(user=request.user, followed_user=follow_user)

        data = {
            "username":kwargs['name'],
            "is_done":is_done,
            "text": "フォロー解除" if is_done else "フォロー",
        }
        
        return JsonResponse(data)

class BlockView(LoginRequiredMixin, DetailView):
    model = BlockUser
    template_name = 'pages/user.html'

    def get(self, request, *args, **kwargs):
        if request.user.username == kwargs['name']:
            return redirect("/")    

        target_user = get_object_or_404(User, username=kwargs['name'])
        block = BlockUser.objects.filter(user=request.user, blocked_user=target_user)

        if block.exists():
            block.delete()
        else:
            block.create(user=request.user, blocked_user=target_user)
            FollowUser.objects.filter(user=request.user, followed_user=target_user).delete()
        
        return redirect(request.META['HTTP_REFERER'])