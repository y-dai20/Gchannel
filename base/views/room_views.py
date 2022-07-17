from django.views.generic import ListView
from base.models import Room

class ShowRoomView(ListView):
    template_name = 'pages/room.html'
    model = Room
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        room = Room.objects.get(admin_user=self.request.user)
        context["title"] = room.title
        context["subtitle"] = room.subtitle

        return context