from django.views.generic import ListView, CreateView, DetailView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse

from base.models import Room, RoomGuest, RoomUser, User
from base.views.index_views import IndexListView
from base.forms import CreateRoomForm

class ShowRoomView(IndexListView):
    template_name = 'pages/room.html'
    model = Room

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        room = get_object_or_404(Room, pk=self.kwargs['pk'])
        context["title"] = room.title
        context["subtitle"] = room.subtitle
        context["room_id"] = room.pk

        if self.request.user == room.admin_user:
            context['is_allowed'] = True
            return context

        room_user = RoomUser.objects.filter(room=room, user=self.request.user)
        if room_user.exists():
            context['is_allowed'] = not room_user[0].is_deleted
        else:
            context['is_allowed'] = None

        return context

    def get_queryset(self):
        self.room = self.kwargs['pk']
        return super().get_queryset()

class CreateRoomView(LoginRequiredMixin, CreateView):
    form_class = CreateRoomForm
    model = Room

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if not form.is_valid():
            return super().post(request, *args, **kwargs)

        room = form.save(commit=False)
        if Room.objects.filter(title=room.title, admin_user=self.request.user).exists():
            messages.error(self.request, '同じタイトルのRoomは作成できません．')
            return redirect(request.META['HTTP_REFERER'])

        room.admin_user = self.request.user
        room.save()

        messages.success(self.request, 'Roomを作成しました．')
        return redirect(request.META['HTTP_REFERER'])
        

    def form_invalid(self, form):
        messages.error(self.request, 'Roomの作成に失敗しました．')
        return super().form_invalid(form)

class JoinRoomView(LoginRequiredMixin, CreateView):
    model = RoomGuest

    def get(self, request, *args, **kwargs):
        room_guest = RoomGuest.objects.filter(guest=self.request.user, room=self.kwargs['pk'])
        if room_guest.exists():
            return super().get(request, *args, **kwargs)

        room_guest.create(guest=self.request.user, room=Room.objects.get(id=self.kwargs['pk']))

        return redirect(request.META['HTTP_REFERER'])

class AcceptRoomGuestView(LoginRequiredMixin, CreateView):
    model = RoomGuest

    def get(self, request, *args, **kwargs):
        room = get_object_or_404(Room, title=kwargs['room'], admin_user=self.request.user)
        guest = get_object_or_404(User, username=kwargs['guest'])
        
        room_guest = get_object_or_404(RoomGuest, room=room, guest=guest)
        if room_guest.room.admin_user != self.request.user:
            return super().get(request, *args, **kwargs)

        room_guest.is_allowed = True
        room_guest.save()

        RoomUser.objects.create(room=room, user=guest, is_deleted=self.request.GET['do_accept'])

        data = {
            "room":room.title,
            "guest":room_guest.guest,
        }

        return JsonResponse(data)

        
