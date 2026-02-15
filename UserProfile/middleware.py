from django.contrib.auth.models import User
from django.http import HttpResponse


class PrefetchUser:
    def __init__(self, get_responce):
        self.get_responce = get_responce

    def __call__(self, request):
        if request.user.is_authenticated:
            request.user = User.objects.prefetch_related("profile__positions__action").get(pk=request.user.pk)

        responce = self.get_responce(request)
        return responce
