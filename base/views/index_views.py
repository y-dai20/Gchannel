from http.client import HTTPResponse
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from base.models import Post, ReplyPost, AgreePost, LikeReply, FavoritePost
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.conf import settings
from django.http import JsonResponse

def get_post_index_item(post):
    agree_count = AgreePost.objects.filter(post=post, is_agree=True).count()
    disagree_count = AgreePost.objects.filter(post=post, is_agree=False).count()
    user_agree = AgreePost.objects.filter(post=post, user=post.user).values('is_agree')
    agree_state = user_agree[0]['is_agree'] if len(user_agree) != 0 else ""
    favorite_state = FavoritePost.objects.filter(post=post, user=post.user)
    reply_count = ReplyPost.objects.filter(post=post).count()
    img_path = settings.MEDIA_URL + str(post.img) if post.img else None

    post_dict = {
        'post_id':post.id,
        'title':post.title,
        'text':post.text,
        'img_path':img_path,
        'username':post.user.username,
        'user_id':post.user.id,
        'created_at':post.created_at,
        'agree_count':agree_count,
        'disagree_count':disagree_count,
        'reply_count':reply_count,
        'agree_state':agree_state,
        'favorite_state':favorite_state,
    }

    return post_dict

class IndexListView(ListView):
    template_name = 'pages/index.html'
    model = Post
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        start_idx = int(request.POST.get('start_idx'))
        posts = Post.objects.filter(is_deleted=False).order_by('-created_at')[start_idx:start_idx + 10]
        
        json_htmls = {}
        for i, post in enumerate(posts):
            json_htmls['a'] = str(render(request, 'snippets/post.html'))

        return JsonResponse(json_htmls)

    def get_queryset(self):
        posts = Post.objects.filter(is_deleted=False).order_by('-created_at')
        
        queryset = []
        for post in posts:
            queryset.append(get_post_index_item(post))

        return queryset

class LargePostIndexListView(IndexListView):
    def get_queryset(self):
        agree_posts = AgreePost.objects.filter(post__is_deleted=False)\
            .values('post').annotate(Count('post')).order_by('-post__created_at').order_by('-post__count')

        queryset = []
        for agree_post in agree_posts:
            post = Post.objects.filter(pk=agree_post['post'])
            queryset.append(get_post_index_item(post[0]))

        return queryset

class FavoritePostIndexListView(IndexListView):
    def get_queryset(self):
        favorite_posts = FavoritePost.objects.filter(user=self.request.user).order_by('-created_at')

        queryset = []
        for favorite_post in favorite_posts:
            queryset.append(get_post_index_item(favorite_post.post))

        return queryset
