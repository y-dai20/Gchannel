from django.views.generic import View
from base.views.functions import get_reply_type_id
from django.http import JsonResponse

class GetReplyTypeIdView(View):
    def get(self, request, *args, **wargs):
        type_id = get_reply_type_id(request.GET['type'])
        data = {'type_id':type_id}

        return JsonResponse(data)