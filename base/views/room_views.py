from django.views.generic import ListView
from base.models import Room

class ShowRoomView(ListView):
    template_name = 'pages/room.html'
    model = Room
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Title"
        context["subtitle"] = "Subtitle"

        room = Room.objects.filter(admin_user=self.request.user)
        if room.exists():
            context["title"] = room[0].title
            context["subtitle"] = room[0].subtitle

        return context