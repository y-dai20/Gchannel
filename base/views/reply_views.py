from http.client import HTTPResponse
from urllib import request
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from base.models import Post, ReplyPost, AgreePost, LikeReply, FavoritePost
from base.forms import ReplyReplyForm, ReplyPostForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import JsonResponse

from base.models.reply_models import ReplyReply

class LikeReplyView(LoginRequiredMixin, DetailView):
    model = LikeReply
    template_name = 'post/index.html'

    def get(self, request, *args, **kwargs):
        reply = get_object_or_404(ReplyPost, pk=kwargs['pk'])
        like_reply = LikeReply.objects.filter(user=request.user, reply=reply)

        is_like = True
        if like_reply.exists():
            like_reply.delete()
            is_like = False
        else:
            like_reply.create(user=request.user, reply=reply)

        json_data = {
            'reply_id':kwargs['pk'],
            'is_like':is_like,
        }

        return JsonResponse(json_data)


class ReplyPostView(LoginRequiredMixin, CreateView):
    form_class = ReplyPostForm
    template_name = 'pages/post_detail.html'
    success_url = ''

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = self.request.user
            reply.post = Post.objects.get(id=self.kwargs['pk'])

            like_post = AgreePost.objects.filter(post=kwargs['pk'], user=request.user)
            if like_post.exists():
                reply.position = 'Agree' if like_post[0].is_agree else 'Disagree'
            
            reply.save()

            return redirect("/post/" + self.kwargs['pk'] + "/")
        
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk":self.kwargs['pk']})

class ReplyDetailView(DetailView):
    template_name = 'pages/reply_detail.html'
    model = ReplyPost

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_reply'] = self.add_like_count_user(kwargs['object'])
        context['target_reply']['post_id'] = kwargs['object'].post.id

        replies = ReplyReply.objects.filter(reply=self.kwargs['pk']).order_by('-created_at')

        reply_dicts = []
        for reply in replies:
            reply_dict = self.add_like_count_user(reply)
            reply_dict['status'] = 'reply2'
            reply_dicts.append(reply_dict)
        context['reply_dicts'] = reply_dicts
        
        return context

    def add_like_count_user(self, queryset):
        dict_queryset = self.convert_q_to_dict(queryset)
        
        like_count = LikeReply.objects.filter(reply=dict_queryset['reply_id']).count()
        dict_queryset['like_count'] = like_count
        if like_count == 0:
            return dict_queryset

        dict_queryset['user_like'] = True if len(LikeReply.objects.filter(reply=dict_queryset['reply_id'], user=dict_queryset['user_id'])) != 0 else False

        return dict_queryset

    def convert_q_to_dict(self, queryset):
        dict_queryset = {
            'reply_id':queryset.id,
            'text':queryset.text,
            'username':queryset.user.username,
            'user_id':queryset.user.id,
            'created_at':queryset.created_at,
        }

        return dict_queryset

class ReplyReplyView(LoginRequiredMixin, CreateView):
    form_class = ReplyReplyForm
    template_name = 'pages/reply_detail.html'
    success_url = ''

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = self.request.user
            print(self.kwargs['pk'])
            reply.reply = ReplyPost.objects.get(pk=self.kwargs['pk'])

            reply.save()

            return redirect("/reply/" + self.kwargs['pk'] + "/")
        
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("reply_detail", kwargs={"pk":self.kwargs['pk']})

class SearchReplyView(LoginRequiredMixin, ListView):
    template_name = 'pages/post_detail.html'
    model = ReplyPost

    def get(self, request, *args, **wargs):
        pass
