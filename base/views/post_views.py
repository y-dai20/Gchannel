from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import JsonResponse

from base.models import Room, Post, ReplyPost, LikeReply, AgreePost, FavoritePost
from base.forms import PostForm
from base.views.index_views import get_post_index_item
from base.views.functions import get_reply_type_id


class PostView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'pages/index.html'
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = self.request.user
            room = request.POST.get('room')
            if len(room) != 0:
                post.room = get_object_or_404(Room, id=room)

            post.save()

            messages.success(self.request, '投稿しました．')
            return redirect(request.META['HTTP_REFERER'])
        
        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.error(self.request, '投稿に失敗しました．')
        return super().form_invalid(form)

class PostDetailView(DetailView):
    template_name = 'pages/post_detail.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        agree_reply = ReplyPost.objects.filter(post=self.kwargs['pk'], position='Agree').order_by('-created_at')
        disagree_reply = ReplyPost.objects.filter(post=self.kwargs['pk'], position='Disagree').order_by('-created_at')
        neutral_reply = ReplyPost.objects.filter(post=self.kwargs['pk'], position='Neutral').order_by('-created_at')

        reply_dicts = []
        for idx in range(max(len(agree_reply), len(disagree_reply), len(neutral_reply))):
            agree = self.add_like_count_user(agree_reply[idx]) if idx < len(agree_reply) else None
            reply_dicts.append(agree)
            neutral = self.add_like_count_user(neutral_reply[idx]) if idx < len(neutral_reply) else None
            reply_dicts.append(neutral)
            disagree = self.add_like_count_user(disagree_reply[idx]) if idx < len(disagree_reply) else None
            reply_dicts.append(disagree)

        context['reply_dicts'] = reply_dicts

        post = Post.objects.filter(pk=self.kwargs['pk'])
        post_dict = get_post_index_item(post[0])
        context['object'] = post_dict

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
            'post_id':queryset.post.id,
            'username':queryset.user.username,
            'user_id':queryset.user.id,
            'url':queryset.url,
            'img':queryset.img,
            'type':queryset.type,
            'type_id':get_reply_type_id(queryset.type),
            'position':queryset.position,
            'created_at':queryset.created_at,
        }

        return dict_queryset

class LargePostDetailView(PostDetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        reply_dicts = []
        like_replys = LikeReply.objects.filter(reply__post=self.kwargs['pk']).annotate(Count('reply'))\
            .order_by('-reply__created_at').order_by('-reply__count')
        for like_reply in like_replys:
            reply = ReplyPost.objects.filter(id=like_reply.reply.id)
            reply_dict = self.convert_q_to_dict(reply[0])
            reply_dict['like_count'] = like_reply.reply__count
            reply_dict['user_like'] = True if like_reply.user == self.request.user else False
            reply_dicts.append(reply_dict)

        context['reply_dicts'] = reply_dicts

        post = Post.objects.filter(pk=self.kwargs['pk'])
        post_dict = get_post_index_item(post[0])
        context['object'] = post_dict

        return context

class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'pages/post.html'
    form_class = PostForm
    
    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk":self.object.pk})

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['pk'])
        if request.user != post.user:
            return redirect('/') 

        return super().post(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, DetailView):
    template_name = 'pages/index.html'
    model = Post

    def get_object(self):
        obj = super().get_object()
        obj.is_deleted = True
        obj.save()
        return obj

    def get(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['pk'])
        if request.user != post.user:
            return redirect('/') 

        self.object = self.get_object()

        return redirect("/")

class PostAgreeView(LoginRequiredMixin, DetailView):
    model = AgreePost
    template_name = ''
    
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        agree_post = AgreePost.objects.filter(user=request.user, post=post)
        is_agree = True if "post/agree" in request.path else False
        
        state = "agree" if is_agree else "disagree"
        if agree_post.exists():
            if agree_post.values('is_agree')[0]['is_agree'] == is_agree:
                agree_post.delete()
                state = ""
            else:
                agree_post.update(is_agree=is_agree)
        else:
            agree_post.create(user=request.user, post=post, is_agree=is_agree)
        
        agree_count = AgreePost.objects.filter(post=post, is_agree=True).count()
        disagree_count = AgreePost.objects.filter(post=post, is_agree=False).count()

        json_data = {
            "post_id":self.kwargs['pk'], 
            "state":state,
            "agree_count":agree_count,
            "disagree_count":disagree_count,
        }

        return JsonResponse(json_data)

class FavoritePostView(LoginRequiredMixin, DetailView):
    model = FavoritePost
    template_name = 'pages/index.html'

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        favorite = FavoritePost.objects.filter(post=post, user=request.user)

        is_favorite = True
        if favorite.exists():
            favorite.delete()
            is_favorite = False
        else:
            favorite.create(post=post, user=request.user)

        json_data = {
            'post_id':kwargs['pk'],
            'is_favorite':is_favorite
        }

        return JsonResponse(json_data)