from django.views import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from memes.models import Meme, Comment

import json


class MemeView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(MemeView, self).dispatch(*args, **kwargs)

    def get(self, request, userid=None):
        if userid is None:
            return HttpResponse("Hello yeet")
        else:
            return HttpResponse(
                json.dumps({
                    "test": userid
                }), content_type="application/json"
            )

    def post(self, request):
        post_data = json.loads(request.body)
        meme = Meme(name=post_data["name"], caption=post_data["caption"], url=post_data["url"])
        meme.save()
        return HttpResponse(
            json.dumps({
                "id": meme.id
            }), content_type="application/json"
        )
