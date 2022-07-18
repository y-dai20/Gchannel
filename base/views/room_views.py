from django.views.generic import ListView, CreateView, DetailView
from base.models import Room
from base.models import *
from base.views.index_views import IndexListView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from base.forms import CreateRoomForm
from django.contrib import messages

class ShowRoomView(IndexListView):
    template_name = 'pages/room.html'
    model = Room

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        room = get_object_or_404(Room, pk=self.kwargs['pk'])
        context["title"] = room.title
        context["subtitle"] = room.subtitle
        context["room_id"] = room.pk

        return context

    def get_queryset(self):
        self.room = self.kwargs['pk']
        return super().get_queryset()

class CreateRoomView(LoginRequiredMixin, CreateView):
    form_class = CreateRoomForm
    model = Room

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.admin_user = self.request.user
            room.save()

            messages.success(self.request, 'Roomを作成しました．')
            return redirect(request.META['HTTP_REFERER'])
        
        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.error(self.request, 'Roomの作成に失敗しました．')
        return super().form_invalid(form)