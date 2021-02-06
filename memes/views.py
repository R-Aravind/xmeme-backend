from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import json


class Meme(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(Meme, self).dispatch(*args, **kwargs)

    def get(self, request, userid=None):
        if userid is None:
            return HttpResponse("Hello yeet")

        return HttpResponse(
            json.dumps({
                "test": userid
            }), content_type="application/json"
        )

    def post(self, request):
        post_data = request.POST
        return HttpResponse(
            json.dumps({
                "name": post_data["name"],
                "caption": post_data["caption"],
                "url": post_data["url"]
            }), content_type="application/json"
        )
